function ajax(url) {
    let table;
    const xhr = new XMLHttpRequest();
    console.log(xhr.responseXML)
    xhr.onload = function(){
      const xmlDoc = xhr.responseXML;
      table = xmlDoc.getElementById('companies-table-block')
    }
    xhr.open("GET", url);
    xhr.send();
    return xhr;
  }