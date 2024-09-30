document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('detectForm');
    button.addEventListener('click', clickDetectarForms); 

    const fillFormButton = document.createElement('button');
    fillFormButton.id = 'fillForm';
    fillFormButton.textContent = 'Fill Form';
    document.body.appendChild(fillFormButton);

    fillFormButton.addEventListener('click', llenarForms);

});

async function clickDetectarForms() {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        console.log('Tabs:', tabs);
        chrome.tabs.sendMessage(tabs[0].id, { from: "popup", type: "highlightForms" }, (response) => {

            console.log('Response:', response);
            if (response.status === "error") {
                console.log("Error:", response.message);
                const no_forms = document.createElement('h2');
                no_forms.textContent = response.message;
                document.body.appendChild(no_forms);
                return;
            }
            else{
                console.log("Forms highlighted");
                const forms_highlighted = document.createElement('h2');
                forms_highlighted.textContent = "Forms highlighted";
                document.body.appendChild(forms_highlighted);

                const button = document.getElementById('detectForm');
                button.remove();
            }
        });
    });
}


async function llenarForms() {
    chrome.tabs.query({active : true, currentWindow : true}, (tabs) => {
        console.log("sending message to fill forms to detect_forms")
        chrome.tabs.sendMessage(tabs[0].id, {from: "popup", type: "sendForms"}, (response) => {
            alert(response.message);
        });
    })
}

async function obtenerMensaje() {
    try {
        const response = await fetch('http://localhost:8000/extension/retornar_json/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const json = await response.json();
        console.log(json); 
        return json.mensaje;
    } catch (error) {
        console.error('Error:', error);
    }
}

async function showAlert() {
    const mensaje = await obtenerMensaje();

    alert(mensaje);
    document.body.innerHTML = '';
    const h1 = document.createElement('h1');
    h1.textContent = mensaje;
    document.body.appendChild(h1);
}

/* chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    console.log('Tabs:', tabs);
    chrome.tabs.sendMessage(tabs[0].id, { from: "popup", type: "getForms" }, (response) => {
        console.log('Response:', response);

    });
}); */