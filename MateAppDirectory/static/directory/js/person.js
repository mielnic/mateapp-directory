(() => {
    const xhr = new XMLHttpRequest();

    const url = '../api/companies';
    
    xhr.open("GET", url);

    xhr.send();

    xhr.onload = function () {
        if (xhr.status === 200) {
            console.log(`Hecho. Se obtuvieron ${xhr.response.length} bytes`);
            console.log(xhr.response);
        } else {
            console.log(`Error ${xhr.status}: ${xhr.statusText}`);
        }
    };

    xhr.onerror = function () {
        console.log('Error de Red');
    };
})();