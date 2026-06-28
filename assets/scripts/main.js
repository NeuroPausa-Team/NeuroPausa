window.addEventListener("load", function () {

    const imagen = document.querySelector(".imagen-proposito");

    if (imagen) {
        imagen.classList.add("mostrar");
    }

});

document.addEventListener("DOMContentLoaded", () => {

    const elementos = document.querySelectorAll(".animar");

    const observer = new IntersectionObserver((entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
            }

        });

    }, {
        threshold: 0.15
    });

    elementos.forEach(el => {
        observer.observe(el);
    });

});

window.addEventListener("load", () => {

    const imgFunciones = document.querySelector(".imagen-funciones");

    if (imgFunciones) {
        imgFunciones.classList.add("mostrar");
    }

});

// IMÁGENES HÁBITOS
const imagenesHabitos = [
    "assets/images/Hidratacion.jfif",
    "assets/images/Sueno1.jpg"
];

// IMÁGENES EMOCIONES

const imagenesEmociones = [
    "assets/images/AnimoFeliz.jpg",
    "assets/images/Animotriste.jpg",
    "assets/images/Animoenojado.jpg"
];

// HIDRATACIÓN Y SUEÑO

let indiceHabitos = 0;

const imgHabitos = document.getElementById("img-habitos");

if (imgHabitos) {

    setInterval(() => {

        imgHabitos.classList.add("fade-out");

        setTimeout(() => {

            indiceHabitos++;

            if (indiceHabitos >= imagenesHabitos.length) {
                indiceHabitos = 0;
            }

            imgHabitos.src = imagenesHabitos[indiceHabitos];

            imgHabitos.classList.remove("fade-out");

        }, 400);

    }, 3000);

}

// ESTADO EMOCIONAL
let indiceEmociones = 0;

const imgEmociones = document.getElementById("img-emociones");

if (imgEmociones) {

    setInterval(() => {

        imgEmociones.classList.add("fade-out");

        setTimeout(() => {

            indiceEmociones++;

            if (indiceEmociones >= imagenesEmociones.length) {
                indiceEmociones = 0;
            }

            imgEmociones.src = imagenesEmociones[indiceEmociones];

            imgEmociones.classList.remove("fade-out");

        }, 400);

    }, 3500);

}




document.addEventListener("DOMContentLoaded", () => {

    const wrapper = document.querySelector(".biblioteca-wrapper");
    const prevBtn = document.querySelector(".prev");
    const nextBtn = document.querySelector(".next");

    if (!wrapper || !prevBtn || !nextBtn) return;

    const scrollAmount = 350;

    // BOTONES
    nextBtn.addEventListener("click", () => {
        wrapper.scrollBy({
            left: scrollAmount,
            behavior: "smooth"
        });
    });

    prevBtn.addEventListener("click", () => {
        wrapper.scrollBy({
            left: -scrollAmount,
            behavior: "smooth"
        });
    });

    // DRAG / SWIPE
    let isDragging = false;
    let startX;
    let scrollLeft;

    wrapper.addEventListener("mousedown", (e) => {
        isDragging = true;
        wrapper.classList.add("dragging");

        startX = e.pageX - wrapper.offsetLeft;
        scrollLeft = wrapper.scrollLeft;
    });

    wrapper.addEventListener("mouseleave", () => {
        isDragging = false;
        wrapper.classList.remove("dragging");
    });

    wrapper.addEventListener("mouseup", () => {
        isDragging = false;
        wrapper.classList.remove("dragging");
    });

    wrapper.addEventListener("mousemove", (e) => {
        if (!isDragging) return;

        e.preventDefault();

        const x = e.pageX - wrapper.offsetLeft;
        const walk = (x - startX) * 1.5;

        wrapper.scrollLeft = scrollLeft - walk;
    });
let touchStartX = 0;
let touchScrollLeft = 0;

wrapper.addEventListener("touchstart", (e) => {
    touchStartX = e.touches[0].pageX;
    touchScrollLeft = wrapper.scrollLeft;
});

wrapper.addEventListener("touchmove", (e) => {
    const touchX = e.touches[0].pageX;
    const walk = (touchX - touchStartX) * 1.2;

    wrapper.scrollLeft = touchScrollLeft - walk;
});
});
const menuToggle = document.querySelector(".menu-toggle");
const nav = document.querySelector("nav");

if(menuToggle && nav){
    menuToggle.addEventListener("click", () => {
        nav.classList.toggle("active");
    });
}
/*FUNCION DE ANIMAR NUMEROS EN PROPOSITO:*/ 
document.addEventListener("DOMContentLoaded", () => {

    const statsSection = document.querySelector(".estadisticas");

    if (!statsSection) return;

    let animated = false;

    function animateValue(id, start, end, duration, suffix = "") {
        const element = document.getElementById(id);
        let current = start;
        const increment = end / (duration / 16);

        const timer = setInterval(() => {
            current += increment;

            if (current >= end) {
                current = end;
                clearInterval(timer);
            }

            element.textContent = Math.floor(current) + suffix;

        }, 16);
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {

            if (entry.isIntersecting && !animated) {
                animated = true;

                animateValue("stat1", 0, 51, 1800, "%");
                animateValue("stat2", 0, 34, 1800, "+");
                animateValue("stat3", 0, 7, 1800, " años");
            }

        });
    }, {
        threshold: 0.35
    });

    observer.observe(statsSection);

});
/*Login de iniciar sesion*/
const btnLogin = document.getElementById("btnLogin");

if (btnLogin) {
    btnLogin.addEventListener("click", () => {
        window.location.href = "login.html";
    });
}
/*Boton para registrarse*/
const btnRegister = document.getElementById("btnRegister");

if (btnRegister) {
    btnRegister.addEventListener("click", () => {
        window.location.href = "register.html";
    });
}
/*Funcionalidad agendar cita*/
const btnCita = document.getElementById("btnCita");

if(btnCita){
    btnCita.addEventListener("click", () => {
        window.location.href = "cita.html";
    });
} 