// mainapp/static/js/tailwind_config.js

tailwind.config = {
    theme: {
        extend: {
            colors: {
                // Your custom color definitions
                'berean-blue': '#2A6F97',
                'berean-red': '#CC0000',
                'berean-lightblue': '#8CD0D2',
                'berean-skyblue': '#E0F2F7',
                // Default Tailwind colors for 'primary', 'background', 'muted', 'muted-foreground'
                primary: '#2A6F97',
                background: '#FFFFFF',
                muted: '#F1F5F9',
                'muted-foreground': '#64748B',
                'primary-foreground': '#FFFFFF',
                card: '#FFFFFF',
                'card-foreground': '#0F172A',
            },
            fontFamily: {
                // Your custom font definitions
                inter: ['Inter', 'sans-serif'],
                montserrat: ['Montserrat', 'sans-serif'],
            },
        }
    }
}