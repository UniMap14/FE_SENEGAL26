// Navigation fluide du site FE_SENEGAL.
//
// 1) Filtres, recherche et pagination : les zones marquées data-live-region sont
//    rechargées sur place (sans remonter en haut de la page ni recharger le bandeau).
//    Sans JavaScript, les liens fonctionnent quand même (ancre #liste).
// 2) Navigation à l'intérieur d'une même section (ex. /emod/ -> /emod/guide/, retour à
//    la liste) : la page suivante s'ouvre directement sur le contenu, sans repasser par
//    le grand bandeau photo.
(function () {
    'use strict';

    var SKIP_KEY = 'fe_skip_hero';

    function headerHeight() {
        var h = document.querySelector('.site-header');
        return h ? h.offsetHeight : 0;
    }
    function firstSegment(pathname) {
        return pathname.split('/').filter(Boolean)[0] || '';
    }
    function isModifiedClick(e) {
        return e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey;
    }
    function scrollToEl(el, smooth) {
        var top = el.getBoundingClientRect().top + window.pageYOffset - headerHeight() - 12;
        window.scrollTo({ top: Math.max(top, 0), behavior: smooth ? 'smooth' : 'auto' });
    }

    /* ---------- 2) Arrivée directement sur le contenu ---------- */
    (function skipHeroOnArrival() {
        var flagged = false;
        try { flagged = sessionStorage.getItem(SKIP_KEY) === '1'; sessionStorage.removeItem(SKIP_KEY); } catch (e) {}
        if (!flagged || location.hash) return;
        var nav = (performance.getEntriesByType && performance.getEntriesByType('navigation')[0]) || {};
        if (nav.type === 'back_forward' || nav.type === 'reload') return;
        var hero = document.querySelector('.page-hero');
        var target = hero && hero.nextElementSibling;
        if (!target) return;
        if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
        scrollToEl(target, false);
    })();

    document.addEventListener('click', function (e) {
        if (isModifiedClick(e)) return;
        var a = e.target.closest && e.target.closest('a[href]');
        if (!a || a.target === '_blank' || a.hasAttribute('download')) return;
        if (a.origin !== location.origin) return;

        // Lien dans une zone "live" vers la même page (autre filtre / autre page de résultats)
        var region = a.closest('[data-live-region]');
        var samePage = a.pathname === location.pathname;
        if (region && samePage && (!a.hash || a.hash === '#' + region.id)) {
            e.preventDefault();
            var url = a.pathname + a.search;
            load(url, true, !!a.closest('.pagination'));
            return;
        }

        // Navigation dans la même section : on ouvre la page suivante au niveau du contenu
        if (a.closest('main') && !a.hash && firstSegment(a.pathname) === firstSegment(location.pathname)
                && firstSegment(location.pathname) !== '') {
            try { sessionStorage.setItem(SKIP_KEY, '1'); } catch (err) {}
        }
    });

    /* ---------- 1) Rechargement sur place des filtres / recherches ---------- */
    var controller = null;

    function currentRegion() { return document.querySelector('[data-live-region]'); }

    function load(url, push, scrollToTop) {
        var region = currentRegion();
        if (!region || !window.fetch || !window.DOMParser) { location.href = url; return; }
        if (controller && controller.abort) controller.abort();
        controller = window.AbortController ? new AbortController() : null;
        region.classList.add('is-loading');
        region.setAttribute('aria-busy', 'true');

        fetch(url, { credentials: 'same-origin', signal: controller ? controller.signal : undefined,
                     headers: { 'X-Requested-With': 'fetch' } })
            .then(function (r) { if (!r.ok) throw new Error('http ' + r.status); return r.text(); })
            .then(function (html) {
                var doc = new DOMParser().parseFromString(html, 'text/html');
                var fresh = doc.querySelector('[data-live-region]');
                if (!fresh) throw new Error('no region');
                region.innerHTML = fresh.innerHTML;
                // Le texte d'introduction du bandeau peut dépendre du filtre (ex. nombre de photos)
                var heroNow = document.querySelector('.page-hero-inner');
                var heroNew = doc.querySelector('.page-hero-inner');
                if (heroNow && heroNew) heroNow.innerHTML = heroNew.innerHTML;
                document.title = doc.title;
                if (push) history.pushState({ live: true }, '', url);
                region.classList.remove('is-loading');
                region.removeAttribute('aria-busy');
                if (scrollToTop) scrollToEl(region, true);
            })
            .catch(function (err) {
                if (err && err.name === 'AbortError') return;
                location.href = url; // repli : navigation classique
            });
    }

    // Recherche (formulaires GET) dans une zone live
    document.addEventListener('submit', function (e) {
        var form = e.target;
        var region = form.closest && form.closest('[data-live-region]');
        if (!region || (form.method || 'get').toLowerCase() !== 'get') return;
        e.preventDefault();
        var params = new URLSearchParams();
        new FormData(form).forEach(function (v, k) { if (String(v).trim() !== '') params.append(k, v); });
        var qs = params.toString();
        load(location.pathname + (qs ? '?' + qs : ''), true, false);
    });

    // Boutons précédent / suivant du navigateur
    if (currentRegion()) {
        try { history.replaceState({ live: true }, '', location.href); } catch (e) {}
        window.addEventListener('popstate', function () {
            if (currentRegion()) load(location.pathname + location.search, false, false);
        });
    }
})();
