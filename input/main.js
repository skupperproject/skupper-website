"use strict";

const $ = document.querySelector.bind(document);
const $$ = document.querySelectorAll.bind(document);

Element.prototype.$ = function () {
  return this.querySelector.apply(this, arguments);
};

Element.prototype.$$ = function () {
  return this.querySelectorAll.apply(this, arguments);
};

window.addEventListener("scroll", () => {
    if (window.scrollY > 50) {
        $("header").classList.add("active");
    } else {
        $("header").classList.remove("active");
    }
});
