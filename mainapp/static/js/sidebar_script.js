document.addEventListener('DOMContentLoaded', function () {
    // Get all the necessary elements from the DOM
    const menuButton = document.getElementById('menu-button');       // The hamburger icon
    const closeButton = document.getElementById('close-sidebar');      // The 'X' button in the sidebar
    const sidebar = document.getElementById('sidebar-menu');         // The sidebar itself
    const overlay = document.getElementById('sidebar-overlay');    // The dark background overlay

    // Function to open the sidebar
    const openSidebar = () => {
        if (sidebar && overlay) {
            // Remove the class that hides it, bringing it into view
            sidebar.classList.remove('translate-x-full');
            // Show the overlay
            overlay.classList.add('active');
        }
    };

    // Function to close the sidebar
    const closeSidebar = () => {
        if (sidebar && overlay) {
            // Add the class that hides it, moving it off-screen
            sidebar.classList.add('translate-x-full');
            // Hide the overlay
            overlay.classList.remove('active');
        }
    };

    // Attach the functions to the click events of the buttons
    if (menuButton) {
        menuButton.addEventListener('click', openSidebar);
    }
    
    if (closeButton) {
        closeButton.addEventListener('click', closeSidebar);
    }

    if (overlay) {
        // Also allow clicking the overlay to close the sidebar
        overlay.addEventListener('click', closeSidebar);
    }
});