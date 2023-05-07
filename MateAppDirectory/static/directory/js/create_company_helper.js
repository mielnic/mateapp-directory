/* Helper purposes:
1) Make Company Name Required.
2) Make Street mandatory for non empty addresses.
*/

// Definitions

const companyName = document.getElementById('id_companyName');
const street = document.getElementById('id_street');
const city = document.getElementById('id_city');
const state = document.getElementById('id_state');
const country = document.getElementById('id_country');
const postalCode = document.getElementById('id_postalCode');

// Make Company Name Required:

companyName.required = true;

// Make Stree mandatory if address => it only enables the other form fields in street is not empty.
// Otherwise it clears a blocks the rest of the form.

// Initial state:

city.disabled = true;
state.disabled = true;
country.disabled = true;
postalCode.disabled = true;

// Event Listener:

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
    } else {
        city.disabled = false;
        state.disabled = false;
        country.disabled = false;
        postalCode.disabled = false;
    }
})