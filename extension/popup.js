document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('resaltarForm');
    button.addEventListener('click', resaltarForms); 

    const fillFormButton = document.createElement('button');
    fillFormButton.id = 'fillForm';
    fillFormButton.textContent = 'Fill Form';
    document.body.appendChild(fillFormButton);

    fillFormButton.addEventListener('click', llenarForms);

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