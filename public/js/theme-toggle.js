(function () {
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');

    // Get current theme from localStorage or system preference
    function getCurrentTheme() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            return savedTheme;
        }
        return prefersDarkScheme.matches ? 'dark' : 'light';
    }

    // Apply theme to document
    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        updateToggleIcon(theme);
    }

    // Update toggle button icon
    function updateToggleIcon(theme) {
        const themeToggle = document.querySelector('.theme-toggle');
        if (!themeToggle) return;

        const icon = themeToggle.querySelector('.theme-icon');
        if (!icon) return;

        if (theme === 'dark') {
            icon.innerHTML = '☀️';
            themeToggle.setAttribute('aria-label', 'Switch to light mode');
        } else {
            icon.innerHTML = '🌙';
            themeToggle.setAttribute('aria-label', 'Switch to dark mode');
        }
    }

    // Toggle theme
    function toggleTheme() {
        const currentTheme = getCurrentTheme();
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        localStorage.setItem('theme', newTheme);
        applyTheme(newTheme);
    }

    // Initialize theme on page load
    function initTheme() {
        const currentTheme = getCurrentTheme();
        applyTheme(currentTheme);
    }

    // Listen for system theme changes
    prefersDarkScheme.addEventListener('change', function (e) {
        if (!localStorage.getItem('theme')) {
            applyTheme(e.matches ? 'dark' : 'light');
        }
    });

    // Initialize when DOM is ready
    function init() {
        initTheme();

        // Add event listener to toggle button
        const toggleButton = document.querySelector('.theme-toggle');
        if (toggleButton) {
            toggleButton.addEventListener('click', toggleTheme);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();