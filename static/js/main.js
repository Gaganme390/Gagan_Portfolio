/* =====================================================
   MAIN.JS — Core functionality
   ===================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    initScrollProgressBar();
    initScrollAnimations();
    init3DTiltCards();
    initTypingEffect();
    initCounterAnimations();
    initTimelineCards();
    initSkillBars();
    initContactForm();
    initSmoothScroll();
    initActiveNavHighlight();
});

/* ── Floating Dock & Dynamic Magnetic Pill Navbar ── */
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');
    const navWrapper = document.querySelector('.nav-links-wrapper');
    const activePill = document.getElementById('nav-active-pill');
    const links = document.querySelectorAll('.nav-links a');

    if (!navbar) return;

    // Scroll shrink effect
    window.addEventListener('scroll', () => {
        if (window.scrollY > 40) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }, { passive: true });

    // Mobile menu toggle
    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            navToggle.classList.toggle('active');
            navLinks.classList.toggle('open');
        });

        links.forEach(link => {
            link.addEventListener('click', () => {
                navToggle.classList.remove('active');
                navLinks.classList.remove('open');
            });
        });
    }

    // Magnetic sliding active indicator pill
    if (activePill && navWrapper && links.length > 0) {
        function movePillTo(element) {
            if (!element || window.innerWidth <= 768) {
                activePill.classList.remove('active');
                return;
            }
            const wrapperRect = navWrapper.getBoundingClientRect();
            const rect = element.getBoundingClientRect();

            const left = rect.left - wrapperRect.left;
            const width = rect.width;
            const top = rect.top - wrapperRect.top;
            const height = rect.height;

            activePill.style.transform = `translate3d(${left}px, ${top}px, 0)`;
            activePill.style.width = `${width}px`;
            activePill.style.height = `${height}px`;
            activePill.classList.add('active');
        }

        // Move to hovered item or active item
        links.forEach(link => {
            link.addEventListener('mouseenter', () => movePillTo(link));
        });

        navWrapper.addEventListener('mouseleave', () => {
            const activeLink = document.querySelector('.nav-links a.active');
            if (activeLink) {
                movePillTo(activeLink);
            } else {
                activePill.classList.remove('active');
            }
        });

        window.addEventListener('resize', () => {
            const activeLink = document.querySelector('.nav-links a.active');
            if (activeLink) movePillTo(activeLink);
        });
    }
}

/* ── Scroll animations with IntersectionObserver ── */
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll(
        '.fade-in, .fade-in-left, .fade-in-right, .scale-in, .stagger-children'
    );

    if (!animatedElements.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Don't unobserve stagger-children so they can re-animate if needed
                if (!entry.target.classList.contains('stagger-children')) {
                    observer.unobserve(entry.target);
                }
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    animatedElements.forEach(el => observer.observe(el));
}

/* ── Typing effect for hero ── */
function initTypingEffect() {
    const typingElement = document.getElementById('typing-text');
    if (!typingElement) return;

    const texts = typingElement.dataset.texts ? typingElement.dataset.texts.split(',') : [];
    if (!texts.length) return;

    let textIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let typingSpeed = 80;

    function type() {
        const currentText = texts[textIndex].trim();

        if (isDeleting) {
            typingElement.textContent = currentText.substring(0, charIndex - 1);
            charIndex--;
            typingSpeed = 40;
        } else {
            typingElement.textContent = currentText.substring(0, charIndex + 1);
            charIndex++;
            typingSpeed = 80;
        }

        if (!isDeleting && charIndex === currentText.length) {
            typingSpeed = 2000; // Pause at end
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            textIndex = (textIndex + 1) % texts.length;
            typingSpeed = 500; // Pause before next word
        }

        setTimeout(type, typingSpeed);
    }

    setTimeout(type, 1000);
}

/* ── Counter animations ── */
function initCounterAnimations() {
    const counters = document.querySelectorAll('[data-count]');
    if (!counters.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => observer.observe(counter));
}

function animateCounter(element) {
    const target = parseInt(element.dataset.count);
    const suffix = element.dataset.suffix || '';
    const duration = 2000;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 4); // easeOutQuart
        const current = Math.round(target * eased);

        element.textContent = current + suffix;

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

/* ── Timeline card expansion ── */
function initTimelineCards() {
    document.querySelectorAll('.timeline-card').forEach(card => {
        const expandBtn = card.querySelector('.timeline-expand-btn');
        if (expandBtn) {
            expandBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                card.classList.toggle('expanded');
            });
        }

        card.addEventListener('click', () => {
            card.classList.toggle('expanded');
        });
    });
}

/* ── Skill bars animation ── */
function initSkillBars() {
    const skillBars = document.querySelectorAll('.skill-bar-fill');
    if (!skillBars.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target.dataset.width;
                entry.target.style.width = target + '%';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });

    skillBars.forEach(bar => observer.observe(bar));
}

