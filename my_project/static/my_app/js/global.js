// Global Touch Scrolling Behavior
document.addEventListener('touchstart', function (event) {
    const target = event.target;

    // Allow scrolling when tapping outside interactive elements
    if (!target.matches('input, select, textarea, button')) {
        document.body.style.touchAction = 'pan-y';
    } else {
        // Restrict touch actions for inputs and interactive elements
        document.body.style.touchAction = 'manipulation';
    }
});
