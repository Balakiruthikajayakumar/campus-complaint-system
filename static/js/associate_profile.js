function goBack(){
  window.history.back();
}

/* FETCH DATA FROM BACKEND */
fetch("/api/associatewarden-profile/")
.then(response => response.json())
.then(data => {
  document.getElementById("name").innerText = data.name;
  document.getElementById("email").innerText = data.email;
  document.getElementById("wardenName").innerText = data.name + " | Associate Warden";
})
.catch(error => {
  console.log("Error loading profile:", error);
});