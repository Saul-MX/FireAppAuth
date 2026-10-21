import { signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/13.0.0/firebase-auth.js"
import { auth } from "./firebase.js"

const siginForm = document.querySelector('#login-form')

siginForm.addEventListener('submit', async (e) => {
    e.preventDefault()
    try {
        const email = siginForm['login-email'].value
        const password = siginForm['login-password'].value
        const credenciales = await signInWithEmailAndPassword(auth, email, password)

        // Cerrar modal y limpiar campos
        const signinModal = document.querySelector('#singin-modal')
        const modal = bootstrap.Modal.getInstance(signinModal)
        modal.hide()

        siginForm.reset()
        console.log(credenciales)
    } catch(error) {
        console.log(error)
        if (error.code === 'auth/invalid-credential' || error.code === 'auth/wrong-password') {
            alert('Correo o contraseña incorrectos')
        } else if (error.code === 'auth/user-not-found') {
            alert('El usuario no existe')
        } else {
            alert(error.message)
        }
    }
})

