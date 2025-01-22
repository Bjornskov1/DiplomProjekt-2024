document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');

    // get JSON-data
    var rawData = document.getElementById('calendar-data').textContent;

    try {
        var events = JSON.parse(rawData); // Convert JSON-string to JSON-object
    } catch (error) {
        console.error("Error parsing JSON:", error);
        return; // Stop here if JSON is invalid
    }

    // Initialize FullCalendar
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: events, // Use JSON-data
        eventClick: function (info) {
            alert(info.event.title + "\n" + info.event.extendedProps.description);
        }
    });

    calendar.render(); // show kalenderen
});