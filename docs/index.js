$("#-popup-video-button").addEventListener("click", () => {
    $("#-popup-video").style.display = "flex";
});

$("#-popup-video").addEventListener("click", (event) => {
    event.target.style.display = "none";
});
