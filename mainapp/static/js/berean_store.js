// store.js

document.addEventListener('DOMContentLoaded', () => {
    console.log("Store functionalities script loaded.");

    // --- Utility Functions for Modals/Sidebars ---
    const sidebarOverlay = document.getElementById('sidebar-overlay');
    const cartSidebar = document.getElementById('cart-sidebar');
    const historyModal = document.getElementById('history-modal');
    const pendingModal = document.getElementById('pending-modal');
    const accountModal = document.getElementById('account-modal');
    const productModal = document.getElementById('product-modal');

    // Utility function to open a modal/sidebar
    function openPanel(panel) {
        // Close all other panels first (optional, but good for single-panel UI)
        closeAllPanels();
        
        if (panel === cartSidebar) {
            panel.classList.remove('translate-x-full');
            panel.classList.add('translate-x-0');
        } else {
            panel.classList.remove('hidden');
            panel.classList.add('flex');
        }
        sidebarOverlay.classList.remove('hidden');
    }

    // Utility function to close all modals and sidebars
    function closeAllPanels() {
        // Sidebar
        cartSidebar.classList.remove('translate-x-0');
        cartSidebar.classList.add('translate-x-full');

        // Modals
        historyModal.classList.add('hidden');
        historyModal.classList.remove('flex');
        pendingModal.classList.add('hidden');
        pendingModal.classList.remove('flex');
        accountModal.classList.add('hidden');
        accountModal.classList.remove('flex');
        productModal.classList.add('hidden');
        productModal.classList.remove('flex');

        sidebarOverlay.classList.add('hidden');
    }
    
    // Attach event listeners to close buttons and overlay
    document.getElementById('close-cart')?.addEventListener('click', closeAllPanels);
    document.getElementById('close-history')?.addEventListener('click', closeAllPanels);
    document.getElementById('close-pending')?.addEventListener('click', closeAllPanels);
    document.getElementById('close-account')?.addEventListener('click', closeAllPanels);
    document.getElementById('close-product-modal')?.addEventListener('click', closeAllPanels);
    sidebarOverlay?.addEventListener('click', (e) => {
        // Only close if the click is directly on the overlay
        if (e.target === sidebarOverlay) {
            closeAllPanels();
        }
    });
    
    // --- Store Navigation & E-commerce Actions ---
    
    // Toggle Cart Sidebar
    document.getElementById('cart-btn')?.addEventListener('click', (e) => {
        e.preventDefault();
        openPanel(cartSidebar);
        updateCartDisplay(); // Call to ensure cart state is rendered
    });

    // Toggle History Modal
    document.getElementById('history-btn')?.addEventListener('click', (e) => {
        e.preventDefault();
        openPanel(historyModal);
    });
    
    // Toggle Pending Orders Modal
    document.getElementById('pending-btn')?.addEventListener('click', (e) => {
        e.preventDefault();
        openPanel(pendingModal);
    });

    // Toggle Account Modal
    document.getElementById('account-btn')?.addEventListener('click', (e) => {
        e.preventDefault();
        openPanel(accountModal);
    });

    // NOTE: Wishlist button and other account links are placeholders as they
    // typically require backend routes, but they open the Account Modal for now.
    document.getElementById('wishlist-btn')?.addEventListener('click', (e) => {
        e.preventDefault();
        // For a simple demo, we'll open the account modal
        openPanel(accountModal);
        // In a real app, this would redirect to a wishlist page/modal.
        console.log("Simulating redirection to Wishlist page...");
    });
    
    // Continue Shopping button (closes cart)
    document.getElementById('continue-shopping')?.addEventListener('click', closeAllPanels);

    // Placeholder for Checkout button logic
    document.getElementById('proceed-checkout-btn')?.addEventListener('click', () => {
        alert("Proceeding to Checkout! (Integration with M-Pesa/Payment Gateway would go here)");
        // In a real application, this would typically be a form submission or an API call.
    });


    // --- Search & Filter Logic ---
    const filterToggle = document.getElementById('filter-toggle');
    const filterPanel = document.getElementById('filter-panel');
    const applyFiltersBtn = document.getElementById('apply-filters');
    const clearFiltersBtn = document.getElementById('clear-filters');
    const searchInput = document.getElementById('search-input');
    const categoryFilters = document.querySelectorAll('.category-filter');
    const priceFilters = document.querySelectorAll('.price-filter');
    const sortSelect = document.getElementById('sort-select');

    // Toggle Filter Panel
    filterToggle?.addEventListener('click', () => {
        filterPanel.classList.toggle('hidden');
    });

    // Apply Filters - Simulation
    applyFiltersBtn?.addEventListener('click', () => {
        const searchTerm = searchInput.value.trim().toLowerCase();
        const selectedCategories = Array.from(categoryFilters).filter(cb => cb.checked).map(cb => cb.dataset.category);
        const selectedPrices = Array.from(priceFilters).filter(cb => cb.checked).map(cb => ({
            min: parseInt(cb.dataset.min),
            max: parseInt(cb.dataset.max)
        }));
        const sortBy = sortSelect.value;

        console.log({
            searchTerm,
            selectedCategories,
            selectedPrices,
            sortBy
        });

        alert("Applying Filters and Search... (This is where you'd re-render the product list via AJAX)");
        filterPanel.classList.add('hidden'); // Hide panel after applying
    });

    // Clear Filters - Simulation
    clearFiltersBtn?.addEventListener('click', () => {
        searchInput.value = '';
        categoryFilters.forEach(cb => cb.checked = false);
        priceFilters.forEach(cb => cb.checked = false);
        sortSelect.value = 'featured';

        alert("Filters Cleared! (You'd typically re-render the full product list)");
    });

    // --- Simulated Cart/Wishlist State Management ---
    // In a real app, this data would come from the Django backend (user session/DB)
    let cartItems = []; // [{ id: 1, name: '...', price: 500, quantity: 1, ... }]
    let wishlistCount = 0;
    
    const cartCountEl = document.getElementById('cart-count');
    const wishlistCountEl = document.getElementById('wishlist-count');
    const cartTotalEl = document.getElementById('cart-total');
    const cartItemsListEl = document.getElementById('cart-items-list');
    const emptyCartMessageEl = document.getElementById('empty-cart-message');
    const clearCartBtn = document.getElementById('clear-cart-btn');

    function updateCartCounts() {
        const totalItems = cartItems.reduce((sum, item) => sum + item.quantity, 0);
        const totalAmount = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        
        cartCountEl.textContent = totalItems;
        cartTotalEl.textContent = `KSH ${totalAmount.toLocaleString()}`;
        
        // Show/Hide relevant elements based on cart state
        if (totalItems > 0) {
            emptyCartMessageEl.classList.add('hidden');
            cartItemsListEl.classList.remove('hidden');
            clearCartBtn.classList.remove('hidden');
        } else {
            emptyCartMessageEl.classList.remove('hidden');
            cartItemsListEl.classList.add('hidden');
            clearCartBtn.classList.add('hidden');
        }
    }
    
    function updateWishlistCount(newCount) {
        wishlistCount = newCount;
        wishlistCountEl.textContent = newCount;
    }

    // Example function to add an item (simulated, needs to be attached to product cards)
    window.addToCart = (productId, name, price) => {
        const existingItem = cartItems.find(item => item.id === productId);
        
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            cartItems.push({ id: productId, name, price, quantity: 1 });
        }
        
        updateCartCounts();
        updateCartDisplay();
        alert(`${name} added to cart!`);
    };

    // Clears the cart
    clearCartBtn?.addEventListener('click', () => {
        if(confirm("Are you sure you want to clear your cart?")) {
            cartItems = [];
            updateCartCounts();
            updateCartDisplay();
        }
    });

    // Renders the cart items in the sidebar
    function updateCartDisplay() {
        cartItemsListEl.innerHTML = ''; // Clear current items
        
        cartItems.forEach(item => {
            const itemElement = document.createElement('div');
            itemElement.classList.add('flex', 'items-center', 'justify-between', 'border-b', 'py-3');
            itemElement.innerHTML = `
                <div class="flex items-center gap-3">
                    <div class="w-16 h-16 bg-gray-100 rounded-lg flex items-center justify-center">
                        <i class="fas fa-box text-xl text-sky-500"></i>
                    </div>
                    <div>
                        <p class="font-semibold text-gray-800">${item.name}</p>
                        <p class="text-sm text-gray-500">KSH ${item.price.toLocaleString()} x ${item.quantity}</p>
                    </div>
                </div>
                <div class="flex flex-col items-end">
                    <p class="font-bold text-sky-600">KSH ${(item.price * item.quantity).toLocaleString()}</p>
                    <button data-id="${item.id}" class="remove-item text-red-500 text-xs mt-1 hover:text-red-700">Remove</button>
                </div>
            `;
            cartItemsListEl.appendChild(itemElement);
        });

        // Re-attach listeners for new remove buttons
        cartItemsListEl.querySelectorAll('.remove-item').forEach(button => {
            button.addEventListener('click', (e) => {
                const itemId = parseInt(e.target.dataset.id);
                cartItems = cartItems.filter(item => item.id !== itemId);
                updateCartCounts();
                updateCartDisplay();
            });
        });
    }

    // Initialize counts on load
    updateCartCounts();
    updateWishlistCount(3); // Start with a simulated wishlist count


    // --- Featured Deals Countdown Timer ---
    function updateCountdown() {
        // Target date: Next Saturday at 11:59:59 PM (Example)
        const now = new Date();
        const nextSaturday = new Date(now);
        nextSaturday.setDate(now.getDate() + (6 - now.getDay() + 7) % 7);
        nextSaturday.setHours(23, 59, 59, 999);
        
        const distance = nextSaturday - now;

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        // const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Display the results
        document.getElementById("countdown-days").textContent = days < 10 ? '0' + days : days;
        document.getElementById("countdown-hours").textContent = hours < 10 ? '0' + hours : hours;
        document.getElementById("countdown-mins").textContent = minutes < 10 ? '0' + minutes : minutes;
        // The seconds element isn't in the HTML, only days, hours, and mins
        
        // If the countdown is finished, clear the interval
        if (distance < 0) {
            clearInterval(countdownInterval);
            document.getElementById("countdown-days").textContent = '00';
            document.getElementById("countdown-hours").textContent = '00';
            document.getElementById("countdown-mins").textContent = '00';
        }
    }
    
    // Update the countdown every minute for performance, or every second for precision.
    const countdownInterval = setInterval(updateCountdown, 60000); // Update every minute
    updateCountdown(); // Initial call to display immediately


    // --- Social Proof Ticker Simulation ---
    // Simulate real-time updates for social proof elements
    const viewersCountEl = document.getElementById('viewers-count');
    const salesCountEl = document.getElementById('sales-count');
    
    function updateSocialProof() {
        // Randomly adjust viewers count (between 10 and 25)
        const newViewers = Math.floor(Math.random() * (25 - 10 + 1)) + 10;
        viewersCountEl.textContent = newViewers;

        // Simulate new sales (increase by 1 or 0)
        let currentSales = parseInt(salesCountEl.textContent);
        if (Math.random() < 0.2) { // 20% chance of a new sale
            currentSales += 1;
            salesCountEl.textContent = currentSales;
        }
    }

    // Update social proof every 10 seconds
    setInterval(updateSocialProof, 10000);

    // --- Product Card Interaction (Simulated) ---
    // Since the HTML only provides the *structure* for the product modal,
    // this function demonstrates how a click on a product card would show details.
    
    // In a real Django setup, you'd add a class/ID to your product cards, like 'product-card'
    // and attach a click listener to all of them to call this function.
    window.showProductDetails = (productData) => {
        document.getElementById('modal-product-name').textContent = productData.name;
        document.getElementById('modal-product-price').textContent = `KSH ${productData.price.toLocaleString()}`;
        document.getElementById('modal-product-description').textContent = productData.description;
        // Update image, features, etc. here

        // Update Add to Cart button to use this product's data
        document.getElementById('modal-add-to-cart').onclick = () => {
            window.addToCart(productData.id, productData.name, productData.price);
            closeAllPanels(); // Optionally close modal after adding to cart
        };

        // Update Add to Wishlist button to use this product's data
        document.getElementById('modal-add-to-wishlist').onclick = () => {
             // Simulated: Add item ID to wishlist in backend
            console.log(`Added product ID ${productData.id} to wishlist.`);
            updateWishlistCount(wishlistCount + 1); // Simulate increment
            alert(`${productData.name} added to wishlist!`);
        };

        openPanel(productModal);
    };

    // Example of how you would call showProductDetails from a product card:
    /*
    // Product data (would come from Django template loop)
    const sampleProduct = {
        id: 101,
        name: "Holy Bible NKJV - Study Edition",
        price: 3500,
        description: "A comprehensive New King James Version Bible with study notes, concordance, and maps. Perfect for deeper devotional study.",
        // ... more data
    };
    
    // To simulate a product card click on page load:
    // setTimeout(() => showProductDetails(sampleProduct), 3000); 
    */
    
});