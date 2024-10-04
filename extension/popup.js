document.addEventListener('DOMContentLoaded', async function() {
    try {
        // Hacemos un fetch a Django para verificar si el usuario está autenticado
        const response = await fetch('http://localhost:8000/extension/validar_sesion/'); // Ruta del API de Django
        const data = await response.json();
        
        const resaltarButton = document.getElementById('resaltarForm');
        
        if (data.autenticado) {
            // Si el usuario está autenticado, mostramos los botones

            // Evento para resaltar formularios
            resaltarButton.addEventListener('click', resaltarForms);

            // Botón para llenar formularios (creado dinámicamente)
            const fillFormButton = document.createElement('button');
            fillFormButton.id = 'fillForm';
            fillFormButton.textContent = 'Llenar Formulario';
            document.body.appendChild(fillFormButton);

            // Evento para llenar formularios
            fillFormButton.addEventListener('click', llenarForms);

        } else {
            // Si no está autenticado, ocultamos el botón de resaltar
            resaltarButton.style.display = 'none';

            // Mostramos un mensaje de no autenticado y enlaces
            document.body.innerHTML = `
                <h1>No estás autenticado, por favor inicia sesión</h1>
                <a href="http://localhost:8000/Users/login/">Login</a><br>
                <a href="http://localhost:8000/Users/register/">Registrarse</a><br>
                <a href="http://localhost:8000/extension/home/">Home</a>
            `;
        }
    } catch (error) {
        console.error("Error al verificar autenticación:", error);
        document.body.innerHTML = "<h1>Error al verificar autenticación</h1>";
    }
});


async function resaltarForms() {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        console.log('Tabs:', tabs);
        chrome.tabs.sendMessage(tabs[0].id, { from: "popup", type: "resaltarForms" }, (response) => {

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

                const button = document.getElementById('resaltarForm');
                button.remove();
            }
        });
    });
}


async function llenarForms() {
    chrome.tabs.query({active : true, currentWindow : true}, (tabs) => {
        console.log("sending message to fill forms to detect_forms")
        chrome.tabs.sendMessage(tabs[0].id, {from: "popup", type: "llenarForms"}, (response) => {
            console.log('Response:', response);
        });
    })
}