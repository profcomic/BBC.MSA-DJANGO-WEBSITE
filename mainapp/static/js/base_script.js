// Script for the base html
document.addEventListener('DOMContentLoaded', function() {
        // Hide nav on top, show on scroll
        let lastScroll = 0;
        const nav = document.getElementById('mainNav');
        window.addEventListener('scroll', function() {
            if(window.scrollY < 50) {
                nav.classList.add('opacity-0', 'pointer-events-none');
            } else {
                nav.classList.remove('opacity-0', 'pointer-events-none');
            }
        });
        // On page load, hide if at top
        if(window.scrollY < 50) {
            nav.classList.add('opacity-0', 'pointer-events-none');
        }

        // Simple dark/light mode toggle (ensure elements with these IDs exist if you want this to work)
        const toggle = document.getElementById('theme-toggle');
        const knob = document.getElementById('toggle-knob');
        if (toggle && knob) { // Added check to prevent errors if elements don't exist
            toggle.addEventListener('click', () => {
                const html = document.documentElement;
                if (html.getAttribute('data-theme') === 'dark') {
                    html.setAttribute('data-theme', 'light');
                    knob.style.left = '0.25rem';
                } else {
                    html.setAttribute('data-theme', 'dark');
                    knob.style.left = '2.25rem';
                }
            });
        }

    const scrollButton = document.getElementById('scroll-to-bottom-btn');
    
    if (scrollButton) {
        // Defining function to get the maximum height of the entire document
        function getDocumentScrollHeight() {
            // Checks documentElement (html tag) and document.body for the largest height
            return Math.max(
                document.body.scrollHeight, 
                document.documentElement.scrollHeight, 
                document.body.offsetHeight, 
                document.documentElement.offsetHeight, 
                document.body.clientHeight, 
                document.documentElement.clientHeight
            );
        }

        scrollButton.addEventListener('click', function() {
            // Scroll to the absolute maximum height of the document
            window.scrollTo({
                top: getDocumentScrollHeight(), 
                behavior: 'smooth'
            });
        });

        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                scrollButton.style.display = 'block';  // Ensuring the button is visible when scrolled down
            } else {
                scrollButton.style.display = 'none';       // hidden at the very top
            }
        }); 
        // visibility if page reloads mid-scroll
        if (window.scrollY > 300) {
             scrollButton.style.display = 'block';
        }
        console.log("Scroll-to-bottom button successfully initialized.");
        } else {
        // This will appear in your browser's console if the button ID is wrong or missing.
        console.error("ERROR: Scroll-to-bottom button element with ID 'scroll-to-bottom-btn' not found in the DOM.");
    }
    
});
