
function detectarForms() {
    inputs = document.querySelectorAll('input[type="text"]');
    if (inputs.length === 0) {
        return {};
    }
    const forms_content = {};
    inputs.forEach(input => {
        if (input.name !== "") {
            forms_content[input.name] = input.value;
        } else if (input.id !== "") {
            forms_content[input.id] = input.value;
        }
/*         else {
            const closest_div = input.closest('div');
            const label = closest_div.querySelector('label');
            if (label) {
                forms_content[label.textContent] = input.value;
            }
        } */
    });
    return forms_content;
};

async function sendForms(){
    return new Promise((resolve, reject) => {
        forms = detectarForms();
        console.log("Forms",forms);
        console.log("sending");
        chrome.runtime.sendMessage({from: "detect_forms", type: "llenarForms", forms: forms}, (response) => {
            console.log('Response:', response);
            if (chrome.runtime.lastError) {
                reject(chrome.runtime.lastError);
            }
            else {
                resolve(response);
            }
        });
    });
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if ((message.from === "popup" && message.type === "llenarForms")) {
        console.log("Sending to background");
        sendForms().then((result) => {
            console.log('Received response from background:', result);
            const filled_forms = result.filled_forms.forms;
            for (const [name, value] of Object.entries(filled_forms)) {

                const inputElement = document.querySelector(`[id="${name}"]`);

                if (!inputElement) {
                    const inputElement = document.querySelector(`[name="${name}"]`);
                }
                
                if (inputElement) {
                    console.log("Setting value for", name, value);
                    inputElement.value = value;
                }
            }
            sendResponse(result);

        }).catch((error) => {
            console.error('Error:', error);
            sendResponse({ status: "error", message: error });
        });
        return true;
    }
});