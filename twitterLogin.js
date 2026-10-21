import { TwitterAuthProvider, signInWithPopup } from "https://www.gstatic.com/firebasejs/13.0.0/firebase-auth.js";
import { auth } from "./firebase.js";

const twitterButton = document.querySelector('#twitter-login');

twitterButton.addEventListener('click', async () => {
    const provider = new TwitterAuthProvider();

    try {
        const credentials = await signInWithPopup(auth, provider);
        console.log(credentials);

        //Cerrar modal
        const signinModal = document.querySelector('#singin-modal');
        const modal = bootstrap.Modal.getInstance(signinModal);
        modal?.hide();
        alert(`Bienvenido ${credentials.user.displayName || credentials.user.email || ''}`);
    } catch (error) {
        console.error(error);
        if (error.code !== 'auth/popup-closed-by-user') {
            alert(error.message);
        }
    }
});
