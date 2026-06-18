window.addEventListener("load", function () {

    const imagen = document.querySelector(".imagen-proposito");

    imagen.classList.add("mostrar");

});

document.addEventListener("DOMContentLoaded", ()=>{

    const elementos =
    document.querySelectorAll(".animar");

    const observer =
    new IntersectionObserver((entries)=>{

        entries.forEach(entry=>{

            if(entry.isIntersecting){

                entry.target.classList.add("visible");
            }

        });

    },{
        threshold:0.15
    });

    elementos.forEach(el=>{
        observer.observe(el);
    });

});

window.addEventListener("load", ()=>{

    const imgFunciones =
    document.querySelector(".imagen-funciones");

    if(imgFunciones){
        imgFunciones.classList.add("mostrar");
    }

});

const imagenesHabitos = [

    "ImagenesNeuroPausa/Hidratacion.jfif",
    "ImagenesNeuroPausa/Sueno1.jpg"

];

const imagenesEmociones = [

    "ImagenesNeuroPausa/AnimoFeliz.jpg",
    "ImagenesNeuroPausa/Animotriste.jpg",
    "ImagenesNeuroPausa/Animoenojado.jpg"

];
//hidratacion y sueño

let indiceHabitos = 0;

const imgHabitos =
document.getElementById("img-habitos");

if(imgHabitos){

    setInterval(() => {

        imgHabitos.classList.add("fade-out");

        setTimeout(() => {

            indiceHabitos++;

            if(indiceHabitos >= imagenesHabitos.length){
                indiceHabitos = 0;
            }

            imgHabitos.src =
            imagenesHabitos[indiceHabitos];

            imgHabitos.classList.remove("fade-out");

        },400);

    },3000);

}
// ESTADO EMOCIONAL

let indiceEmociones = 0;

const imgEmociones =
document.getElementById("img-emociones");

if(imgEmociones){

    setInterval(() => {

        imgEmociones.classList.add("fade-out");

        setTimeout(() => {

            indiceEmociones++;

            if(indiceEmociones >= imagenesEmociones.length){
                indiceEmociones = 0;
            }

            imgEmociones.src =
            imagenesEmociones[indiceEmociones];

            imgEmociones.classList.remove("fade-out");

        },400);

    },3500);

}
