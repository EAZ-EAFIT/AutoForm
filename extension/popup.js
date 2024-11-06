document.addEventListener('DOMContentLoaded', async function() {
    try {
        const response = await fetch('http://localhost:8000/extension/validar_sesion/');
        const data = await response.json();
        
        const resaltarButton = document.getElementById('resaltarForm');
        
        if (data.autenticado) {
            resaltarButton.addEventListener('click', resaltarForms);

            // Botón para llenar formularios (creado dinámicamente)
            const fillFormButton = document.createElement('button');
            fillFormButton.id = 'fillForm';
            fillFormButton.textContent = 'Llenar Formulario';
            fillFormButton.classList.add('btn', 'btn-success', 'mt-2', 'btn-sm'); // Añadido w-100 para ancho completo
            document.body.appendChild(fillFormButton);

            fillFormButton.addEventListener('click', llenarForms);

        } else {
            resaltarButton.style.display = 'none';

            document.body.innerHTML = `
                <div class="text-center mx-auto" style="max-width: 400px; padding: 20px;">
                    <h1 class="text-danger">No estás autenticado</h1>
                    <p class="text-muted">Por favor, inicia sesión o regístrate</p>
                    <a href="http://localhost:8000/Users/login/" class="btn btn-link btn-sm pb-1">Login</a>
                    <a href="http://localhost:8000/Users/register/" class="btn btn-link btn-sm ms-2 pb-1">Registrarse</a>
                    <a href="http://localhost:8000/extension/home/" class="btn btn-link btn-sm ms-2">Home</a>
                </div>
            `;
        }
    } catch (error) {
        console.error("Error al verificar autenticación:", error);
        document.body.innerHTML = `
            <div class="text-center text-danger mx-auto" style="max-width: 400px; padding: 20px;">
                <h1>Error al verificar autenticación</h1>
                <p>Ocurrió un problema al conectarse al servidor. Inténtelo más tarde.</p>
            </div>
        `;
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