/* Helper Purposes:
1) Toggle Select Company / New Company Form.
2) Make Company Name required if New Company form
3) Auto complete Address with Company Address if exists.
4) Make Street required if address form is not empty.
5) Clear Address Form on toggle.
6) Build and assign the Save Button value to signal the view to run the appropiate saving routine.
7) Translate 2 button strings to spanish.
*/

const companySelection = document.getElementById('id_company');
const street = document.getElementById('id_street');
const city = document.getElementById('id_city');
const state = document.getElementById('id_state');
const country = document.getElementById('id_country');
const postalCode = document.getElementById('id_postalCode');
const companyName = document.getElementById('id_companyName');
const firstName = document.getElementById('id_firstName');
const lastName = document.getElementById('id_lastName');
const companySelector = document.getElementById('company_selector');
const companyForm = document.getElementById('company_form');
const newCompany = document.getElementById('new_company');
const newCompanyTitle = document.getElementById('new_company_title');
const saveButton = document.getElementById('save_button');
let messageNewCompany = 'Add Company';
let messageSelectCompany = 'Select Company';
const lan = navigator.language.includes("es") ? "es" : "en";

// Idioma del formulario:
if (lan == "es") {
    messageNewCompany = 'Agregar Compañía';
    messageSelectCompany = 'Seleccionar Compañía';
}

// Inicializa en 0 el botón de submit.
let css = '0';

// Bloquea la edición de los datos secundarios de Address hasta que ingresa algo o existe algo en Street.
(function () {
    if (street.value == '') {
        city.disabled = true;
        state.disabled = true;
        country.disabled = true;
        postalCode.disabled = true;
    } else {
        city.disabled = false;
        state.disabled = false;
        country.disabled = false;
        postalCode.disabled = false;
    }
})();

// Oculta el formulario de nueva compañía,
companyForm.style.display = 'none';
newCompanyTitle.style.display = 'none';

// Hace mandatorio alternativamente le campo de lastName y firstName
lastName.required = true;
firstName.addEventListener('keyup', (event) => {
    lastName.required = firstName.value == '' ? true : false;
})

// Habilita la edición de los campos secundarios de Address al tipear en street.
street.addEventListener('keyup', (event) => {
    if (street.value == '') {
        city.disabled = true;
        state.disabled = true;
        country.disabled = true;
        postalCode.disabled = true;
        city.value = '';
        state.value = '';
        country.value = '';
        postalCode.value = '';
        buildss();
    } else {
        city.disabled = false;
        state.disabled = false;
        country.disabled = false;
        postalCode.disabled = false;
        buildss();
    }
})

// Carga los campos de Address desde Company al seleccionar una compañía existente.
companySelection.addEventListener('change', (event) => {
    ajax({
        url : `/directory/api/companies/${event.target.value}`,
        load : company => {
            ajax({
                url : `/directory/api/address/${company.address}`,
                load : address => {
                    street.value = address.street;
                    city.value = address.city;
                    state.value = address.state;
                    country.value = address.country;
                    postalCode.value = address.postalCode;
                    city.disabled = false;
                    state.disabled = false;
                    country.disabled = false;
                    postalCode.disabled = false;
                }
            })
        }
    })
});

// XHR llamado por el evento de arriba.
function ajax(config) {
    
    const xhr = new XMLHttpRequest();
    xhr.open("GET", config.url);
    xhr.send();

    xhr.onload = function () {
        if (xhr.status === 200) {
            console.log(`Done. We've got ${xhr.response.length} bytes`);
            config.load(JSON.parse(xhr.response));
            buildss();
        } else {
            console.log(`Error ${xhr.status}: ${xhr.statusText}`);
            clear();
            buildss()
        }
    };

    xhr.onerror = function () {
        console.log('Network Error');
    };
};

// Muestra u oculta el formulario de nueva compañía.
function toggle() {
    
    if (companyForm.style.display === 'none'){
    companySelector.style.display = 'none';
    newCompanyTitle.style.display = 'block';
    companyForm.style.display = 'block';
    companyName.required = true
    newCompany.innerHTML = messageSelectCompany;
    clear();
    buildss();
    } else { companySelector.style.display = 'block';
    companyForm.style.display = 'none';
    newCompanyTitle.style.display = 'none';
    companyName.required = false
    newCompany.innerHTML = messageNewCompany;
    clear();
    buildss();
}
}

//Limpia el formulario de address si hubo una compañía seleccionada y se vuelve a crear compañia.
function clear() {
    companySelection.value = '';
    companyName.value = '';
    street.value = '';
    city.value = '';
    state.value = '';
    country.value = '';
    postalCode.value = '';
}

// Construye el value del botón para señalizar a la vista los formularios correctos.
function buildss() {
    if (companyForm.style.display === 'none' && companyName.value === '') {
        css = '0';
    } else if (companyForm.style.display === 'block') {
        css = '2';
    } else {
        css = '1';
    }
    let ass = (street.value === ''? '0' : '1');
    let ss = `1${ass}${css}`
    saveButton.name = ss
    saveButton.value = ss
}