// Inicio de sesión con Twitter/X (OAuth mediante ventana emergente)
import { TwitterAuthProvider, signInWithPopup } from "https://www.gstatic.com/firebasejs/13.0.0/firebase-auth.js";
import { auth } from "./firebase.js";
import { getErrorMessage, isCancelled } from "./authErrors.js";

const twitterButton = document.querySelector('#twitter-login');

twitterButton.addEventListener('click', async () => {
    const provider = new TwitterAuthProvider();

    try {
        // Abre la ventana de X y espera a que el usuario autorice
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
