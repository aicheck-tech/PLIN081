/**
 * PLIN081 Simple Localization System
 * Basic language switcher for testing
 */

class SimpleLocalization {
    constructor() {
        this.currentLanguage = localStorage.getItem('plin081-language') || 'cs';
        this.init();
    }

    init() {
        this.createLanguageSwitcher();
        this.applyLanguage(this.currentLanguage);
        this.bindEvents();
    }

    createLanguageSwitcher() {
        const switcher = document.createElement('div');
        switcher.id = 'language-switcher';
        switcher.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background: white;
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            font-family: Arial, sans-serif;
            font-size: 14px;
        `;

        switcher.innerHTML = `
            <label for="lang-select" style="margin-right: 8px;">Language:</label>
            <select id="lang-select" style="padding: 4px; border: 1px solid #ccc; border-radius: 3px;">
                <option value="cs" ${this.currentLanguage === 'cs' ? 'selected' : ''}>Čeština</option>
                <option value="en" ${this.currentLanguage === 'en' ? 'selected' : ''}>English</option>
            </select>
        `;

        document.body.appendChild(switcher);
    }

    bindEvents() {
        const select = document.getElementById('lang-select');
        select.addEventListener('change', (e) => {
            this.switchLanguage(e.target.value);
        });
    }

    switchLanguage(lang) {
        this.currentLanguage = lang;
        localStorage.setItem('plin081-language', lang);
        this.applyLanguage(lang);
    }

    applyLanguage(lang) {
        // Hide all language-specific elements
        const allLangElements = document.querySelectorAll('[data-lang]');
        allLangElements.forEach(el => {
            el.classList.add('hidden');
        });

        // Show elements for current language
        const currentLangElements = document.querySelectorAll(`[data-lang="${lang}"]`);
        currentLangElements.forEach(el => {
            el.classList.remove('hidden');
            
            // Update page title if available
            const title = el.getAttribute('data-title');
            if (title) {
                document.title = title;
            }
        });

        // Update document language attribute
        document.documentElement.lang = lang;
    }
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.localization = new SimpleLocalization();
});