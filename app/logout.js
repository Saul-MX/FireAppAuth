// Cierre de sesión
import { signOut } from "https://www.gstatic.com/firebasejs/13.0.0/firebase-auth.js"
import { auth } from "./firebase.js"
import { getErrorMessage } from "./authErrors.js"

const logout = document.querySelector('#logout')

logout.addEventListener('click', async (e) => {
    e.preventDefault()
    try {
        // signOut borra la sesión; onAuthStateChanged (main.js) actualiza el navbar
        await signOut(auth)
        console.log("Sesión terminada")
    } catch (error) {
        console.log(error)
        alert(getErrorMessage(error))
    }
})
