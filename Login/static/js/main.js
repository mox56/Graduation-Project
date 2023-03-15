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

function filtertable() {
  var input, filter, table, tr, td, i, txtvalue;

  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("students");
  tr = table.getElementsByTagName("tr");

  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[4];
    if (td) {
      txtvalue = td.textContent || td.innerText;
      if (txtvalue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}
