
function detectForms() {
    forms = document.querySelectorAll('form');
    if (forms.length === 0) {
        return {};
    }

    const forms_content = {};
    forms.forEach(form => {
        console.log(form)
        const formData = new FormData(form);
        for (let [name, value] of formData.entries()) {
                forms_content[name] =  value;
                console.log(`${name}: ${value}`);
            }
    });
    return forms_content;
};

function highlightForms() {
    forms = document.querySelectorAll('form');
    if (forms.length === 0) {
        return { status: "error", message: "No forms found" };
    }

    forms.forEach(form => {
        console.log(form)
        const formData = new FormData(form);
        for (let [name, value] of formData.entries()) {
            const inputElement = form.querySelector(`[name="${name}"]`);

            if (inputElement && inputElement.type === "text") {
                inputElement.style.backgroundColor = 'lightgreen';
                inputElement.style.border = '2px solid black';  
                inputElement.style.padding = '4px';               
            }
        }
    });
    return { status: "success" };
}


chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if ((message.from === "popup" || message.type === "highlightForms")) {
        const result = highlightForms();
        sendResponse(result);
    }
    return true;
});

async function sendForms(){
    return new Promise((resolve, reject) => {
        forms = detectForms();
        console.log("Forms",forms);
        console.log("sending");
        chrome.runtime.sendMessage({from: "detect_forms", type: "sendForms", forms: forms}, (response) => {
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
    if ((message.from === "popup" || message.type === "sendForms")) {
        console.log("Sending to background");
        sendForms().then((result) => {
            console.log('Received response from background:', result);
            const filled_forms = result.filled_forms.forms;
            for (const [name, value] of Object.entries(filled_forms)) {
                const inputElement = document.querySelector(`[name="${name}"]`);
                console.log(inputElement, name, value);
                if (inputElement) {
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



/*
console.log("Message listener activated:", message);
forms = detectForms();

const response = sendForms();

sendResponse({ forms: response });
return true; */