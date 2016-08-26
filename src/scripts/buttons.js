function buttonInit() {
  var buttons = document.querySelectorAll("button.c-poem__condition-switch");
  Array.prototype.filter.call(buttons,function(b) {
    b.addEventListener("click",function buttonClick() {
      document.body.className = "is-"+this.dataset.beacon+" is-"+window.wb_status.time;
    });
  });
}

if (document.readystate == "loading") {
  document.addEventListener("DOMContentLoaded", buttonInit);
} else {
  buttonInit();
}