let complaints = [

{
id:"CMP001",
student:"Arjun Kumar",
complaint:"Wifi not working in hostel",
category:"Hostel",
status:"Pending"
},

{
id:"CMP002",
student:"Meera Sharma",
complaint:"Noise in girls hostel",
category:"Hostel",
status:"Pending"
},

{
id:"CMP003",
student:"Rahul",
complaint:"Broken chairs in lab",
category:"Infra",
status:"Approved"
},

{
id:"CMP004",
student:"Vikram",
complaint:"Request extra holidays",
category:"Other",
status:"Rejected"
}

]

let currentFilter="All"


function loadTable(){

let body=document.getElementById("complaintsBody")
body.innerHTML=""

complaints.forEach((c,index)=>{

if(currentFilter!="All" && c.status!=currentFilter) return

let actions=""

if(c.status=="Pending"){

actions=`
<button class="view">View</button>
<button class="approve" onclick="approveComplaint(${index})">Approve</button>
<button class="reject" onclick="rejectComplaint(${index})">Reject</button>
`

}

else if(c.status=="Approved"){

actions=`
<button class="view">View</button>
<button class="forward" onclick="forwardComplaint(${index})">Forward</button>
`

}

else{

actions=`<button class="view">View</button>`

}


let row=`

<tr>

<td>${c.id}</td>
<td>${c.student}</td>
<td>${c.complaint}</td>
<td>${c.category}</td>

<td>
<span class="status ${c.status.toLowerCase()}">
${c.status}
</span>
</td>

<td>${actions}</td>

</tr>

`

body.innerHTML+=row

})

}


function approveComplaint(i){

complaints[i].status="Approved"
loadTable()

}


function rejectComplaint(i){

complaints[i].status="Rejected"
loadTable()

}


function forwardComplaint(i){

complaints[i].status="Forwarded"
loadTable()

}


function filterComplaints(status){

currentFilter=status
loadTable()

}


document.getElementById("search").addEventListener("keyup",function(){

let value=this.value.toLowerCase()

let rows=document.querySelectorAll("#complaintTable tbody tr")

rows.forEach(r=>{
r.style.display=r.innerText.toLowerCase().includes(value)?"":"none"
})

})


function goBack(){

window.history.back()

}


loadTable()