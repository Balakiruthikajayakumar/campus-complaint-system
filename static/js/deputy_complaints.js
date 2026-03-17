function filterComplaints(status){
  alert("Filtering: " + status);
}

// Optional search logic (basic)
document.getElementById("search").addEventListener("keyup", function(){
  let value = this.value.toLowerCase();
  let rows = document.querySelectorAll("#complaintsBody tr");

  rows.forEach(row => {
    row.style.display = row.innerText.toLowerCase().includes(value) ? "" : "none";
  });
});