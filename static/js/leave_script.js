let currentFilter = "All";

function filterLeave(status){

currentFilter = status;

let rows = document.querySelectorAll("#leaveBody tr");

rows.forEach(row => {

let statusText = row.querySelector(".status").innerText;

if(currentFilter === "All" || statusText === currentFilter){

row.style.display = "";

}
else{

row.style.display = "none";

}

});

}

function approveLeave(id){

fetch(`/leave/tutor-approve/${id}/`)
.then(response => location.reload())

}

function rejectLeave(id){

fetch(`/leave/tutor-reject/${id}/`)
.then(response => location.reload())

}

function forwardLeave(id){

fetch(`/leave/tutor-forward/${id}/`)
.then(response => location.reload())

}

document.getElementById("search").addEventListener("keyup", function(){

let value = this.value.toLowerCase();

let rows = document.querySelectorAll("#leaveBody tr");

rows.forEach(row => {

row.style.display = row.innerText.toLowerCase().includes(value) ? "" : "none";

});

});

function goBack(){

window.history.back();

}