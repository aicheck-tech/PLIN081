 (function() {
      var langs = { cs: 'Čeština', en: 'English' };
      var current = localStorage.getItem('plin081-language') || 'cs';

      // All in DOMContentLoaded to guarantee DOM elements exist
      document.addEventListener('DOMContentLoaded', function() {
          // 1. Prefill
          var src = document.querySelector('textarea[data-lang="' + current + '"]');
          var mainMd = document.getElementById('main-md');
          mainMd.innerHTML = src.value.trim();
          if (src && mainMd) mainMd.value = src.value.trim();
          document.querySelectorAll('textarea[data-lang]:not([data-template])').forEach(el => el.remove());

          // 2. Reveal.js initialize
          Reveal.initialize({
              hash: true,
              plugins: [ RevealMarkdown ]
          });

          // 3. Language switcher
          function setLang(lang) {
              localStorage.setItem('plin081-language', lang);
              window.location.reload();
          }

          var div = document.createElement('div');
          div.id = 'language-switcher';
          div.style.cssText = `
              position: fixed; top: 20px; right: 20px; z-index: 1000;
              background: white; border: 1px solid #ccc; border-radius: 4px;
              padding: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
              font-family: Arial, sans-serif; font-size: 14px;
          `;
          var sel = document.createElement('select');
          Object.entries(langs).forEach(([code, name]) => {
              var opt = document.createElement('option');
              opt.value = code;
              opt.textContent = name;
              if (code === current) opt.selected = true;
              sel.appendChild(opt);
          });
          sel.onchange = function() { setLang(sel.value); };
          div.innerHTML = '<label for="lang-select" style="margin-right: 8px;">Language:</label>';
          div.appendChild(sel);
          document.body.appendChild(div);
      });
  })();