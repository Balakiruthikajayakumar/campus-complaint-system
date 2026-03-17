function filterOutpass(status){
  alert("Filtering: " + status);
}

document.getElementById("search").addEventListener("keyup", function(){
  let value = this.value.toLowerCase();
  let rows = document.querySelectorAll("tbody tr");

  rows.forEach(row => {
    row.style.display = row.innerText.toLowerCase().includes(value) ? "" : "none";
  });
});