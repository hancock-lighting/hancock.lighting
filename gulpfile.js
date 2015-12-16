var gulp         = require('gulp'),
    autoprefixer = require('gulp-autoprefixer'),
    browserSync  = require('browser-sync'),
    cache        = require('gulp-cache'),
    concat       = require('gulp-concat'),
    gae          = require('gulp-gae'),
    imagemin     = require('gulp-imagemin'),
    jshint       = require('gulp-jshint'),
    minifycss    = require('gulp-minify-css'),
    plumber      = require('gulp-plumber'),
    rename       = require('gulp-rename'),
    sass         = require('gulp-sass'),
    sourcemaps   = require('gulp-sourcemaps'),
    uglify       = require('gulp-uglify');


gulp.task('browser-sync', function() {
  browserSync({
    proxy: "localhost:8080"
  });
});

gulp.task('bs-reload', function () {
  browserSync.reload();
});

gulp.task('gae-serve', function () {
  gulp.src('dist/app.yaml')
    .pipe(gae('dev_appserver.py', [], {}));
});

gulp.task('backend', function(){
  gulp.src(['src/backend/**/*'])
    .pipe(gulp.dest('dist/'));
});

gulp.task('static', function(){
  gulp.src(['src/static/**/*'])
    .pipe(gulp.dest('dist/static'))
    .pipe(browserSync.reload({stream:true}));
});

gulp.task('templates', function(){
  gulp.src(['src/templates/**/*'])
    .pipe(gulp.dest('dist/templates'))
    .pipe(browserSync.reload({stream:true}));
});

gulp.task('images', function(){
  gulp.src('src/images/**/*')
    .pipe(cache(imagemin({ optimizationLevel: 3, progressive: true, interlaced: true })))
    .pipe(gulp.dest('dist/static/images/'));
});

gulp.task('styles', function(){
  gulp.src(['src/styles/**/*.scss'])
    .pipe(plumber({
      errorHandler: function (error) {
        console.log(error.message);
        this.emit('end');
    }}))
    //.pipe(sourcemaps.init())
    .pipe(sass())
    //.pipe(sourcemaps.write('./maps'))
    .pipe(autoprefixer('last 2 versions'))
    .pipe(gulp.dest('dist/static/styles/'))
    .pipe(rename({suffix: '.min'}))
    .pipe(minifycss())
    .pipe(gulp.dest('dist/static/styles/'))
    .pipe(browserSync.reload({stream:true}))
});

gulp.task('scripts', function(){
  return gulp.src('src/scripts/**/*.js')
    .pipe(plumber({
      errorHandler: function (error) {
        console.log(error.message);
        this.emit('end');
    }}))
    .pipe(jshint())
    .pipe(jshint.reporter('default'))
    .pipe(concat('main.js'))
    .pipe(gulp.dest('dist/static/scripts/'))
    .pipe(rename({suffix: '.min'}))
    .pipe(uglify())
    .pipe(gulp.dest('dist/static/scripts/'))
    .pipe(browserSync.reload({stream:true}))
});

gulp.task('dist', ['backend', 'static', 'templates', 'images', 'styles', 'scripts']);

gulp.task('default', ['dist', 'gae-serve', 'browser-sync'], function(){
  gulp.watch("src/backend/**/*", ['backend']);
  gulp.watch("src/static/**/*", ['static']);
  gulp.watch("src/templates/**/*", ['templates']);
  gulp.watch("src/styles/**/*.scss", ['styles']);
  gulp.watch("src/scripts/**/*.js", ['scripts']);
  gulp.watch("src/images/**/*.js", ['images']);
});