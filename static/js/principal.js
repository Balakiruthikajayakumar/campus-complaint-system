// 🔍 Search functionality only (DB data already rendered by Django)

document.addEventListener("DOMContentLoaded", function(){

    let searchInput = document.getElementById("search");

    if(searchInput){

        searchInput.addEventListener("keyup", function(){

            let value = this.value.toLowerCase();

            let rows = document.querySelectorAll("#complaintTable tbody tr");

            rows.forEach(row => {
                row.style.display = row.innerText.toLowerCase().includes(value) ? "" : "none";
            });

        });
    }

});