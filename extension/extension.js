function showAlert() {
    alert('Hello World');
    document.body.innerHTML = '';
    const h1 = document.createElement('h1');
    h1.textContent = 'Hello World';
    document.body.appendChild(h1);
}