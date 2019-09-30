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

window.addEventListener("load", () => {
    let path = window.location.pathname;
    let child = $("#-top-left-nav").firstChild;

    if (path.charAt(path.length - 1) === "/") {
        path = "/index.html";
    }

    console.log(path);

    if (path === "/index.html") {
        return;
    }

    while (child) {
        if (child.nodeType === 1) {
            if (child.href === path) {
                child.classList.add("selected");
            }
        }

        child = child.nextSibling;
    }
});
