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
    "../assets/images/Hidratacion.jfif",
    "../assets/images/Sueno1.jpg"
];

// IMÁGENES EMOCIONES

const imagenesEmociones = [
    "../assets/images/AnimoFeliz.jpg",
    "../assets/images/Animotriste.jpg",
    "../assets/images/Animoenojado.jpg"
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

    const getScrollAmount = () => {
        const card = wrapper.querySelector(".biblioteca-card");
        const cardsContainer = wrapper.querySelector(".biblioteca-cards");
        const gap = cardsContainer ? parseFloat(getComputedStyle(cardsContainer).gap) || 24 : 24;
        return card ? card.offsetWidth + gap : 350;
    };

    // BOTONES
    nextBtn.addEventListener("click", () => {
        wrapper.scrollBy({
            left: getScrollAmount(),
            behavior: "smooth"
        });
    });

    prevBtn.addEventListener("click", () => {
        wrapper.scrollBy({
            left: -getScrollAmount(),
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

if (menuToggle && nav) {
    menuToggle.addEventListener("click", () => {
        const abierto = nav.classList.toggle("active");
        menuToggle.setAttribute("aria-expanded", String(abierto));
    });
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && nav.classList.contains("active")) {
            nav.classList.remove("active");
            menuToggle.setAttribute("aria-expanded", "false");
            menuToggle.focus();
        }
    });
}

// Modo oscuro / bajo estímulo
const btnModoOscuro = document.getElementById("btnModoOscuro");
if (btnModoOscuro) {
    btnModoOscuro.addEventListener("click", () => {
        document.body.classList.toggle("modo-oscuro");
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
                const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
                if (reduceMotion) return; // Respeta prefers-reduced-motion manteniendo los valores finales del HTML

                animateValue("stat1", 0, 51, 1800, "%");
                animateValue("stat2", 0, 34, 1800, "+");
                animateValue("stat3", 0, 4, 1800, "–8 años");
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
/*Funcionalidad para abrir el modal de información de Saber más*/

const modal = document.getElementById("modalInfo");
const btnSaberMas = document.querySelector(".btn-saber-mas");
const closeModal = document.querySelector(".close-modal");

if (modal && btnSaberMas && closeModal) {
    btnSaberMas.addEventListener("click", () => {
        modal.style.display = "flex";
    });

    closeModal.addEventListener("click", () => {
        modal.style.display = "none";
    });

    window.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });
}
/*Animacion al hacer scroll la app desing*/
const animatedElements = document.querySelectorAll('.fade-up, .slide-up');

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if(entry.isIntersecting){
            entry.target.classList.add('show');
        }
    });
}, {
    threshold: 0.2
});

animatedElements.forEach(el => observer.observe(el));
/* ===========================================================
LÓGICA PARA EL FORMULARIO DE ONBOARDING
   =========================================================== */
const formularioOnboarding = document.getElementById("formulario-onboarding"); // Asegúrate de que tu <form> en el HTML tenga este ID

if (formularioOnboarding) {
    formularioOnboarding.addEventListener("submit", async (e) => {
        e.preventDefault(); // Evita que la página se recargue sola

        // Captura los valores de tus campos (ajusta los selectores según los IDs o clases de tus inputs en el HTML)
        const etapaSeleccionada = document.querySelector('input[name="etapa"]:checked')?.value || "Perimenopausa";
        
        // Ejemplo si tus síntomas son checkboxes seleccionados
        const sintomasSeleccionados = Array.from(document.querySelectorAll('input[name="sintomas"]:checked'))
            .map(checkbox => checkbox.value);

        const queBuscasSeleccionado = document.querySelector('input[name="queBuscas"]:checked')?.value || "Comunidad de apoyo";

        const datosOnboarding = {
            etapa: etapaSeleccionada,
            sintomas: sintomasSeleccionados.length > 0 ? sintomasSeleccionados : ["Cambios de ánimo"],
            queBuscas: queBuscasSeleccionado
        };

        try {
            const respuesta = await fetch("http://127.0.0.1:5000/api/completar-onboarding", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                credentials: "include", // <--- ESTO ES LO CLAVE PARA QUE VIAJE LA SESIÓN
                body: JSON.stringify(datosOnboarding)
            });

            const resultado = await respuesta.json();

            if (respuesta.ok) {
                console.log("Onboarding guardado exitosamente:", resultado);
                // Aquí puedes redirigir al usuario a la pantalla principal de tu app
                // window.location.href = "index.html"; 
            } else {
                console.error("Error del servidor:", resultado.error);
                alert("Error: " + resultado.error);
            }
        } catch (error) {
            console.error("Error de red al conectar con el backend:", error);
            alert("No se pudo conectar con el servidor.");
        }
    });
}