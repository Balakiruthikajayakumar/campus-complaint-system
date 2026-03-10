// FILTER BUTTONS

function filterLeave(type){

let rows = document.querySelectorAll("#leaveBody tr");

rows.forEach(row => {

let statusElement = row.querySelector(".status");

if(!statusElement){
return;
}

let status = statusElement.innerText.trim();

if(type === "All"){
row.style.display = "";
}

else if(type === "Pending" && status === "submitted"){
row.style.display = "";
}

else if(type === "Approved" && status === "tutor_approved"){
row.style.display = "";
}

else if(type === "Forwarded" && (status === "hod_approved" || status === "deputy_approved")){
row.style.display = "";
}

else if(type === "Rejected" && status === "rejected"){
row.style.display = "";
}

else{
row.style.display = "none";
}

});

}


// SEARCH FUNCTION

document.addEventListener("DOMContentLoaded", function(){

let search = document.getElementById("search");

search.addEventListener("keyup", function(){

let value = this.value.toLowerCase();

let rows = document.querySelectorAll("#leaveBody tr");

rows.forEach(row => {

row.style.display = row.innerText.toLowerCase().includes(value) ? "" : "none";

});

});

});


// BACK BUTTON

function goBack(){
window.history.back();
}