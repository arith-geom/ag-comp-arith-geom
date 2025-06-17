/*******************************************************************************
 * Multi-Theme Switcher
 * Allows switching between 5 different design themes
 * DISABLED - Using floating theme switcher instead
 ******************************************************************************/

(function() {
    // Define available themes
    const themes = {
        'default': {
            name: 'Modern AG (Default)',
            file: '/assets/css/modern-ag.css',
            description: 'Enhanced Heidelberg University theme'
        },
        'classic': {
            name: 'Classic Academic',
            file: '/assets/css/theme-1-classic.css',
            description: 'Traditional university style'
        },
        'modern': {
            name: 'Modern Minimalist',
            file: '/assets/css/theme-2-modern.css',
            description: 'Sleek contemporary design'
        },
        'dark': {
            name: 'Dark Professional',
            file: '/assets/css/theme-3-dark.css',
            description: 'Cyberpunk dark theme'
        },
        'pastel': {
            name: 'Pastel Soft',
            file: '/assets/css/theme-4-pastel.css',
            description: 'Warm and friendly colors'
        },
        'minimal': {
            name: 'Ultra Minimal',
            file: '/assets/css/theme-5-minimal.css',
            description: 'Bauhaus-inspired clean'
        }
    };

    let currentTheme = localStorage.getItem('selected-theme') || 'default';
    let themeStylesheet = null;

    // Initialize theme switcher - DISABLED
    function initThemeSwitcher() {
        // DISABLED - using floating theme switcher instead
        return;
        
        createThemeSwitcherUI();
        loadTheme(currentTheme);
    }

    // Create the theme switcher UI - DISABLED
    function createThemeSwitcherUI() {
        // DISABLED - using floating theme switcher instead
        return;
    }

    // Load theme function (keep for compatibility)
    function loadTheme(themeKey) {
        if (!themes[themeKey]) return;

        const theme = themes[themeKey];
        currentTheme = themeKey;

        // Remove existing theme stylesheet
        if (themeStylesheet) {
            themeStylesheet.remove();
            themeStylesheet = null;
        }

        // Load new theme stylesheet (if not default)
        if (themeKey !== 'default' && theme.file) {
            themeStylesheet = document.createElement('link');
            themeStylesheet.rel = 'stylesheet';
            themeStylesheet.href = theme.file;
            themeStylesheet.id = 'theme-stylesheet';
            document.head.appendChild(themeStylesheet);
        }

        // Store theme preference
        localStorage.setItem('selected-theme', themeKey);

        // Update body class
        document.body.className = document.body.className.replace(/theme-\w+/g, '');
        if (themeKey !== 'default') {
            document.body.classList.add(`theme-${themeKey}`);
        }

        // Show notification
        showThemeNotification(theme.name);

        // Update theme switcher UI if exists
        updateThemeSwitcherUI();
    }

    // Show theme change notification
    function showThemeNotification(themeName) {
        // Create notification
        const notification = document.createElement('div');
        notification.className = 'theme-notification';
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">🎨</span>
                <span class="notification-text">Theme changed to: ${themeName}</span>
            </div>
        `;

        // Add styles
        const style = document.createElement('style');
        style.textContent = `
            .theme-notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background: rgba(0, 0, 0, 0.9);
                color: white;
                padding: 15px 20px;
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
                z-index: 10001;
                opacity: 0;
                transform: translateY(-20px);
                transition: all 0.3s ease;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }

            .theme-notification.show {
                opacity: 1;
                transform: translateY(0);
            }

            .notification-content {
                display: flex;
                align-items: center;
                gap: 10px;
            }

            .notification-icon {
                font-size: 18px;
            }

            .notification-text {
                font-size: 14px;
                font-weight: 500;
            }
        `;

        document.head.appendChild(style);
        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => notification.classList.add('show'), 100);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                document.body.removeChild(notification);
                document.head.removeChild(style);
            }, 300);
        }, 3000);
    }

    // Update theme switcher UI
    function updateThemeSwitcherUI() {
        // DISABLED - using floating theme switcher instead
        return;
    }

    // Toggle theme switcher visibility - DISABLED
    window.toggleThemeSwitcher = function() {
        // DISABLED - using floating theme switcher instead
        return;
    };

    // Switch theme function (keep for compatibility)
    window.switchTheme = function(themeKey) {
        loadTheme(themeKey);
    };

    // DISABLED - Don't initialize the old theme switcher
    // document.addEventListener('DOMContentLoaded', initThemeSwitcher);

    console.log('Theme switcher multi disabled - using floating switcher instead');
})(); 