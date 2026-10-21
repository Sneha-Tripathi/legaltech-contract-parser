// ==========================================
// LEGALTECH HOME PAGE JAVASCRIPT
// ==========================================

// ---------- PRELOADER ----------

window.addEventListener("load", () => {

    const preloader = document.getElementById("preloader");

    if (preloader) {

        preloader.style.opacity = "0";

        setTimeout(() => {

            preloader.style.display = "none";

        }, 500);

    }

});

// ---------- SCROLL TO TOP ----------

const scrollBtn = document.getElementById("scrollBtn");

window.addEventListener("scroll", () => {

    if (window.scrollY > 250) {

        scrollBtn.style.display = "flex";

    } else {

        scrollBtn.style.display = "none";

    }

});

if (scrollBtn) {

    scrollBtn.addEventListener("click", () => {

        window.scrollTo({

            top: 0,

            behavior: "smooth"

        });

    });

}

// ---------- NAVBAR EFFECT ----------

const navbar = document.querySelector(".custom-navbar");

window.addEventListener("scroll", () => {

    if (window.scrollY > 50) {

        navbar.style.padding = "12px 0";

        navbar.style.background = "rgba(8,12,28,.98)";

        navbar.style.boxShadow = "0 10px 30px rgba(0,0,0,.35)";

    }

    else {

        navbar.style.padding = "18px 0";

        navbar.style.background = "rgba(8,12,28,.92)";

        navbar.style.boxShadow = "none";

    }

});

// ---------- COUNTER ANIMATION ----------

const counters = document.querySelectorAll(".counter");

let counterStarted = false;

function startCounters() {

    if (counterStarted) return;

    counterStarted = true;

    counters.forEach(counter => {

        const text = counter.innerText;

        const number = parseInt(text.replace(/\D/g, ""));

        const suffix = text.replace(/[0-9]/g, "");

        let count = 0;

        const speed = Math.max(10, Math.floor(number / 80));

        const update = () => {

            count += speed;

            if (count >= number) {

                counter.innerText = number + suffix;

            }

            else {

                counter.innerText = count + suffix;

                requestAnimationFrame(update);

            }

        };

        update();

    });

}

window.addEventListener("scroll", () => {

    const section = document.querySelector(".counter-section");

    if (!section) return;

    const position = section.getBoundingClientRect().top;

    if (position < window.innerHeight - 100) {

        startCounters();

    }

});

// ---------- ACTIVE NAVBAR LINK ----------

const links = document.querySelectorAll(".nav-link");

links.forEach(link => {

    link.addEventListener("click", function () {

        links.forEach(item => item.classList.remove("active"));

        this.classList.add("active");

    });

});

// ---------- FEATURE CARD HOVER ----------

const cards = document.querySelectorAll(".feature-card");

cards.forEach(card => {

    card.addEventListener("mouseenter", () => {

        card.style.transform = "translateY(-12px) scale(1.02)";

    });

    card.addEventListener("mouseleave", () => {

        card.style.transform = "translateY(0) scale(1)";

    });

});

// ---------- PARALLAX HERO IMAGE ----------

const dashboard = document.querySelector(".dashboard-img");

window.addEventListener("mousemove", (e) => {

    if (!dashboard) return;

    let x = (window.innerWidth / 2 - e.pageX) / 50;

    let y = (window.innerHeight / 2 - e.pageY) / 50;

    dashboard.style.transform = `translate(${x}px, ${y}px)`;

});

// ---------- FADE IN SECTIONS ----------

const observer = new IntersectionObserver((entries) => {

    entries.forEach(entry => {

        if (entry.isIntersecting) {

            entry.target.classList.add("show");

        }

    });

}, {

    threshold: 0.2

});

document.querySelectorAll(

    ".feature-card,.info-card,.step-card,.testimonial-card,.counter-box"

).forEach(el => {

    observer.observe(el);

});

// ---------- CONSOLE MESSAGE ----------

console.log(

    "%cLegalTech Contract Parser",

    "color:#7c5cff;font-size:22px;font-weight:bold;"

);

console.log(

    "%cAI Powered Legal Document Analysis Platform",

    "color:#00d4ff;font-size:14px;"

);