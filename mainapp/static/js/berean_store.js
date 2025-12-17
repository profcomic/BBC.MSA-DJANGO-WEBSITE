document.addEventListener('DOMContentLoaded', function() {

    // =========================================================
    // 1. COMPONENT & SELECTOR SETUP
    // =========================================================

    const overlay = document.getElementById('sidebar-overlay');
    
    // Select all elements that can open a component (Icons in the navigation)
    // NOTE: You must ensure these IDs exist in your 'ecommerce_nav.html' include.
    const componentToggles = document.querySelectorAll(
        '#toggle-cart-btn, #toggle-wishlist-btn, #toggle-account-btn, #toggle-history-btn, #toggle-pending-btn, .product-quick-view-btn'
    );
    
    // Select all buttons used to explicitly close a modal/sidebar (e.g., 'X' icon)
    const closeButtons = document.querySelectorAll('.close-btn');

    // =========================================================
    // 2. UNIVERSAL MODAL/SIDEBAR TOGGLE LOGIC
    // =========================================================
    
    // List of all component IDs that might be open
    const allComponents = [
        'cart-sidebar', 
        'wishlist-sidebar', 
        'account-modal', 
        'history-modal', 
        'pending-modal', 
        'product-modal'
    ].map(id => document.getElementById(id)).filter(el => el != null);


    function toggleComponent(targetId, show = null) {
        const targetComponent = document.getElementById(targetId);

        if (!targetComponent) return; // Exit if the element isn't found

        // Determine the action: true=show, false=hide, null=toggle
        const isCurrentlyHidden = targetComponent.classList.contains('hidden');
        const shouldShow = (show === true) || (show === null && isCurrentlyHidden);
        
        if (shouldShow) {
            // Hide all other components before showing the current one
            allComponents.forEach(comp => {
                if (comp.id !== targetId) {
                    comp.classList.add('hidden');
                }
            });
            
            // Show the target component and the overlay
            targetComponent.classList.remove('hidden');
            overlay.classList.remove('hidden');
        } else {
            // Hide the target component and the overlay
            targetComponent.classList.add('hidden');
            overlay.classList.add('hidden');
        }
    }

    // --- Attach Listeners to Open Buttons ---
    componentToggles.forEach(button => {
        button.addEventListener('click', function() {
            // The button's ID must map to the component ID (e.g., toggle-cart-btn -> cart-sidebar)
            // Or, use a data attribute (data-target-id) if IDs don't match 1:1.
            const targetId = button.id.replace('toggle-', '');
            toggleComponent(targetId, true);
        });
    });

    // --- Close via Specific Buttons (e.g., 'X' or 'Continue Shopping') ---
    closeButtons.forEach(button => {
        button.addEventListener('click', () => toggleComponent(button.closest('[id$="-sidebar"], [id$="-modal"]').id, false));
    });

    // --- Close via Overlay Click ---
    if (overlay) {
        overlay.addEventListener('click', () => {
            // Find the currently visible component and hide it
            const visibleComponent = allComponents.find(comp => !comp.classList.contains('hidden'));
            if (visibleComponent) {
                toggleComponent(visibleComponent.id, false);
            }
        });
    }

    // =========================================================
    // 3. FAQ ACCORDION LOGIC
    // =========================================================

    faqQuestions.forEach(question => {
    question.addEventListener('click', () => {
        const answer = question.nextElementSibling;

        // 1. Toggles the 'hidden' class (primary visibility control)
        answer.classList.toggle('hidden'); 

        // 2. *** TEMPORARY TEST: Change color to something obvious ***
        answer.classList.toggle('bg-red-200'); // Add a highly visible test color

        const chevron = question.querySelector('.fa-chevron-down');
        if (chevron) {
            chevron.classList.toggle('rotate-180');
        }
    });
});

});
    
