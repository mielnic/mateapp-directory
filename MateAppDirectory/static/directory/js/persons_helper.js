const lan = navigator.language.includes("es") ? "es" : "en";
const search = document.getElementById('id_q');

if (lan == "es") {
    search.placeholder = 'Nombres y/o Apellidos:';
} else {
    search.placeholder = 'Names:';
}