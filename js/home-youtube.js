// Lazy-load embedded YouTube players when a homepage video thumbnail is clicked.
document.querySelectorAll(".home_youtube_card").forEach(function (card) {
  const thumb = card.querySelector(".home_youtube_thumb");
  if (!thumb) return;

  thumb.style.cursor = "pointer";
  thumb.addEventListener("click", function () {
    const id = card.getAttribute("data-video-id");
    if (!id) return;

    const iframe = document.createElement("iframe");
    iframe.src = "https://www.youtube.com/embed/" + id + "?autoplay=1&rel=0";
    iframe.frameBorder = "0";
    iframe.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
    iframe.allowFullscreen = true;
    iframe.style.width = "100%";
    iframe.style.height = "100%";
    iframe.style.border = "0";

    thumb.innerHTML = "";
    thumb.appendChild(iframe);
  });
});
