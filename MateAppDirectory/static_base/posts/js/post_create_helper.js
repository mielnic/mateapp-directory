var slider = document.getElementById("slider");
var person = document.getElementById("id_person");
var company = document.getElementById("id_company");
// var action = document.getElementById("id_action");

person.style.display = "block";
company.style.display = "none";
// action.removeAttribute('checked');

function selectChoice(){

    if (slider.checked == true){
        person.style.display = "none";
        company.style.display = "block";
        company.required = true;
    } else {
        person.style.display = "block";
        person.required = true;
        company.style.display = "none";
    }

}