//Mail Link Animation

const mailIcon = document.querySelector('.bi-envelope-plus');
const mailLink = document.getElementById('mail-link');

// Icon visibility on mouseover.

if (mailLink.innerText !== "") {
mailIcon.style.visibility = "hidden";
mailLink.onmouseover = () =>{
    mailIcon.style.visibility = "visible";
} 
mailLink.onmouseout = () =>{
    mailIcon.style.visibility = "hidden";
}} else mailIcon.style.visibility = "hidden";

// Whastapp link & animation.

const wappIcon = document.querySelector('.bi-whatsapp')
const personWhappLink = document.getElementById('person-whapp-link')

// Icon visibility on mouseover.

if (personWhappLink.innerText !== "") {
wappIcon.style.visibility = "hidden";
personWhappLink.onmouseover = () =>{
    wappIcon.style.visibility = "visible";
} 
personWhappLink.onmouseout = () =>{
    wappIcon.style.visibility = "hidden";
}} else wappIcon.style.visibility = "hidden";

// Builds whastapp web link. OK for Buenos Aires, Argentina,
// works OK in the rest of Argentina´s numbers stored without 
// CPP screening number (15).

let tel = personWhappLink.innerHTML
function buildWhappLink(tel) {
    tel = tel.replace(/[^0-9]+/g, '');
    tel = tel.replace(/^0/, '');
    tel = tel.replace(/15(?=[0-9]{8}$)/, '');
    (tel.length >=11)? tel = tel.replace(/(?<=^54)(9)/, '') : tel = tel;
    if (tel.length == 8) {
        tel = `5411${tel}`
        }
    else if (/^54/.test(tel) == false) {
        tel = `54${tel}`
        }
    link = `https://wa.me/${tel}`;

    return link;
}
link = buildWhappLink(tel)
personWhappLink.setAttribute('href', link);
