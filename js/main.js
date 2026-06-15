/* ============================================
   NATALEXPERIENCE TOURS — Main JavaScript
   ============================================ */

(function () {
  'use strict';

  // WhatsApp Config
  const WHATSAPP_NUMBER = '5584999868411';
  const WHATSAPP_BASE_URL = `https://wa.me/${WHATSAPP_NUMBER}`;

  // ---- Navbar Scroll Effect ---- //
  const navbar = document.querySelector('.navbar');

  function updateNavbar() {
    if (!navbar) return;
    if (window.scrollY > 60) {
      navbar.classList.remove('navbar--transparent');
      navbar.classList.add('navbar--solid');
    } else {
      navbar.classList.add('navbar--transparent');
      navbar.classList.remove('navbar--solid');
    }
  }

  window.addEventListener('scroll', updateNavbar, { passive: true });
  updateNavbar();

  // ---- Hamburger Menu ---- //
  const hamburger = document.querySelector('.navbar__hamburger');
  const mobileMenu = document.querySelector('.mobile-menu');

  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('active');
      mobileMenu.classList.toggle('active');
      document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
    });

    // Close on link click
    mobileMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        mobileMenu.classList.remove('active');
        document.body.style.overflow = '';
      });
    });
  }

  // ---- Scroll Animations (IntersectionObserver) ---- //
  const animateElements = document.querySelectorAll('.animate-on-scroll');

  if (animateElements.length > 0) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -50px 0px' }
    );

    animateElements.forEach(el => observer.observe(el));
  }

  // ---- FAQ Accordion ---- //
  const faqItems = document.querySelectorAll('.faq-item');

  faqItems.forEach(item => {
    const question = item.querySelector('.faq-item__question');
    if (question) {
      question.addEventListener('click', () => {
        const isActive = item.classList.contains('active');

        // Close all
        faqItems.forEach(i => i.classList.remove('active'));

        // Toggle current
        if (!isActive) {
          item.classList.add('active');
        }
      });
    }
  });

  // ---- WhatsApp Link Builder ---- //
  window.openWhatsApp = function (message) {
    const defaultMessage = 'Olá! Gostaria de saber mais sobre as experiências da NatalExperience Tours. Podem me ajudar?';
    const msg = encodeURIComponent(message || defaultMessage);
    window.open(`${WHATSAPP_BASE_URL}?text=${msg}`, '_blank');
  };

  // Set up all WhatsApp buttons
  document.querySelectorAll('[data-whatsapp]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const message = btn.getAttribute('data-whatsapp-message') || '';
      window.openWhatsApp(message);
    });
  });

  // ---- Bento Gallery Lightbox ---- //
  const lightbox = document.querySelector('.lightbox');
  const lightboxImg = lightbox ? lightbox.querySelector('img') : null;
  const lightboxClose = lightbox ? lightbox.querySelector('.lightbox__close') : null;
  const lightboxPrev = lightbox ? lightbox.querySelector('.lightbox__prev') : null;
  const lightboxNext = lightbox ? lightbox.querySelector('.lightbox__next') : null;
  const lightboxCurrentEl = document.getElementById('lightbox-current');
  const lightboxTotalEl = document.getElementById('lightbox-total');

  let galleryImages = [];
  let currentGalleryIndex = 0;

  // Collect gallery image sources from bento gallery items
  function collectGalleryImages() {
    let items = Array.from(document.querySelectorAll('.bento-gallery__item'));
    items.sort((a, b) => {
      return (parseInt(a.getAttribute('data-gallery-index'), 10) || 0) - (parseInt(b.getAttribute('data-gallery-index'), 10) || 0);
    });
    galleryImages = [];
    items.forEach(item => {
      const img = item.querySelector('img');
      if (img && img.src) {
        galleryImages.push(img.src);
      } else {
        // For placeholder divs, create a canvas snapshot
        const placeholder = item.querySelector('.placeholder-img');
        if (placeholder) {
          // Use a data URL representing the placeholder
          const canvas = document.createElement('canvas');
          canvas.width = 800;
          canvas.height = 600;
          const ctx = canvas.getContext('2d');
          const computedStyle = window.getComputedStyle(placeholder);
          const bg = computedStyle.backgroundImage;
          // Create a gradient fill
          if (bg && bg.includes('linear-gradient')) {
            const colors = bg.match(/#[a-fA-F0-9]{6}/g) || ['#0077b6', '#00b4d8'];
            const gradient = ctx.createLinearGradient(0, 0, 800, 600);
            gradient.addColorStop(0, colors[0] || '#0077b6');
            gradient.addColorStop(1, colors[1] || '#00b4d8');
            ctx.fillStyle = gradient;
          } else {
            ctx.fillStyle = '#0077b6';
          }
          ctx.fillRect(0, 0, 800, 600);
          // Add text
          const span = placeholder.querySelector('span');
          if (span) {
            ctx.font = '80px serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(span.textContent, 400, 300);
          }
          galleryImages.push(canvas.toDataURL('image/jpeg', 0.8));
        }
      }
    });
    return galleryImages;
  }

  function showGalleryImage(index) {
    if (galleryImages.length === 0) return;
    currentGalleryIndex = (index + galleryImages.length) % galleryImages.length;
    if (lightboxImg) {
      lightboxImg.src = galleryImages[currentGalleryIndex];
      lightboxImg.style.animation = 'none';
      lightboxImg.offsetHeight; // trigger reflow
      lightboxImg.style.animation = 'lightboxFadeIn 0.3s ease';
    }
    if (lightboxCurrentEl) lightboxCurrentEl.textContent = currentGalleryIndex + 1;
    if (lightboxTotalEl) lightboxTotalEl.textContent = galleryImages.length;
  }

  function openLightbox(index) {
    collectGalleryImages();
    if (galleryImages.length === 0) return;
    showGalleryImage(index);
    if (lightbox) {
      lightbox.classList.add('active');
      document.body.style.overflow = 'hidden';
    }
  }

  function closeLightbox() {
    if (lightbox) {
      lightbox.classList.remove('active');
      document.body.style.overflow = '';
    }
  }

  // Global function for the "See all" button
  window.openGalleryLightbox = function(index) {
    openLightbox(index || 0);
  };

  if (lightbox && lightboxImg) {
    // Click on gallery items
    document.querySelectorAll('.bento-gallery__item').forEach(item => {
      item.addEventListener('click', (e) => {
        // Don't trigger if clicking the "see all" button itself
        if (e.target.closest('.bento-gallery__see-all')) return;
        const index = parseInt(item.getAttribute('data-gallery-index'), 10) || 0;
        openLightbox(index);
      });
    });

    // Also handle legacy [data-lightbox] elements
    document.querySelectorAll('[data-lightbox]').forEach(el => {
      if (!el.classList.contains('bento-gallery__item')) {
        el.addEventListener('click', () => {
          const imgEl = el.querySelector('img');
          if (imgEl && lightboxImg) {
            lightboxImg.src = imgEl.src;
            lightbox.classList.add('active');
            document.body.style.overflow = 'hidden';
          }
        });
      }
    });

    // Close button
    if (lightboxClose) {
      lightboxClose.addEventListener('click', (e) => {
        e.stopPropagation();
        closeLightbox();
      });
    }

    // Prev/Next buttons
    if (lightboxPrev) {
      lightboxPrev.addEventListener('click', (e) => {
        e.stopPropagation();
        showGalleryImage(currentGalleryIndex - 1);
      });
    }

    if (lightboxNext) {
      lightboxNext.addEventListener('click', (e) => {
        e.stopPropagation();
        showGalleryImage(currentGalleryIndex + 1);
      });
    }

    // Click background to close
    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) {
        closeLightbox();
      }
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
      if (!lightbox.classList.contains('active')) return;
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowLeft') showGalleryImage(currentGalleryIndex - 1);
      if (e.key === 'ArrowRight') showGalleryImage(currentGalleryIndex + 1);
    });
  }

  // ---- Counter Animation ---- //
  const counters = document.querySelectorAll('[data-counter]');

  if (counters.length > 0) {
    const counterObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const el = entry.target;
            const target = parseInt(el.getAttribute('data-counter'), 10);
            const suffix = el.getAttribute('data-suffix') || '';
            const duration = 2000;
            const step = Math.ceil(target / (duration / 16));
            let current = 0;

            const update = () => {
              current += step;
              if (current >= target) {
                el.textContent = target.toLocaleString('pt-BR') + suffix;
              } else {
                el.textContent = current.toLocaleString('pt-BR') + suffix;
                requestAnimationFrame(update);
              }
            };
            requestAnimationFrame(update);
            counterObserver.unobserve(el);
          }
        });
      },
      { threshold: 0.5 }
    );

    counters.forEach(el => counterObserver.observe(el));
  }

  // ---- Smooth Scroll for anchor links ---- //
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      const targetEl = document.querySelector(targetId);
      if (targetEl) {
        e.preventDefault();
        targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ---- Contact Form ---- //
  const APPS_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbwVj1RiePDs5QZAmSpU4H6kFAZM74EyBinIwKa1pD0YJCnnnU83hQhJTYV9zcjFuT5z/exec';

  const contactForm = document.querySelector('#contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const submitBtn = contactForm.querySelector('[type="submit"]');
      submitBtn.disabled = true;
      submitBtn.textContent = 'Enviando...';

      const payload = {
        name:     contactForm.querySelector('[name="name"]')?.value || '',
        email:    contactForm.querySelector('[name="email"]')?.value || '',
        phone:    contactForm.querySelector('[name="phone"]')?.value || '',
        interest: contactForm.querySelector('[name="interest"]')?.value || '',
        message:  contactForm.querySelector('[name="message"]')?.value || ''
      };

      try {
        await fetch(APPS_SCRIPT_URL, {
          method: 'POST',
          body: JSON.stringify(payload)
        });

        const successEl = document.createElement('div');
        successEl.className = 'form-success';
        successEl.innerHTML = '✅ Mensagem enviada! Entraremos em contato em breve.';
        successEl.style.cssText = 'background: #d4edda; color: #155724; padding: 16px 24px; border-radius: 8px; margin-top: 16px; font-weight: 500; text-align: center;';
        contactForm.appendChild(successEl);
        setTimeout(() => successEl.remove(), 6000);
        contactForm.reset();
      } catch (err) {
        const errorEl = document.createElement('div');
        errorEl.innerHTML = '❌ Erro ao enviar. Tente pelo WhatsApp ou e-mail direto.';
        errorEl.style.cssText = 'background: #f8d7da; color: #721c24; padding: 16px 24px; border-radius: 8px; margin-top: 16px; font-weight: 500; text-align: center;';
        contactForm.appendChild(errorEl);
        setTimeout(() => errorEl.remove(), 6000);
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Enviar Mensagem';
      }
    });
  }

  // ---- Preloader (optional) ---- //
  window.addEventListener('load', () => {
    document.body.classList.add('loaded');
  });

})();
