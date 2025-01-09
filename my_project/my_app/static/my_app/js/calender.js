document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');

    // Hent JSON-data fra script-tagget
    var rawData = document.getElementById('calendar-data').textContent;

    try {
        var events = JSON.parse(rawData); // Konverter JSON-strengen til et objekt
        console.log("Parsed Events:", events); // Debug JSON i konsollen
    } catch (error) {
        console.error("Error parsing JSON:", error);
        return; // Stop her, hvis JSON ikke kan parses
    }

    // Initialiser FullCalendar
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: events, // Brug JSON-data direkte
        eventClick: function (info) {
            alert(info.event.title + "\n" + info.event.extendedProps.description);
        }
    });

    calendar.render(); // Vis kalenderen
});