const slider = document.getElementById("slider");
const person = document.getElementById("id_person");
const company = document.getElementById("id_company");
const action = document.getElementById("id_action");

person.style.display = "block";
company.style.display = "none";
action.removeAttribute('checked');

function selectChoice(){

    if (slider.checked == true){
        person.style.display = "none";
        company.style.display = "block";
    } else {
        person.style.display = "block";
        company.style.display = "none";
    }

}