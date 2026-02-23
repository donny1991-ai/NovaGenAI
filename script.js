/* ═══════════════════════════════════════════════════════
   NOVAGENAI — script.js
   ═══════════════════════════════════════════════════════ */

// ── Nav blur on scroll ───────────────────────────────
const nav = document.getElementById('nav');
let ticking = false;
window.addEventListener('scroll', () => {
    if (!ticking) {
        window.requestAnimationFrame(() => {
            nav.style.background = window.scrollY > 40 ? 'rgba(0,0,0,.85)' : 'rgba(0,0,0,.6)';
            ticking = false;
        });
        ticking = true;
    }
});

// ── Smooth anchor scroll ─────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
        const target = document.querySelector(anchor.getAttribute('href'));
        if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth' }); }
    });
});

// ── Scroll-triggered animations ──────────────────────
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.solutions, .testimonials, .contact, .footer, .fade-up').forEach(el => observer.observe(el));

// ── Testimonials Carousel ────────────────────────────
const testimonialsData = [
    { quote: "On-premise AI means our patient data never leaves our building. Non-negotiable in healthcare.", by: "Dr. Ahmad Razif, CTO, Healthcare Group", img: "images/testimonials/ahmad-razif.jpg" },
    { quote: "The Clarify platform gives us real-time intelligence we never had before. Game changer.", by: "Sarah Lim, Sales Director, CryoCord Group", img: "images/testimonials/sarah-lim.jpg" },
    { quote: "Multilingual AI support in English, Bahasa, and Mandarin — unlike anything in the market.", by: "Mei Ling Chen, Patient Relations Manager, CryoCord", img: "images/testimonials/mei-ling.jpg" },
    { quote: "Onboarding went from 3-month staff training to 2 weeks with their knowledge base AI.", by: "Priya Nair, HR Manager, Healthcare Org", img: "images/testimonials/priya-nair.jpg" },
    { quote: "Their predictive cell model is first-of-its-kind innovation in biotech AI.", by: "Dr. Tan Wei Ming, Lab Director, Medical Group", img: "images/testimonials/tan-wei-ming.jpg" },
    { quote: "ROI was visible within the first month. Enquiry-to-patient conversion doubled.", by: "James Wong, CIO, Private Hospital", img: "images/testimonials/james-wong.jpg" },
    { quote: "Finally, an AI company that understands Malaysian healthcare. Built compliance-first.", by: "Farah Ismail, COO, Biotech Firm", img: "images/testimonials/farah-ismail.jpg" },
    { quote: "The intersection of artificial intelligence and cell biology represents the next frontier. NovaGenAI is positioned at this exact convergence.", by: "Prof. Dr. Cheong Soon Keng, Academy of Sciences Malaysia", img: "images/testimonials/cheong-soon-keng.jpg" },
    { quote: "Their voice agent handles 80% of our enquiries autonomously. Our team focuses on what matters.", by: "Rachel Goh, Operations Manager, CryoCord Group", img: "images/testimonials/rachel-goh.jpg" },
    { quote: "The RAG system turned 10 years of SOPs into an instant knowledge base. Staff love it.", by: "Kumar Selvam, IT Director, Medical Centre", img: "images/testimonials/kumar-selvam.jpg" },
    { quote: "We deployed their DGX Spark solution in 3 weeks. Patient data sovereignty solved.", by: "Dr. Amir Hassan, CISO, Hospital Group", img: "images/testimonials/amir-hassan.jpg" },
    { quote: "Marketing compliance used to take weeks of legal review. Now it's built into the AI.", by: "Lisa Tan, Marketing Director, Healthcare Corp", img: "images/testimonials/lisa-tan.jpg" },
    { quote: "The predictive analytics on cell viability have improved our storage protocols dramatically.", by: "Dr. Nurul Ain, Research Scientist, CryoCord Labs", img: "images/testimonials/nurul-ain.jpg" },
    { quote: "Integration was seamless. Their team understands healthcare workflows inside out.", by: "David Chong, Head of Digital, Private Hospital", img: "images/testimonials/david-chong.jpg" },
    { quote: "We've cut our customer response time from 24 hours to under 2 minutes with the voice agent.", by: "Siti Aminah, Customer Service Lead, CryoCord", img: "images/testimonials/siti-aminah.jpg" },
    { quote: "The Clarify dashboard gives me visibility I've never had. Every lead, every touchpoint, tracked.", by: "Kevin Yap, Regional Sales Manager, CryoCord Group", img: "images/testimonials/kevin-yap.jpg" },
    { quote: "Their AI doesn't just automate — it augments our clinical decision-making.", by: "Dr. Liew Kah Meng, Chief Medical Officer", img: "images/testimonials/liew-kah-meng.jpg" },
    { quote: "Compliance-first AI is rare. NovaGenAI built it into their DNA, not as an afterthought.", by: "Tan Sri Dato' Razali, Board Advisor, Healthcare Group", img: "images/testimonials/razali.jpg" },
    { quote: "The HR automation alone saved us RM200K annually. Everything else is a bonus.", by: "Anita Kaur, CFO, CryoCord Group", img: "images/testimonials/anita-kaur.jpg" },
    { quote: "Best AI partner we've worked with. They understand both the tech and the science.", by: "Dr. Rajan Pillai, Director of Innovation, Biotech Ventures", img: "images/testimonials/rajan-pillai.jpg" },
];

const carousel = document.getElementById('testimonials-carousel');
const prevBtn = document.getElementById('testimonial-prev');
const nextBtn = document.getElementById('testimonial-next');

