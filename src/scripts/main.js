function init() {
  if (wb_status.beacon == "raining") {
    makeItRain();
  }

  function makeItRain() {
    var canvas = document.getElementById("weather-canvas");
    var ctx = canvas.getContext("2d");
    var imgd;
    var w,h;
    var downscale = 2;

    var raintone = wb_status.time == "daytime" ? 255 : 255;

    var angle = Math.PI/8;
    var speed = 1/5;
    var sheets = [1,3,5];

    function sizeCanvas() {
      w = Math.floor(canvas.offsetWidth/downscale);
      h = Math.floor(canvas.offsetHeight/downscale);
    }

    sizeCanvas();
    window.addEventListener("resize",sizeCanvas);

    var buflen = 200000;

    var backing = new Uint8ClampedArray(buflen);


    var sheetslen = sheets.length;
    var dx = speed*Math.sin(angle)/downscale;
    var dy = speed*Math.cos(angle)/downscale;

    for (var i = 0; i<buflen; i++) {
        backing[i] = (Math.random()>0.95) ? 256/sheetslen*Math.random() : 0;
    }


    function refresh(t) {
      if (w != canvas.width) {
        canvas.width = w;
        canvas.height = h;
        imgd = ctx.createImageData(w,h);
        for (var i = 0; i<4*w*h; i++) {
          imgd.data[i] = raintone;
        }
      }

      var offsets = sheets.map(function(s) {
        var offset_x = Math.round(dx*t*s);
        var offset_y = Math.round(dy*t*s);
        return (-(offset_x+w*offset_y)%buflen)+buflen;
      });
      for (var i = 0; i<w*h; i++) {
        var imgd_i = 3+4*i;
        imgd.data[imgd_i] = 0;
        for (var s = 0; s < sheetslen; s++) {
          imgd.data[imgd_i] += backing[(offsets[s]+i)%buflen];
        }
      }
      
      ctx.putImageData(imgd, 0, 0);
      window.requestAnimationFrame(refresh);
    }
    window.requestAnimationFrame(refresh);
  }
};

if (document.readystate == "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}