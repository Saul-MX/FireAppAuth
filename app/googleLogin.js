// Inicio de sesión con Google (OAuth mediante ventana emergente)
import { GoogleAuthProvider, signInWithPopup } from "https://www.gstatic.com/firebasejs/13.0.0/firebase-auth.js";
import { auth } from "./firebase.js";
import { getErrorMessage, isCancelled } from "./authErrors.js";

const googleButton = document.querySelector('#google-login');

googleButton.addEventListener('click', async () => {
    const provider = new GoogleAuthProvider();

    try {
        // Abre la ventana de Google y espera a que el usuario autorice
        const credentials = await signInWithPopup(auth, provider);
        console.log(credentials);

        // Cerrar modal
        const signinModal = document.querySelector('#signin-modal');
        const modal = bootstrap.Modal.getInstance(signinModal);
        modal?.hide();

        alert(`Bienvenido ${credentials.user.displayName || credentials.user.email || ''}`);
    } catch (error) {
        console.error(error);
        // Si el usuario cerró la ventana no se muestra nada
        if (!isCancelled(error)) {
            alert(getErrorMessage(error));
        }
    }
});
