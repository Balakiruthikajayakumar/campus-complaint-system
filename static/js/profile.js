/* =====================================================
   PROFILE PAGE JAVASCRIPT
   Handles simple actions for tutor profile page
   ===================================================== */


/* -----------------------------------------------------
   BACK BUTTON FUNCTION
   Takes the user to the previous page
   ----------------------------------------------------- */
function goBack(){
    window.history.back();
}


/* -----------------------------------------------------
   OPTIONAL: Future enhancement
   If you want to load profile data using API
   you can enable this section later.

   Currently Django template already loads data using:
   {{ request.user.username }}
   {{ request.user.email }}
   {{ request.user.department }}

   So API call is not needed.
------------------------------------------------------ */

/*
fetch("/api/tutor-profile/")
.then(response => response.json())
.then(data => {

    document.getElementById("name").innerText = data.name;
    document.getElementById("email").innerText = data.email;
    document.getElementById("department").innerText = data.department;

    document.getElementById("tutorName").innerText =
        data.name + " | Tutor";

})
.catch(error => {
    console.log("Error loading profile:", error);
});
*/