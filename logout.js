import { auth } from "./firebase.js";
import { signOut } from "https://www.gstatic.com/firebasejs/13.0.0/firebase-auth.js"

const logout = document.getElementById('logout');

logout.addEventListener('click', async () => {
    await signOut(auth)
    console.log("Sesion terminada")
})