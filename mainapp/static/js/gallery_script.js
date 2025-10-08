// --- DATA MODEL ---
const ITEMS_PER_LOAD = 10;
let currentIndex = 0;

// Define all media items with type, URL, and a title for the hover effect
const allMediaItems = [
    // Custom Uploaded Files
    { type: 'video', url: 'kids-ministry.jpg', title: 'Ministry Highlight Reel' },
    { type: 'photo', url: 'image_1ae344.png', title: 'Summer Sunset Photo' },
    
    // Placeholders for variety
    { type: 'video', url: 'https://placehold.co/800x1200/F59E0B/000000?text=V-Clip+1', title: 'Epic Adventure Day' },
    { type: 'photo', url: 'https://placehold.co/800x1200/3B82F6/ffffff?text=P-Shot+2', title: 'City Nightscape' },
    { type: 'video', url: 'https://placehold.co/800x1200/10B981/000000?text=V-Clip+3', title: 'Green Screen Prank' },
    { type: 'photo', url: 'https://placehold.co/800x1200/8B5CF6/ffffff?text=P-Shot+4', title: 'Abstract Art Gallery' },
    { type: 'video', url: 'https://placehold.co/800x1200/EF4444/000000?text=V-Clip+5', title: 'Vintage Car Restoration' },
    { type: 'photo', url: 'https://placehold.co/800x1200/EC4899/000000?text=P-Shot+6', title: 'Pet Portrait Series' },
    { type: 'video', url: 'https://placehold.co/800x1200/FACC15/000000?text=V-Clip+7', title: 'Cooking Challenge Bloopers' },
    { type: 'photo', url: 'https://placehold.co/800x1200/525252/ffffff?text=P-Shot+8', title: 'Monochrome Forest' },
    { type: 'video', url: 'https://placehold.co/800x1200/06B6D4/000000?text=V-Clip+9', title: 'Drone Flyover' },
    { type: 'photo', url: 'https://placehold.co/800x1200/F43F5E/000000?text=P-Shot+10', title: 'Travel Diaries: Rome' },
    { type: 'video', url: 'https://placehold.co/800x1200/14B8A6/000000?text=V-Clip+11', title: 'Fitness Workout Guide' },
    { type: 'photo', url: 'https://placehold.co/800x1200/A855F7/ffffff?text=P-Shot+12', title: 'Minimalist Office Setup' },
    { type: 'video', url: 'https://placehold.co/800x1200/22C55E/000000?text=V-Clip+13', title: 'Unboxing Gadgets' },
    { type: 'photo', url: 'https://placehold.co/800x1200/FB923C/000000?text=P-Shot+14', title: 'Mountain Hiking View' },
    { type: 'video', url: 'https://placehold.co/800x1200/EF4444/000000?text=V-Clip+15', title: 'Gaming Stream Highlights' },
];


// --- UTILITY FUNCTIONS ---

// Function to shuffle array elements (Fisher-Yates algorithm)
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        // Swap array[i] and array[j]
        [array[i], array[j]] = [array[j], array[i]];
    }
}

// SVG for the Video Play Icon (Large, Center)
const videoIconSVG = `
    <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
        <svg class="w-12 h-12 text-white/90 drop-shadow-lg" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd"></path>
        </svg>
    </div>
`;

// SVG for the Photo Camera Icon (Small, Top Right)
const photoIconSVG = `
    <div class="absolute top-2 right-2 pointer-events-none p-1 bg-black/40 rounded-full">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect width="18" height="18" x="3" y="3" rx="2" ry="2"/>
            <circle cx="12" cy="12" r="3"/>
            <line x1="16.5" y1="7.5" x2="16.5" y2="7.5"/>
        </svg>
    </div>
`;


// --- RENDERING LOGIC ---

// This function is called by the 'Load More' button's onclick handler
function renderItems() {
    const gallery = document.getElementById('gallery-grid');
    const loadMoreBtn = document.getElementById('load-more-btn');

    if (!gallery || !loadMoreBtn) return;
    
    const start = currentIndex;
    const end = Math.min(currentIndex + ITEMS_PER_LOAD, allMediaItems.length);

    // Create a document fragment to minimize DOM reflows
    const fragment = document.createDocumentFragment();

    for (let i = start; i < end; i++) {
        const item = allMediaItems[i];
        
        // 1. Create the container
        const itemContainer = document.createElement('div');
        itemContainer.className = 'group relative rounded-xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:scale-[1.02] grid-item-container';
        itemContainer.setAttribute('data-type', item.type);

        // 2. Add the Image/Thumbnail
        const imageHtml = `<img src="${item.url}" alt="${item.title}" class="transition duration-500 group-hover:opacity-80">`;
        
        // 3. Add the type indicator (Video or Photo)
        const indicatorHtml = item.type === 'video' ? videoIconSVG : photoIconSVG;
        
        // 4. Add the Title Hover Overlay (Positioned at the TOP)
        const hoverOverlayHtml = `
            <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col items-center justify-start p-4">
                <p class="bg-black/70 px-3 py-1 rounded text-white text-sm font-semibold text-center leading-tight shadow-md">${item.title}</p>
            </div>
        `;

        // Combine and set inner HTML
        itemContainer.innerHTML = imageHtml + indicatorHtml + hoverOverlayHtml;

        // Append to fragment
        fragment.appendChild(itemContainer);
    }

    // Append all new items to the grid at once
    gallery.appendChild(fragment);

    // Update index
    currentIndex = end;

    // Check if all items are loaded and hide the button if necessary
    if (currentIndex >= allMediaItems.length) {
        loadMoreBtn.classList.add('hidden');
        console.log("All items loaded.");
    } else {
        // If more items exist, show how many are remaining
        const remaining = allMediaItems.length - currentIndex;
        loadMoreBtn.textContent = `Load More (${remaining} remaining)`;
    }
}

// Attach renderItems globally so the HTML button can call it
window.renderItems = renderItems;


// --- INITIALIZATION ---
// Run the shuffle and initial render once the page content has fully loaded
window.addEventListener('load', () => {
    // 1. Shuffle the complete list of items once
    shuffleArray(allMediaItems);

    // 2. Render the initial set of items (first 10)
    renderItems();
});
