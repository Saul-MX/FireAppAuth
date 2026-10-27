// Avisos breves en una esquina de la pantalla (toast de Bootstrap)
const toastElement = document.querySelector('#app-toast');
const toastMessage = document.querySelector('#app-toast-message');

// type: 'success' (por defecto) o 'error'
export const showToast = (message, type = 'success') => {
    toastMessage.textContent = message;
    toastElement.classList.toggle('is-error', type === 'error');
    bootstrap.Toast.getOrCreateInstance(toastElement, { delay: 4000 }).show();
};
