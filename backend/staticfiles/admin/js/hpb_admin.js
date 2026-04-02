/* HPB Admin JS — amélioration UX éditeur d'articles */
(function() {
  'use strict';

  document.addEventListener('DOMContentLoaded', function() {

    /* ── Compteur de mots dans l'éditeur ──────────────────── */
    function updateWordCount(editorEl) {
      const text = editorEl.innerText || '';
      const words = text.trim().split(/\s+/).filter(w => w.length > 0).length;
      const chars = text.replace(/\s/g, '').length;
      const readMin = Math.max(1, Math.round(words / 200));

      let counter = document.getElementById('hpb-word-count');
      if (!counter) {
        counter = document.createElement('div');
        counter.id = 'hpb-word-count';
        counter.style.cssText = [
          'display:flex', 'gap:16px', 'padding:8px 14px',
          'background:rgba(245,197,24,.06)', 'border-top:1px solid rgba(245,197,24,.12)',
          'font-size:11px', 'color:#8b9ab5', 'font-family:monospace',
        ].join(';');
        const ckEditor = editorEl.closest('.ck-editor') || editorEl.parentElement;
        ckEditor.appendChild(counter);
      }
      counter.innerHTML = [
        `<span>📝 <strong style="color:#f5c518">${words}</strong> mots</span>`,
        `<span>🔤 <strong style="color:#60a5fa">${chars}</strong> caractères</span>`,
        `<span>⏱ Lecture : <strong style="color:#34d399">~${readMin} min</strong></span>`,
      ].join('');

      /* Mettre à jour le champ read_time */
      const rtField = document.getElementById('id_read_time');
      if (rtField && !rtField._userEdited) rtField.value = readMin;
    }

    /* ── Attendre que CKEditor soit initialisé ────────────── */
    const waitForCK = setInterval(function() {
      const editables = document.querySelectorAll('.ck-editor__editable_inline');
      if (editables.length === 0) return;
      clearInterval(waitForCK);

      editables.forEach(function(el) {
        /* Compteur initial */
        updateWordCount(el);
        /* Observer les changements */
        const observer = new MutationObserver(function() { updateWordCount(el); });
        observer.observe(el, { childList: true, subtree: true, characterData: true });
      });

      /* Marquer read_time comme édité manuellement si l'user le touche */
      const rtField = document.getElementById('id_read_time');
      if (rtField) rtField.addEventListener('input', function() { this._userEdited = true; });

    }, 500);

    /* ── Indicateur de sauvegarde ─────────────────────────── */
    const form = document.querySelector('form#article_form, form[id$="_form"]');
    if (form) {
      let dirty = false;
      form.addEventListener('input', function() {
        if (!dirty) {
          dirty = true;
          const save = document.querySelector('.submit-row');
          if (save) {
            const dot = document.createElement('span');
            dot.id = 'hpb-unsaved';
            dot.textContent = '● Modifications non sauvegardées';
            dot.style.cssText = 'color:#f5c518;font-size:11px;font-weight:700;margin-left:auto;';
            save.appendChild(dot);
          }
        }
      });
      form.addEventListener('submit', function() {
        const dot = document.getElementById('hpb-unsaved');
        if (dot) dot.remove();
      });
    }

    /* ── Raccourci clavier Ctrl+S pour sauvegarder ────────── */
    document.addEventListener('keydown', function(e) {
      if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        const saveBtn = document.querySelector('input[name="_continue"], .submit-row input[type="submit"]:first-of-type');
        if (saveBtn) saveBtn.click();
      }
    });

    /* ── Aperçu de la couleur de catégorie ────────────────── */
    const catField = document.getElementById('id_category');
    if (catField) {
      const COLORS = {
        'DevOps': '#f5c518', 'Cloud': '#60a5fa', 'GIS': '#34d399',
        'Backend': '#a5b4fc', 'Linux': '#f87171', 'AI': '#fb923c',
      };
      function updateCatBadge() {
        const val = catField.value;
        const color = COLORS[val] || '#8b9ab5';
        let badge = document.getElementById('hpb-cat-badge');
        if (!badge) {
          badge = document.createElement('span');
          badge.id = 'hpb-cat-badge';
          badge.style.cssText = 'margin-left:10px;padding:3px 12px;border-radius:12px;font-size:11px;font-weight:700;';
          catField.parentNode.insertBefore(badge, catField.nextSibling);
        }
        badge.textContent = val || '—';
        badge.style.background = color + '22';
        badge.style.border = `1px solid ${color}55`;
        badge.style.color = color;
      }
      updateCatBadge();
      catField.addEventListener('change', updateCatBadge);
      catField.addEventListener('input',  updateCatBadge);
    }
  });
})();