/* ── Contact form ── */
function initContactForm() {
    const form = document.getElementById('contact-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitBtn = form.querySelector('.form-submit .btn');
        const statusEl = document.getElementById('form-status');
        const originalText = submitBtn.textContent;

        submitBtn.textContent = 'Sending...';
        submitBtn.disabled = true;

        const data = {
            name: form.querySelector('[name="name"]').value,
            email: form.querySelector('[name="email"]').value,
            subject: form.querySelector('[name="subject"]').value,
            message: form.querySelector('[name="message"]').value,
        };

        try {
            const response = await fetch('/contact/submit/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });
            const result = await response.json();

            if (result.success) {
                statusEl.className = 'form-status success';
                statusEl.textContent = result.message;
                form.reset();
            } else {
                statusEl.className = 'form-status error';
                statusEl.textContent = result.message || 'Something went wrong.';
            }
        } catch (err) {
            statusEl.className = 'form-status error';
            statusEl.textContent = 'Network error. Please try again.';
        }

        submitBtn.textContent = originalText;
        submitBtn.disabled = false;

        setTimeout(() => {
            statusEl.className = 'form-status';
            statusEl.style.display = 'none';
        }, 5000);
    });
}

/* ── Seamless Connected Flow Scroll & Transition ── */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"], a[href*="#"]').forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (!href.includes('#')) return;

            const targetId = href.substring(href.indexOf('#'));
            if (targetId === '#') return;

            const targetSection = document.querySelector(targetId);

            if (targetSection) {
                e.preventDefault();

                // Section divider light-beam pulse animation
                const divider = targetSection.previousElementSibling;
                if (divider && divider.classList.contains('section-divider')) {
                    divider.classList.remove('beam-pulse');
                    void divider.offsetWidth; // trigger reflow
                    divider.classList.add('beam-pulse');
                }

                // Trigger entrance animation for target section elements instantly for connected flow
                targetSection.querySelectorAll('.fade-in, .fade-in-left, .fade-in-right, .scale-in, .stagger-children').forEach(el => {
                    el.classList.add('visible');
                });

                const offset = 90;
                const targetTop = targetSection.getBoundingClientRect().top + window.scrollY - offset;

                window.scrollTo({
                    top: targetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/* ── Top Scroll Progress Bar ── */
function initScrollProgressBar() {
    const progressBar = document.getElementById('scroll-progress');
    if (!progressBar) return;

    let ticking = false;

    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
                if (totalHeight > 0) {
                    const progress = (window.scrollY / totalHeight) * 100;
                    progressBar.style.width = `${Math.min(100, Math.max(0, progress))}%`;
                }
                ticking = false;
            });
            ticking = true;
        }
    }, { passive: true });
}

/* ── Subtle 3D Card Tilt Micro-interactions ── */
function init3DTiltCards() {
    // Disable on touch devices
    if ('ontouchstart' in window || navigator.maxTouchPoints > 0) return;

    const cards = document.querySelectorAll(
        '.project-card, .cert-card, .about-stat-card, .contact-card, .github-stat-card, .github-repo-card'
    );

    cards.forEach(card => {
        card.style.transition = 'transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.4s cubic-bezier(0.2, 0.8, 0.2, 1), border-color 0.3s ease';

        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = ((y - centerY) / centerY) * -6; // max 6 deg tilt
            const rotateY = ((x - centerX) / centerX) * 6;

            card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateY(-6px) scale(1.02)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px) scale(1)';
        });
    });
}

/* ── Active Section Navigation & Magnetic Pill Tracking ── */
function initActiveNavHighlight() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-links a[href*="#"]');
    const activePill = document.getElementById('nav-active-pill');
    const navWrapper = document.querySelector('.nav-links-wrapper');

    if (!sections.length || !navLinks.length) return;

    function movePillTo(element) {
        if (!element || !activePill || !navWrapper || window.innerWidth <= 768) {
            if (activePill) activePill.classList.remove('active');
            return;
        }
        const wrapperRect = navWrapper.getBoundingClientRect();
        const rect = element.getBoundingClientRect();

        const left = rect.left - wrapperRect.left;
        const width = rect.width;
        const top = rect.top - wrapperRect.top;
        const height = rect.height;

        activePill.style.transform = `translate3d(${left}px, ${top}px, 0)`;
        activePill.style.width = `${width}px`;
        activePill.style.height = `${height}px`;
        activePill.classList.add('active');
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                navLinks.forEach(link => {
                    const href = link.getAttribute('href');
                    if (href && href.endsWith(`#${id}`)) {
                        navLinks.forEach(l => l.classList.remove('active'));
                        link.classList.add('active');
                        movePillTo(link);

                        // Trigger light beam sweep on section divider
                        const divider = entry.target.previousElementSibling;
                        if (divider && divider.classList.contains('section-divider')) {
                            divider.classList.add('beam-pulse');
                        }
                    }
                });
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '-10% 0px -45% 0px'
    });

    sections.forEach(section => observer.observe(section));
}
