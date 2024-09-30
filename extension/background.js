async function sendFormsDjango(forms) {
    try {
        const response = await fetch('http://localhost:8000/extension/recibir_forms/', {
            method: 'POST',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify({forms: forms})
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const json = await response.json();
        console.log(json); 
        return json;
    } catch (error) {
        console.error('Error:', error);
    }
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log("Message listener activated:", message);

    if (message.from === "detect_forms" && message.type === "sendForms") {
        console.log("Received message from detect_forms, sending to back_end");
        if (!message.forms || message.forms.length === 0) {
            console.log("Received forms are null or empty");
            sendResponse({ status: "error", message: "Received forms are null or empty" });
            return;
        }
        sendFormsDjango(message.forms).then((filled_forms) => {
            console.log('Received response from back_end:', filled_forms);
            sendResponse({ status: "success", filled_forms: filled_forms });

        }).catch((error) => {
            console.error('Error:', error);
            sendResponse({ status: "error", message: error });
        });
        return true;
    }
  });