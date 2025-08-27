/**
 * PLIN081 Localization System
 * JavaScript-based language switcher for Czech/English content in Reveal.js presentations
 */

class RevealLocalization {
    constructor() {
        this.currentLanguage = localStorage.getItem('plin081-language') || 'cs';
        this.textareas = null;
        this.languageContent = {};
        this.languageTitles = {};
        this.init();
    }

    init() {
        // Wait for both DOM and Reveal.js to be ready
        this.waitForReady(() => {
            this.setupLocalization();
        });
    }

    waitForReady(callback) {
        const checkReady = () => {
            if (document.readyState === 'complete' && window.Reveal && window.Reveal.isReady()) {
                callback();
            } else {
                setTimeout(checkReady, 100);
            }
        };
        checkReady();
    }

    setupLocalization() {
        this.collectLanguageContent();
        this.createLanguageSwitcher();
        this.applyLanguage(this.currentLanguage);
        this.bindEvents();
    }

    collectLanguageContent() {
        // Find all textarea elements with language data
        this.textareas = document.querySelectorAll('textarea[data-template][data-lang]');
        
        this.textareas.forEach(textarea => {
            const lang = textarea.getAttribute('data-lang');
            const title = textarea.getAttribute('data-title');
            
            // Store content for language switching
            this.languageContent[lang] = textarea.innerHTML.trim();
            
            if (title) {
                this.languageTitles[lang] = title;
            }
        });
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
        if (select) {
            select.addEventListener('change', (e) => {
                this.switchLanguage(e.target.value);
            });
        }
    }

    switchLanguage(lang) {
        this.currentLanguage = lang;
        localStorage.setItem('plin081-language', lang);
        this.applyLanguage(lang);
    }

    applyLanguage(lang) {
        // Update document language attribute
        document.documentElement.lang = lang;

        // Update page title if available
        if (this.languageTitles[lang]) {
            document.title = this.languageTitles[lang];
        }

        // Update the active textarea content
        if (this.languageContent[lang] && this.textareas.length > 0) {
            // Find the first textarea (assuming single section pages)
            const activeTextarea = this.textareas[0];
            if (activeTextarea) {
                activeTextarea.innerHTML = this.languageContent[lang];
                
                // Re-process the markdown with Reveal.js
                this.refreshRevealContent();
            }
        }
    }

    refreshRevealContent() {
        if (window.Reveal) {
            // Force Reveal.js to re-process the markdown
            const plugin = window.Reveal.getPlugin('markdown');
            if (plugin && plugin.processSlides) {
                const sections = document.querySelectorAll('section[data-markdown]');
                sections.forEach(section => {
                    plugin.processSlides(section);
                });
            }
            
            // Sync the presentation
            window.Reveal.sync();
        }
    }
}

// Initialize the localization system
document.addEventListener('DOMContentLoaded', () => {
    // Use a timeout to ensure Reveal.js has time to initialize
    setTimeout(() => {
        window.revealLocalization = new RevealLocalization();
    }, 1000);
});