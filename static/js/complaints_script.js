function filterComplaints(status){

    let rows = document.querySelectorAll("#complaintsBody tr");

    rows.forEach(row => {

        let statusClass = row.querySelector(".status").classList[1];

        if(status === "All"){
            row.style.display = "";
        }

        else if(status === statusClass){
            row.style.display = "";
        }

        else{
            row.style.display = "none";
        }

    });

}