function showForm(type){

document.getElementById("collegeForm").style.display="none";
document.getElementById("hostelForm").style.display="none";
document.getElementById("anonymousForm").style.display="none";

if(type==="college"){
document.getElementById("collegeForm").style.display="block";
}

if(type==="hostel"){
document.getElementById("hostelForm").style.display="block";
}

if(type==="anonymous"){
document.getElementById("anonymousForm").style.display="block";
}

}

function showHostel(gender){

let hostel=document.getElementById("hostelSelect");

hostel.innerHTML="";

if(gender==="male"){

hostel.innerHTML+=`<option>BH1</option>`;
hostel.innerHTML+=`<option>BH2</option>`;
hostel.innerHTML+=`<option>BH3</option>`;

}

if(gender==="female"){

hostel.innerHTML+=`<option>Girls Hostel</option>`;

}

}