/* ═══════════════════════════════════════════════════════
   NOVAGENAI BLOG — INTERACTIONS
   ═══════════════════════════════════════════════════════ */

(function () {
    'use strict';

    /* ── READING PROGRESS BAR ──────────────────────── */
    const progressBar = document.querySelector('.blog-progress');
    if (progressBar) {
        const updateProgress = () => {
            const scrollTop = window.scrollY;
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
            progressBar.style.width = Math.min(progress, 100) + '%';
        };
        window.addEventListener('scroll', updateProgress, { passive: true });
        updateProgress();
    }

    /* ── FAQ ACCORDION ─────────────────────────────── */
    document.querySelectorAll('.faq-item__question').forEach(btn => {
        btn.addEventListener('click', () => {
            const item = btn.closest('.faq-item');
            const answer = item.querySelector('.faq-item__answer');
            const isOpen = item.classList.contains('open');

            // Close all others
            document.querySelectorAll('.faq-item.open').forEach(openItem => {
                if (openItem !== item) {
                    openItem.classList.remove('open');
                    openItem.querySelector('.faq-item__answer').style.maxHeight = '0';
                }
            });

            if (isOpen) {
                item.classList.remove('open');
                answer.style.maxHeight = '0';
            } else {
                item.classList.add('open');
                answer.style.maxHeight = answer.scrollHeight + 'px';
            }
        });
    });

    /* ── CATEGORY FILTER ───────────────────────────── */
    const pills = document.querySelectorAll('.blog-filter-pill');
    const cards = document.querySelectorAll('.blog-card');
    const featured = document.querySelector('.blog-featured');

    pills.forEach(pill => {
        pill.addEventListener('click', () => {
            pills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');

            const cat = pill.dataset.category;

            cards.forEach(card => {
                if (cat === 'all' || card.dataset.category === cat) {
                    card.style.display = '';
                    requestAnimationFrame(() => card.classList.add('visible'));
                } else {
                    card.classList.remove('visible');
                    card.style.display = 'none';
                }
            });

            if (featured) {
                if (cat === 'all' || featured.dataset.category === cat) {
                    featured.style.display = '';
                } else {
                    featured.style.display = 'none';
                }
            }
        });
    });

    /* ── SCROLL ANIMATIONS (IntersectionObserver) ──── */
    const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -40px 0px' };
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.blog-card, .fade-in-up').forEach(el => {
        observer.observe(el);
    });

    /* ── SOCIAL SHARE BUTTONS ──────────────────────── */
    document.querySelectorAll('[data-share]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const type = btn.dataset.share;
            const url = encodeURIComponent(window.location.href);
            const title = encodeURIComponent(document.title);

            const urls = {
                linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${url}`,
                x: `https://x.com/intent/tweet?url=${url}&text=${title}`,
                copy: null
            };

            if (type === 'copy') {
                navigator.clipboard.writeText(window.location.href).then(() => {
                    btn.classList.add('copied');
                    const orig = btn.innerHTML;
                    setTimeout(() => btn.classList.remove('copied'), 2000);
                });
                return;
            }

            if (urls[type]) {
                window.open(urls[type], '_blank', 'width=600,height=500');
            }
        });
    });

    /* ── LOAD MORE ─────────────────────────────────── */
    const loadMoreBtn = document.querySelector('.blog-load-more__btn');
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', () => {
            // Placeholder: In production, fetch next page via API
            // For now, show hidden cards
            const hidden = document.querySelectorAll('.blog-card[hidden]');
            hidden.forEach((card, i) => {
                if (i < 4) {
                    card.removeAttribute('hidden');
                    card.style.display = '';
                    observer.observe(card);
                }
            });
            if (document.querySelectorAll('.blog-card[hidden]').length === 0) {
                loadMoreBtn.style.display = 'none';
            }
        });
    }

})();
