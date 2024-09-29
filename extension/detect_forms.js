
function detectForms() {
    forms = document.querySelectorAll('form');
    if (forms.length === 0) {
        return [];
    }

    const forms_array = [];
    forms.forEach(form => {
        console.log(form)
        const formData = new FormData(form);
        for (let [name, value] of formData.entries()) {
            forms_array.push({[name]: value});
            console.log(`${name}: ${value}`);
        }
    });
    return forms_array; 
};

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log("Message listener activated:", message);
    forms = detectForms();

    sendResponse({ forms: forms });

    return true;
  });
