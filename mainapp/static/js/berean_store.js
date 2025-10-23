console.log('Berean Store JavaScript loaded');
document.addEventListener('DOMContentLoaded', () => {

  // ============================================================================
  // UTILITY FUNCTIONS
  // ============================================================================

  // Utility function to toggle visibility
  function toggleVisibility(element, show = true) {
    if (show) {
      element.classList.remove('hidden');
      element.classList.remove('translate-x-full');
      element.classList.remove('opacity-0');
      element.classList.add('flex', 'opacity-100', 'translate-x-0');
    } else {
      element.classList.add('hidden');
      element.classList.remove('flex', 'opacity-100', 'translate-x-0');
    }
  }

  // ============================================================================
  // MODAL AND SIDEBAR MANAGEMENT
  // ============================================================================

  function initializeModalsAndSidebars() {
    // Overlay toggle functions
    const overlays = {
      sidebar: document.getElementById('sidebar-overlay'),
      cartSidebar: document.getElementById('cart-sidebar'),
      wishlistSidebar: document.getElementById('wishlist-sidebar'),
      historyModal: document.getElementById('history-modal'),
      pendingModal: document.getElementById('pending-modal'),
      accountModal: document.getElementById('account-modal'),
      productModal: document.getElementById('product-modal'),
    };

    // Button references
    const btns = {
      wishlistBtn: document.getElementById('wishlist-btn'),
      cartBtn: document.getElementById('cart-btn'),
      historyBtn: document.getElementById('history-btn'),
      pendingBtn: document.getElementById('pending-btn'),
      accountBtn: document.getElementById('account-btn'),
      closeCart: document.getElementById('close-cart'),
      closeWishlist: document.getElementById('close-wishlist'),
      closeHistory: document.getElementById('close-history'),
      closePending: document.getElementById('close-pending'),
      closeAccount: document.getElementById('close-account'),
      productCloseBtn: document.getElementById('close-product-modal'),
      continueShopping: document.getElementById('continue-shopping'),
    };

    // Event listeners for opening modals/sidebars
    if (btns.wishlistBtn) {
      btns.wishlistBtn.addEventListener('click', () => {
        toggleVisibility(overlays.wishlistSidebar, true);
      });
    }

    if (btns.cartBtn) {
      btns.cartBtn.addEventListener('click', () => {
        toggleVisibility(overlays.cartSidebar, true);
      });
    }

    if (btns.historyBtn) {
      btns.historyBtn.addEventListener('click', () => {
        toggleVisibility(overlays.historyModal, true);
      });
    }

    if (btns.pendingBtn) {
      btns.pendingBtn.addEventListener('click', () => {
        toggleVisibility(overlays.pendingModal, true);
      });
    }

    if (btns.accountBtn) {
      btns.accountBtn.addEventListener('click', () => {
        toggleVisibility(overlays.accountModal, true);
      });
    }

    // Close buttons
    if (btns.closeCart) {
      btns.closeCart.addEventListener('click', () => {
        toggleVisibility(overlays.cartSidebar, false);
      });
    }

    if (btns.closeWishlist) {
      btns.closeWishlist.addEventListener('click', () => {
        toggleVisibility(overlays.wishlistSidebar, false);
      });
    }

    if (btns.closeHistory) {
      btns.closeHistory.addEventListener('click', () => {
        toggleVisibility(overlays.historyModal, false);
      });
    }

    if (btns.closePending) {
      btns.closePending.addEventListener('click', () => {
        toggleVisibility(overlays.pendingModal, false);
      });
    }

    if (btns.closeAccount) {
      btns.closeAccount.addEventListener('click', () => {
        toggleVisibility(overlays.accountModal, false);
      });
    }

    if (btns.productCloseBtn) {
      btns.productCloseBtn.addEventListener('click', () => {
        toggleVisibility(overlays.productModal, false);
      });
    }

    // Continue shopping closes cart sidebar
    const continueBtn = document.getElementById('continue-shopping');
    if (continueBtn) {
      continueBtn.addEventListener('click', () => {
        toggleVisibility(overlays.cartSidebar, false);
      });
    }

    // Overlay click to close
    Object.values(overlays).forEach(overlay => {
      if (overlay) {
        overlay.addEventListener('click', (e) => {
          if (e.target === overlay) {
            toggleVisibility(overlay, false);
          }
        });
      }
    });

    // Optional: Close modals with ESC key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        Object.values(overlays).forEach(overlay => {
          if (overlay) {
            toggleVisibility(overlay, false);
          }
        });
      }
    });
  }

  // ============================================================================
  // WISHLIST FUNCTIONALITY
  // ============================================================================

  function initializeWishlist() {
    const wishlistItemsContainer = document.getElementById('wishlist-items-list');
    const wishlistCountSpan = document.getElementById('wishlist-count');
    const wishlistEmptyMsg = document.getElementById('empty-wishlist-message');

    if (!wishlistItemsContainer || !wishlistCountSpan) return;

    // Sample wishlist array
    let wishlistItems = [];

    // Product database - this should ideally come from your Django backend
    const productDatabase = {
      // Books
      101: { name: "The Berean Study Bible", price: 1500, category: "Books" },
      102: { name: "Prayer Warrior's Guide", price: 800, category: "Books" },
      103: { name: "Faith & Purpose", price: 650, category: "Books" },
      104: { name: "Mission Minded", price: 900, category: "Books" },
      105: { name: "Youth Ministry Handbook", price: 1250, category: "Books" },
      106: { name: "History of the Early Church", price: 1100, category: "Books" },

      // Merchandise
      'merch-tshirt-01': { name: "BBC Branded T-Shirt", price: 1200, category: "Merchandise" },
      'merch-hoodie-01': { name: "BBC Hoodie", price: 2500, category: "Merchandise" },
      'merch-mug-01': { name: "BBC Coffee Mug", price: 500, category: "Merchandise" },
      'merch-cap-01': { name: "Branded Baseball Cap", price: 800, category: "Merchandise" },
      'merch-lanyard-01': { name: "Event Lanyard", price: 150, category: "Merchandise" },
      'merch-bag-01': { name: "Tote Bag", price: 750, category: "Merchandise" },

      // Food & Snacks
      'food-101': { name: "Fresh Watermelon", price: 150, category: "Food & Snacks" },
      'food-102': { name: "Pilau Rice", price: 200, category: "Food & Snacks" },
      'food-103': { name: "Chicken Biryani", price: 250, category: "Food & Snacks" },
      'food-104': { name: "Crispy Bhajia", price: 100, category: "Food & Snacks" },
      'food-105': { name: "Fried Potatoes", price: 80, category: "Food & Snacks" },
      'food-106': { name: "Fresh Doughnuts", price: 50, category: "Food & Snacks" },
      'food-107': { name: "Beef Samosas", price: 30, category: "Food & Snacks" },
      'food-108': { name: "Mandazi", price: 20, category: "Food & Snacks" },
      'food-109': { name: "Soft Chapati", price: 30, category: "Food & Snacks" },
      'pack-301': { name: "Mixed Snacks Pack", price: 200, category: "Food & Snacks" },
      'service-401': { name: "Event Catering", price: 500, category: "Services" },

      // Beverages
      'drink-201': { name: "Fresh Orange Juice", price: 100, category: "Beverages" },
      'drink-202': { name: "Passion Fruit Juice", price: 120, category: "Beverages" },
      'drink-203': { name: "Fresh Mango Juice", price: 130, category: "Beverages" },
      'drink-204': { name: "Pineapple Juice", price: 110, category: "Beverages" },
      'drink-205': { name: "Mixed Fruit Juice", price: 140, category: "Beverages" },
      'drink-206': { name: "Fresh Lemon Water", price: 60, category: "Beverages" },
      'drink-207': { name: "Herbal Tea", price: 80, category: "Beverages" },
      'drink-208': { name: "Ginger Tea", price: 70, category: "Beverages" }
    };

    // Add to wishlist function
    document.querySelectorAll('.wishlist-icon, #modal-add-to-wishlist').forEach(btn => {
      if (btn) {
        btn.addEventListener('click', () => {
          const productId = btn.dataset.productId || btn.closest('[data-product-id]')?.dataset.productId;
          if (productId && productDatabase[productId]) {
            const product = productDatabase[productId];
            const newItem = {
              id: productId,
              name: product.name,
              price: product.price,
              category: product.category
            };
            wishlistItems.push(newItem);
            updateWishlist();
          } else {
            // Fallback for demo purposes
            const newItem = {
              id: Date.now(),
              name: 'Sample Wishlist Item',
              price: 500,
              category: 'General'
            };
            wishlistItems.push(newItem);
            updateWishlist();
          }
        });
      }
    });

    function updateWishlist() {
      wishlistCountSpan.textContent = wishlistItems.length;
      if (wishlistItems.length === 0) {
        wishlistEmptyMsg.classList.remove('hidden');
        wishlistItemsContainer.classList.add('hidden');
      } else {
        wishlistEmptyMsg.classList.add('hidden');
        wishlistItemsContainer.classList.remove('hidden');
        // Render wishlist items with proper product information
        wishlistItemsContainer.innerHTML = wishlistItems.map(item => `
          <div class="flex justify-between items-center bg-gray-50 p-4 rounded-lg">
            <div>
              <p class="font-semibold">${item.name}</p>
              <p class="text-sm text-gray-500">KSH ${item.price.toLocaleString()}</p>
            </div>
            <button class="text-red-500 remove-wishlist-item" data-id="${item.id}">
              <i class="fas fa-trash"></i>
            </button>
          </div>
        `).join('');
      }

      // Attach remove event
      document.querySelectorAll('.remove-wishlist-item').forEach(btn => {
        btn.addEventListener('click', () => {
          const id = btn.dataset.id;
          wishlistItems = wishlistItems.filter(i => i.id !== id);
          updateWishlist();
        });
      });
    }

    // Initialize wishlist
    updateWishlist();
  }

  // ============================================================================
  // CART FUNCTIONALITY
  // ============================================================================

  function initializeCart() {
    const cartItemsContainer = document.getElementById('cart-items-list');
    const cartCountSpan = document.getElementById('cart-count');
    const cartTotalSpan = document.getElementById('cart-total');
    const emptyCartMsg = document.getElementById('empty-cart-message');
    const clearCartBtn = document.getElementById('clear-cart-btn');
    const checkoutBtn = document.getElementById('proceed-checkout-btn');

    if (!cartItemsContainer || !cartCountSpan) return;

    let cartItems = [];

    // Product database - this should ideally come from your Django backend
    const productDatabase = {
      // Books
      101: { name: "The Berean Study Bible", price: 1500, category: "Books" },
      102: { name: "Prayer Warrior's Guide", price: 800, category: "Books" },
      103: { name: "Faith & Purpose", price: 650, category: "Books" },
      104: { name: "Mission Minded", price: 900, category: "Books" },
      105: { name: "Youth Ministry Handbook", price: 1250, category: "Books" },
      106: { name: "History of the Early Church", price: 1100, category: "Books" },

      // Merchandise
      'merch-tshirt-01': { name: "BBC Branded T-Shirt", price: 1200, category: "Merchandise" },
      'merch-hoodie-01': { name: "BBC Hoodie", price: 2500, category: "Merchandise" },
      'merch-mug-01': { name: "BBC Coffee Mug", price: 500, category: "Merchandise" },
      'merch-cap-01': { name: "Branded Baseball Cap", price: 800, category: "Merchandise" },
      'merch-lanyard-01': { name: "Event Lanyard", price: 150, category: "Merchandise" },
      'merch-bag-01': { name: "Tote Bag", price: 750, category: "Merchandise" },

      // Food & Snacks
      'food-101': { name: "Fresh Watermelon", price: 150, category: "Food & Snacks" },
      'food-102': { name: "Pilau Rice", price: 200, category: "Food & Snacks" },
      'food-103': { name: "Chicken Biryani", price: 250, category: "Food & Snacks" },
      'food-104': { name: "Crispy Bhajia", price: 100, category: "Food & Snacks" },
      'food-105': { name: "Fried Potatoes", price: 80, category: "Food & Snacks" },
      'food-106': { name: "Fresh Doughnuts", price: 50, category: "Food & Snacks" },
      'food-107': { name: "Beef Samosas", price: 30, category: "Food & Snacks" },
      'food-108': { name: "Mandazi", price: 20, category: "Food & Snacks" },
      'food-109': { name: "Soft Chapati", price: 30, category: "Food & Snacks" },
      'pack-301': { name: "Mixed Snacks Pack", price: 200, category: "Food & Snacks" },
      'service-401': { name: "Event Catering", price: 500, category: "Services" },

      // Beverages
      'drink-201': { name: "Fresh Orange Juice", price: 100, category: "Beverages" },
      'drink-202': { name: "Passion Fruit Juice", price: 120, category: "Beverages" },
      'drink-203': { name: "Fresh Mango Juice", price: 130, category: "Beverages" },
      'drink-204': { name: "Pineapple Juice", price: 110, category: "Beverages" },
      'drink-205': { name: "Mixed Fruit Juice", price: 140, category: "Beverages" },
      'drink-206': { name: "Fresh Lemon Water", price: 60, category: "Beverages" },
      'drink-207': { name: "Herbal Tea", price: 80, category: "Beverages" },
      'drink-208': { name: "Ginger Tea", price: 70, category: "Beverages" }
    };

    // Sample add to cart buttons
    document.querySelectorAll('.bg-sky-600, #modal-add-to-cart, .add-to-cart-btn').forEach(btn => {
      if (btn) {
        btn.addEventListener('click', () => {
          const productId = btn.dataset.productId || btn.closest('[data-product-id]')?.dataset.productId;
          if (productId && productDatabase[productId]) {
            const product = productDatabase[productId];
            const newItem = {
              id: productId,
              name: product.name,
              price: product.price,
              quantity: 1,
              category: product.category
            };

            // Check if item exists, update quantity if so
            const existing = cartItems.find(i => i.id === newItem.id);
            if (existing) {
              existing.quantity += 1;
            } else {
              cartItems.push(newItem);
            }
            updateCart();
          } else {
            // Fallback for demo purposes
            const newItem = {
              id: Date.now(),
              name: 'Sample Product',
              price: 500,
              quantity: 1,
              category: 'General'
            };
            const existing = cartItems.find(i => i.id === newItem.id);
            if (existing) {
              existing.quantity += 1;
            } else {
              cartItems.push(newItem);
            }
            updateCart();
          }
        });
      }
    });

    function updateCart() {
      cartCountSpan.textContent = cartItems.reduce((sum, item) => sum + item.quantity, 0);
      const total = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0);
      cartTotalSpan.textContent = `KSH ${total.toLocaleString()}`;
      if (cartItems.length === 0) {
        emptyCartMsg.classList.remove('hidden');
        cartItemsContainer.classList.add('hidden');
      } else {
        emptyCartMsg.classList.add('hidden');
        cartItemsContainer.classList.remove('hidden');
        // Render cart items
        cartItemsContainer.innerHTML = cartItems.map(item => `
          <div class="flex justify-between items-center bg-gray-50 p-4 rounded-lg">
            <div>
              <p class="font-semibold">${item.name}</p>
              <p class="text-sm text-gray-500">KSH ${item.price.toLocaleString()} x ${item.quantity}</p>
            </div>
            <div class="flex items-center gap-2">
              <button class="decrease-qty bg-gray-200 px-2 rounded" data-id="${item.id}">-</button>
              <span>${item.quantity}</span>
              <button class="increase-qty bg-gray-200 px-2 rounded" data-id="${item.id}">+</button>
              <button class="remove-cart-item text-red-500 ml-2" data-id="${item.id}">
                <i class="fas fa-trash"></i>
              </button>
            </div>
          </div>
        `).join('');

        // Attach quantity buttons
        document.querySelectorAll('.increase-qty').forEach(btn => {
          btn.addEventListener('click', () => {
            const id = parseInt(btn.dataset.id);
            const item = cartItems.find(i => i.id === id);
            if (item) {
              item.quantity += 1;
              updateCart();
            }
          });
        });
        document.querySelectorAll('.decrease-qty').forEach(btn => {
          btn.addEventListener('click', () => {
            const id = parseInt(btn.dataset.id);
            const item = cartItems.find(i => i.id === id);
            if (item && item.quantity > 1) {
              item.quantity -= 1;
              updateCart();
            }
          });
        });
        document.querySelectorAll('.remove-cart-item').forEach(btn => {
          btn.addEventListener('click', () => {
            const id = parseInt(btn.dataset.id);
            cartItems = cartItems.filter(i => i.id !== id);
            updateCart();
          });
        });
      }
    }

    // Clear cart
    if (clearCartBtn) {
      clearCartBtn.addEventListener('click', () => {
        cartItems = [];
        updateCart();
      });
    }

    // Proceed to checkout
    if (checkoutBtn) {
      checkoutBtn.addEventListener('click', () => {
        alert('Proceeding to checkout... (implement your checkout process)');
      });
    }

    // Initialize cart
    updateCart();
  }

  // ============================================================================
  // SEARCH AND FILTER FUNCTIONALITY
  // ============================================================================

  function initializeSearchAndFilters() {
    // Toggle Filter Panel
    const filterToggleBtn = document.getElementById('filter-toggle');
    const filterPanel = document.getElementById('filter-panel');
    if (filterToggleBtn && filterPanel) {
      filterToggleBtn.addEventListener('click', () => {
        filterPanel.classList.toggle('hidden');
      });
    }

    // Filter application
    document.getElementById('apply-filters')?.addEventListener('click', () => {
      const selectedPriceFilters = Array.from(document.querySelectorAll('.price-filter:checked')).map(cb => ({
        min: parseFloat(cb.dataset.min),
        max: parseFloat(cb.dataset.max),
      }));
      const selectedCategories = Array.from(document.querySelectorAll('.category-filter:checked')).map(cb => cb.dataset.category);
      const sortBy = document.getElementById('sort-select')?.value;

      console.log('Filters applied:', selectedPriceFilters, selectedCategories, sortBy);
      // Implement filtering logic based on your product data
    });

    document.getElementById('clear-filters')?.addEventListener('click', () => {
      document.querySelectorAll('.price-filter, .category-filter').forEach(cb => (cb.checked = false));
      document.getElementById('sort-select').value = 'featured';
    });

    // Search input
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
      searchInput.addEventListener('input', () => {
        const query = searchInput.value.toLowerCase();
        console.log('Searching for:', query);
        // Implement search filtering on your product list
      });
    }
  }

  // ============================================================================
  // FAQ FUNCTIONALITY
  // ============================================================================

  function initializeFAQ() {
    // FAQ Accordion
    document.querySelectorAll('.faq-question').forEach((btn) => {
      if (btn) {
        btn.addEventListener('click', () => {
          const answer = btn.nextElementSibling;
          answer.classList.toggle('hidden');
        });
      }
    });
  }

  // ============================================================================
  // COUNTDOWN TIMER FUNCTIONALITY
  // ============================================================================

  function initializeCountdown() {
    const countdownDays = document.getElementById('countdown-days');
    const countdownHours = document.getElementById('countdown-hours');
    const countdownMins = document.getElementById('countdown-mins');
    const countdownSecs = document.getElementById('countdown-secs');

    if (!countdownDays || !countdownHours || !countdownMins) return;

    // Set your deal end date here
    const dealEndDate = new Date('2024-12-31T23:59:59');

    function updateCountdown() {
      const now = new Date();
      const diff = dealEndDate - now;
      if (diff <= 0) {
        // Deal expired
        countdownDays.textContent = '00';
        countdownHours.textContent = '00';
        countdownMins.textContent = '00';
        countdownSecs.textContent = '00';
        clearInterval(countdownInterval);
        return;
      }
      const days = Math.floor(diff / (1000 * 60 * 60 * 24));
      const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
      const mins = Math.floor((diff / (1000 * 60)) % 60);
      const secs = Math.floor((diff / 1000) % 60);
      countdownDays.textContent = days.toString().padStart(2, '0');
      countdownHours.textContent = hours.toString().padStart(2, '0');
      countdownMins.textContent = mins.toString().padStart(2, '0');
      countdownSecs.textContent = secs.toString().padStart(2, '0');
    }

    const countdownInterval = setInterval(updateCountdown, 1000);
    updateCountdown();
  }

  // ============================================================================
  // BADGE UPDATE FUNCTIONALITY
  // ============================================================================

  function initializeBadgeUpdates() {
    const wishlistCount = document.getElementById('wishlist-count');
    const cartCount = document.getElementById('cart-count');
    const pendingCountBadge = document.getElementById('pending-count');

    let state = {
      wishlist: 3,
      cart: 1,
      pendingOrders: 0
    };

    const updateBadges = () => {
      if (wishlistCount) {
        wishlistCount.textContent = state.wishlist;
        wishlistCount.classList.toggle('hidden', state.wishlist === 0);
      }

      if (cartCount) {
        cartCount.textContent = state.cart;
      }

      if (pendingCountBadge) {
        pendingCountBadge.textContent = state.pendingOrders;
        pendingCountBadge.classList.toggle('hidden', state.pendingOrders === 0);
      }
    };

    // Make functions available globally
    window.BereanStoreBadges = {
      updateBadges,
      getState: () => state,
      setState: (newState) => {
        state = { ...state, ...newState };
        updateBadges();
      }
    };

    // Initialize badges
    updateBadges();
  }

  // ============================================================================
  // INITIALIZE ALL FUNCTIONALITY BASED ON PRESENT ELEMENTS
  // ============================================================================

  // Initialize core functionality
  initializeModalsAndSidebars();
  initializeWishlist();
  initializeCart();
  initializeSearchAndFilters();
  initializeFAQ();
  initializeCountdown();
  initializeBadgeUpdates();

  // ============================================================================
  // EXPOSE FUNCTIONS FOR COMPONENT-LEVEL INITIALIZATION
  // ============================================================================

  // Make functions available globally for component-specific initialization
  window.BereanStore = {
    initializeModalsAndSidebars,
    initializeWishlist,
    initializeCart,
    initializeSearchAndFilters,
    initializeFAQ,
    initializeCountdown,
    initializeBadgeUpdates,
    toggleVisibility
  };

  console.log('All Berean Store functionality initialized successfully');

});