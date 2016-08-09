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
    proxy: "127.0.0.1:8080"
  });
});

gulp.task('bs-reload', function () {
  browserSync.reload();
});

gulp.task('gae-serve', function () {
  gulp.src('dist/app.yaml')
    .pipe(gae('dev_appserver.py', [], {}));
});

var pipelines = {
  backend: {
    src: "src/backend/**/*",
    dest: "dist",
    munges: []
  },
  static: {
    src: "src/static/**/*",
    dest: "dist/static",
    munges: []
  },
  templates: {
    src: "src/templates/**/*",
    dest: "dist/templates",
    munges: []
  },
  images: {
    src: "src/images/**/*",
    dest: "dist/static/images",
    munges: [
              ["imagemin({ optimizationLevel: 3, progressive: true, interlaced: true })"]
            ]
  },
  styles: {
    src: "src/styles/**/*.scss",
    dest: "dist/static/styles",
    munges: [
              ["sass()",
               "autoprefixer('last 2 versions')"],
              ["rename({suffix: '.min'})",
               "minifycss()"]
            ]
  },
  styletemplates: {
    src: "dist/static/styles/**/*",
    dest: "dist/templates/styles",
    munges: []
  },
  scripts: {
    src: "src/scripts/**/*.js",
    dest: "dist/static/scripts",
    munges: [
              ["jshint()",
               "jshint.reporter('default')",
               "concat('main.js')"],
              ["rename({suffix: '.min'})",
               "uglify()"]
            ]
  },
};

var pipeline_names = Object.keys(pipelines);

pipeline_names.forEach(function(pn) {
  gulp.task(pn, function() {
    var p = pipelines[pn];
    var g = gulp.src(p.src)
                .pipe(plumber({
                  errorHandler: function (error) {
                    console.log(error.message);
                    this.emit('end');
                  }}));
    if (p.munges.length) {
      p.munges.forEach(function(m) {
        m.forEach(function(step) {
          g = g.pipe(eval(step));
        });
        g = g.pipe(gulp.dest(p.dest));
      });
    } else {
      g = g.pipe(gulp.dest(p.dest));
    }
    g = g.pipe(browserSync.reload({stream:true}));
  });
});

gulp.task('pipelines',pipeline_names);

gulp.task('watch-pipelines',function() {
  pipeline_names.forEach(function(pn) {
    gulp.watch(pipelines[pn].src,[pn]);
  });
})

gulp.task('default', ['pipelines', 'watch-pipelines', 'gae-serve', 'browser-sync']);
