const lan = navigator.language.includes("es") ? "es" : "en";
const search = document.getElementsByClassName('q');

for (var i =0; i < search.length; i++) {
    if (lan == "es") {
        search[i].placeholder = '¿A quien buscas?';
    } else {
        search[i].placeholder = 'Anything:';
    }
}