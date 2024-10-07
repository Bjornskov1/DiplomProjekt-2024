// Function to display the current time when the button is clicked
function displayTime() {
    const currentDate = new Date();
    document.getElementById('current-time').innerHTML = "Current Time: " + currentDate.toLocaleTimeString();
}

function getCurrentDate() {
    const currentDate = new Date();
    document.getElementById('current-date').innerHTML = "Current Date: " + currentDate.toDateString();
}
