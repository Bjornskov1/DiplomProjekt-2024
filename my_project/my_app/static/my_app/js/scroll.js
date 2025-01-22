document.addEventListener('DOMContentLoaded', () => {
    const content = document.getElementById('content');
    if (!content) {
        console.error("The #content element is not found!");
        return;
    }

    let isScrolling = false; // Tracks whether the user is actively scrolling
    let lastY = 0; // Tracks the last pointer position

    // Pointer down: Start scrolling
    content.addEventListener('pointerdown', (e) => {
        isScrolling = true;
        lastY = e.pageY; // Record the pointer's current position
        console.log("Pointer down at:", lastY); //for debug purposes
    });


    content.addEventListener('pointermove', (e) => {
        if (!isScrolling) return; // Only scroll if pointer is active
        const deltaY = lastY - e.pageY; // Calculate movement delta
        content.scrollTop += deltaY; // Adjust scroll position dynamically
        lastY = e.pageY; // Update the last pointer position
        console.log("Pointer moved, deltaY:", deltaY, "New scrollTop:", content.scrollTop);
    });

    // Pointer up: Stop scrolling
    content.addEventListener('pointerup', () => {
        isScrolling = false;
        console.log("Pointer up, scrolling stopped.");
    });

    // Pointer cancel: Handle interruptions
    content.addEventListener('pointercancel', () => {
        isScrolling = false;
        console.log("Pointer cancelled.");
    });


    content.addEventListener('contextmenu', (e) => e.preventDefault());
});