if (carousel) {
    let list = [...testimonialsData];
    let cardSize = window.matchMedia('(min-width: 640px)').matches ? 365 : 280;

    window.addEventListener('resize', () => {
        cardSize = window.matchMedia('(min-width: 640px)').matches ? 365 : 280;
        renderCards();
    });

    function getInitials(name) {
        const parts = name.replace(/^(Dr\.|Prof\.|Tan Sri|Dato')\s*/gi, '').split(' ');
        return (parts[0]?.[0] || '') + (parts[1]?.[0] || '');
    }

    function renderCards() {
        carousel.innerHTML = '';
        const half = Math.floor(list.length / 2);

        list.forEach((t, index) => {
            const position = index - half;
            const isCenter = position === 0;

            const card = document.createElement('div');
            card.className = 'testimonial-card' + (isCenter ? ' testimonial-card--center' : '');

            const offsetX = (cardSize / 1.5) * position;
            const offsetY = isCenter ? -65 : (position % 2 ? 15 : -15);
            const rotation = isCenter ? 0 : (position % 2 ? 2.5 : -2.5);

            card.style.transform = `translate(-50%, -50%) translateX(${offsetX}px) translateY(${offsetY}px) rotate(${rotation}deg)`;
            card.style.zIndex = isCenter ? 10 : (5 - Math.abs(position));
            card.style.width = cardSize + 'px';
            card.style.height = cardSize + 'px';

            const authorName = t.by.split(',')[0].trim();
            const initials = getInitials(authorName);

            card.innerHTML = `
                <img src="${t.img}" alt="${authorName}" class="testimonial-card__avatar">
                <h3 class="testimonial-card__quote">"${t.quote}"</h3>
                <p class="testimonial-card__author">— ${t.by}</p>
            `;

            card.addEventListener('click', () => move(position));
            carousel.appendChild(card);
        });
    }

    function move(steps) {
        if (steps === 0) return;
        if (steps > 0) {
            for (let i = 0; i < steps; i++) list.push(list.shift());
        } else {
            for (let i = 0; i < Math.abs(steps); i++) list.unshift(list.pop());
        }
        renderCards();
    }

    prevBtn?.addEventListener('click', () => move(-1));
    nextBtn?.addEventListener('click', () => move(1));
    renderCards();
}

// ── Org Diagram — position nodes in a circle ─────────
const orgDiagram = document.getElementById('org-diagram');
if (orgDiagram) {
    const nodes = orgDiagram.querySelectorAll('.org-node');
    const hub = document.getElementById('org-hub');
    const svgLines = document.getElementById('org-lines');

    function positionOrgNodes() {
        if (window.innerWidth < 768) return; // mobile uses flex column
        const w = orgDiagram.offsetWidth;
        const h = orgDiagram.offsetHeight;
        const cx = w / 2;
        const cy = h / 2;
        const radius = Math.min(cx, cy) - 80;

        svgLines.setAttribute('viewBox', `0 0 ${w} ${h}`);
        svgLines.innerHTML = '';

        nodes.forEach((node, i) => {
            const angle = (i / nodes.length) * Math.PI * 2 - Math.PI / 2;
            const nx = cx + radius * Math.cos(angle);
            const ny = cy + radius * Math.sin(angle);
            node.style.left = nx + 'px';
            node.style.top = ny + 'px';
            node.style.transform = 'translate(-50%, -50%)';

            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', cx);
            line.setAttribute('y1', cy);
            line.setAttribute('x2', nx);
            line.setAttribute('y2', ny);
            svgLines.appendChild(line);
        });
    }

    positionOrgNodes();
    window.addEventListener('resize', positionOrgNodes);

    // Click toggle for mobile
    nodes.forEach(node => {
        node.addEventListener('click', (e) => {
            const wasActive = node.classList.contains('active');
            nodes.forEach(n => n.classList.remove('active'));
            if (!wasActive) node.classList.add('active');
        });
    });
}

// ── Contact form handling ────────────────────────────
const contactForm = document.getElementById('contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const btn = contactForm.querySelector('.contact__submit');
        const origText = btn.textContent;
        btn.textContent = 'Sent! We\'ll be in touch.';
        btn.style.background = '#22C55E';
        setTimeout(() => {
            btn.textContent = origText;
            btn.style.background = '';
            contactForm.reset();
        }, 3000);
    });
}

/* ── Agents Page: Org Diagram Click Interaction ── */
document.querySelectorAll('.ag-org-node').forEach(node => {
    node.addEventListener('click', () => {
        const dept = node.dataset.dept;
        // Remove active from all nodes and details
        document.querySelectorAll('.ag-org-node').forEach(n => n.classList.remove('active'));
        document.querySelectorAll('.ag-dept-detail').forEach(d => d.classList.remove('active'));
        // Activate clicked
        node.classList.add('active');
        const detail = document.querySelector(`.ag-dept-detail[data-dept="${dept}"]`);
        if (detail) detail.classList.add('active');
    });
});

// Auto-show first department
const firstNode = document.querySelector('.ag-org-node');
if (firstNode) firstNode.click();

// Remove Spline watermark
setInterval(()=>{
  const sv=document.querySelector('spline-viewer');
  if(!sv||!sv.shadowRoot)return;
  const logo=sv.shadowRoot.querySelector('#logo');
  if(logo)logo.remove();
  sv.shadowRoot.querySelectorAll('a').forEach(a=>{
    if(a.href&&a.href.includes('spline'))a.remove();
  });
},500);
