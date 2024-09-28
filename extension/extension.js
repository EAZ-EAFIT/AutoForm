document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('myButton');
    button.addEventListener('click', showAlert);  // Asigna el evento en el archivo JS
});

async function obtenerMensaje() {
    try {
        const response = await fetch('http://localhost:8000/extension/retornar_json/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const json = await response.json();
        console.log(json);  // Verifica lo que está recibiendo
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