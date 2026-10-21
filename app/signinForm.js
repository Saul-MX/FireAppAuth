// Inicio de sesión con correo y contraseña
import { signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/13.0.0/firebase-auth.js"
import { auth } from "./firebase.js"
import { getErrorMessage } from "./authErrors.js"

const signinForm = document.querySelector('#login-form')

signinForm.addEventListener('submit', async (e) => {
    // Evita que el formulario recargue la página
    e.preventDefault()

    const email = signinForm['login-email'].value
    const password = signinForm['login-password'].value

    try {
        // Valida las credenciales contra Firebase
        const credentials = await signInWithEmailAndPassword(auth, email, password)
        console.log(credentials)

        // Cerrar modal y limpiar campos
        const signinModal = document.querySelector('#signin-modal')
        const modal = bootstrap.Modal.getInstance(signinModal)
        modal.hide()
        signinForm.reset()

        alert(`Bienvenido ${credentials.user.email}`)
    } catch (error) {
        console.log(error)
        alert(getErrorMessage(error))
    }
})
