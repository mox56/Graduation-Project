function showtable(page) {
  document.querySelectorAll("div").forEach((div) => {
    div.style.display = "none";
  });
  document.querySelector(`#${page}`).style.display = "contents";
}

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("button").forEach((button) => {
    button.onclick = function () {
      showtable(this.dataset.page);
    };
  });
});
