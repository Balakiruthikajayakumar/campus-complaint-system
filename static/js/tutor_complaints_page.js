function filterComplaints(status){

let rows = document.querySelectorAll("#complaintsBody tr");

rows.forEach(row => {

let complaintStatus = row.querySelector(".status").innerText.trim().toLowerCase();

if(status === "All"){
row.style.display = "";
}

else if(status === "submitted"){
if(complaintStatus === "submitted"){
row.style.display = "";
}else{
row.style.display = "none";
}
}

else if(status === "tutor_approved"){
if(complaintStatus === "tutor_approved"){
row.style.display = "";
}else{
row.style.display = "none";
}
}

else if(status === "rejected"){
if(complaintStatus === "rejected"){
row.style.display = "";
}else{
row.style.display = "none";
}
}

});

}