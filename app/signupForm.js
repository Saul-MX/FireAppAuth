// Registro de usuarios con correo y contraseña
import { createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/13.0.0/firebase-auth.js"
import { auth } from "./firebase.js"
import { getErrorMessage } from "./authErrors.js"

const signupForm = document.querySelector('#signup-form')

signupForm.addEventListener('submit', async (e) => {
    // Evita que el formulario recargue la página
    e.preventDefault()

    const email = signupForm['signup-email'].value
    const password = signupForm['signup-password'].value

    try {
        // Crea el usuario en Firebase; si tiene éxito, la sesión queda iniciada
        const userCredential = await createUserWithEmailAndPassword(auth, email, password)
        console.log(userCredential)

        // Cerrar modal y limpiar campos
        const signupModal = document.querySelector('#signup-modal')
        const modal = bootstrap.Modal.getInstance(signupModal)
        modal.hide()
        signupForm.reset()

        alert(`Bienvenido ${userCredential.user.email}`)
    } catch (error) {
        console.log(error)
        alert(getErrorMessage(error))
    }
})
