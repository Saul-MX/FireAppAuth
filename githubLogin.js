import { GithubAuthProvider, signInWithPopup } from "https://www.gstatic.com/firebasejs/13.0.0/firebase-auth.js";
import { auth } from "./firebase.js";

const githubButton = document.querySelector('#github-login');

githubButton.addEventListener('click', async () => {
    const provider = new GithubAuthProvider();
    provider.addScope('user:email');

    try {
        const credentials = await signInWithPopup(auth, provider);
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
