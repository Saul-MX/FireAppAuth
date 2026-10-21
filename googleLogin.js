import { GoogleAuthProvider, signInWithPopup } from "https://www.gstatic.com/firebasejs/13.0.0/firebase-auth.js";
import { auth } from "./firebase.js";

const googleButton = document.querySelector('#google-login');

googleButton.addEventListener('click', async () => {
    const provider = new GoogleAuthProvider();

    try {
        const credenciales = await signInWithPopup(auth, provider);
        console.log(credenciales);

        // Cerrar modal
        const signinModal = document.querySelector('#singin-modal');
        const modal = bootstrap.Modal.getInstance(signinModal);
        if (modal) {
            modal.hide();
            alert('Bienvnido' + credenciales.user.displayName)
        }
    } catch (error) {
        console.error(error);
        if (error.code !== 'auth/popup-closed-by-user') {
            alert(error.message);
        }
    }
});
