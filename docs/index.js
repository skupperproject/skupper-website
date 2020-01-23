(function() {
    let layer = $("#-popup-video-layer");

    let escapeListener = (event) => {
        if (event.key === "Escape") {
            layer.style.display = "none";
            window.removeEventListener("keyup", escapeListener);
        }
    };

    $("#-popup-video-button").addEventListener("click", () => {
        layer.style.display = "flex";
        window.addEventListener("keyup", escapeListener);
    });

    layer.addEventListener("click", () => {
        layer.style.display = "none";
        window.removeEventListener("keyup", escapeListener);
    }, false);
})();
