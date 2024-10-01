function resaltarForms() {
    inputs = document.querySelectorAll('input[type="text"]');
    if (inputs.length === 0) {
        return { status: "error", message: "No se encontraron formularios" };
    }
    inputs.forEach(input => {
        console.log(input);
        input.style.backgroundColor = 'lightgreen';
        input.style.border = '2px solid black';  
        input.style.padding = '4px';
    });

    return { status: "success" };
}


chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if ((message.from === "popup" && message.type === "resaltarForms")) {
        const result = resaltarForms();
        sendResponse(result);
    }
    return true;
});

