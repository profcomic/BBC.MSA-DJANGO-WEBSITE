document.addEventListener('DOMContentLoaded', function() {

    // ==========================================================
    // 1. CAROUSEL SCRIPT (Weekly Services)
    // ==========================================================
    const carousel = document.getElementById('service-carousel');
    const cards = document.querySelectorAll('.service-card');

    const transitionDurationMs = 500; 
    const readingPauseMs = 2500; 
    const slideInterval = transitionDurationMs + readingPauseMs;

    if (carousel && cards.length > 0) {
        carousel.style.transition = `transform ${transitionDurationMs / 1000}s ease-in-out`;

        function autoSlide() {
            const firstCard = carousel.firstElementChild;
            const cardWidth = firstCard.offsetWidth;

            carousel.style.transform = `translateX(-${cardWidth}px)`;

            setTimeout(() => {
                carousel.style.transition = 'none';
                carousel.appendChild(firstCard);
                carousel.style.transform = 'translateX(0)';
                
                requestAnimationFrame(() => {
                    requestAnimationFrame(() => {
                        carousel.style.transition = `transform ${transitionDurationMs / 1000}s ease-in-out`;
                    });
                });
            }, transitionDurationMs);
        }
        setInterval(autoSlide, slideInterval);
    }


    // ==========================================================
    // 2. MINISTRY CUBE FLIP SCRIPT
    // ==========================================================
    const dataElement = document.getElementById('ministry-data');
    if (dataElement) {
        const ministryData = JSON.parse(dataElement.textContent);
        
        const cols = [
            { id: 1, wrapper: document.getElementById('wrapper-1'), data: ministryData.col1, currentIndex: 0, direction: 'clockwise' }, 
            { id: 2, wrapper: document.getElementById('wrapper-2'), data: ministryData.col2, currentIndex: 0, direction: 'anticlockwise' }
        ];

        const flipInterval = 4000;
        const cubeFlipTime = 500; 
        const halfFlipTime = cubeFlipTime / 2;

        function renderCard(column, ministry) {
            return `
                <div class="ministry-content p-6 bg-white shadow-lg rounded-xl flex flex-col items-center justify-center h-64 border-t-4 border-sky-500">
                    <img src="${ministry.image}" alt="${ministry.title}" class="mb-4 w-16 h-16 object-contain rounded-full border-2 border-sky-200 p-1">
                    <h3 class="text-xl font-bold text-sky-900 mb-2">${ministry.title}</h3>
                    <p class="text-gray-600 text-center text-sm">${ministry.description}</p>
                </div>
            `;
        }

        function flipAndSwap(column) {
            const { wrapper, data, direction } = column;
            if (data.length === 0) return;
            
            const flipClass = (direction === 'clockwise') ? 'flipped-cube-clockwise' : 'flipped-cube-anticlockwise';
            
            wrapper.classList.add(flipClass);

            setTimeout(() => {
                const nextIndex = (column.currentIndex + 1) % data.length;
                const nextMinistry = data[nextIndex];

                wrapper.innerHTML = renderCard(column, nextMinistry);
                column.currentIndex = nextIndex; 
                
                setTimeout(() => {
                    wrapper.classList.remove(flipClass);
                }, halfFlipTime); 

            }, halfFlipTime);
        }

        function startFlipping() {
            cols.forEach(flipAndSwap);
            setTimeout(startFlipping, flipInterval);
        }

        setTimeout(startFlipping, flipInterval); 
    }


    // ==========================================================
    // 3. COUNTDOWN SCRIPT (Event Timer)
    // ==========================================================
   
    // Target date: November 15, 2025 at 10:00 PM (22:00:00) EAT is +03:00 from UTC.
    // Since we don't know the local time zone of the server/user, specifying the full date
    // with time is best, and JS handles the calculation relative to the user's clock.
    function pad(num) {
        return num < 10 ? '0' + num : num;
    }
    
    function startCountdown(targetDate, elementId) {
        const countDownDate = new Date(targetDate).getTime();
        const countdownElement = document.getElementById(elementId);
  
        if (!countdownElement) return;

        const x = setInterval(function() {
           const now = new Date().getTime();
           const distance = countDownDate - now;

           const container = document.getElementById("youth-countdown-timer");

        // Check if the event has passed or is live
         // Calculations
            // ... inside the setInterval function ...
            if (distance > 0) {
                const days = Math.floor(distance / (1000 * 60 * 60 * 24));
                const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((distance % (1000 * 60)) / 1000);   
 
                if (document.getElementById("youth-countdown-days")) document.getElementById("youth-countdown-days").innerHTML = pad(days);
                if (document.getElementById("youth-countdown-hours")) document.getElementById("youth-countdown-hours").innerHTML = pad(hours);
                if (document.getElementById("youth-countdown-minutes")) document.getElementById("youth-countdown-minutes").innerHTML = pad(minutes);
                if (document.getElementById("youth-countdown-seconds")) document.getElementById("youth-countdown-seconds").innerHTML = pad(seconds); 

                // NOTE: If you are using the 'youth-countdown-timer' element
                // for the circle *container*, you should remove this line 
                // as it will overwrite the circles' HTML structure:
                // countdownElement.innerHTML = days + "Days " + hours + "Hours " + minutes + "Minutes " + seconds + "Seconds";
            
            } else {
                // ... The rest of the 'else' block (clear interval, display "LIVE NOW")
                clearInterval(x);
                countdownElement.innerHTML = '<p class="text-4xl font-bold text-red-00">EVENT IS LIVE NOW!</p>';
                countdownElement.classList.add('text-red-400');
            }
        }, 1000);
    }

    // Initialize the countdown here, inside DOMContentLoaded
    // Ensure this date is in the future relative to the current time: 2025-10-03 10:07:16 PM EAT
    startCountdown("2025-11-15T19:00:00Z", "youth-countdown-timer");
    // If you think the problem might be the date format, try a simple, very near date:
    
});

 
        