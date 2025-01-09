const content = document.getElementById('content'); // The scrollable container
let startY = 0; // Starting Y position of the touch
let scrollY = 0; // Current scroll position

content.addEventListener('touchstart', (e) => {
    startY = e.touches[0].pageY; // Get where the touch starts
    scrollY = content.scrollTop; // Record current scroll position
});

content.addEventListener('touchmove', (e) => {
    const deltaY = startY - e.touches[0].pageY; // Calculate touch movement
    content.scrollTop = scrollY + deltaY; // Scroll the container
    e.preventDefault(); // Prevent default behavior (e.g., text selection)
});
