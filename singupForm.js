import { createUserWithEmailAndPassword  } from "https://www.gstatic.com/firebasejs/13.0.0/firebase-auth.js";
import { auth } from './firebase.js'    
const singupForm = document.querySelector('#singup-form')

singupForm.addEventListener('submit', async(e) => {
    e.preventDefault()
    const email = singupForm['singup-email'].value
    const password = singupForm['singup-password'].value

    try {
        const userCredential = await createUserWithEmailAndPassword(auth, email, password)

        const singupModal = document.querySelector('#singup-modal')
        const modal = bootstrap.Modal.getInstance(singupModal)
        modal.hide()

        document.querySelector('#singup-email').value = ''
        document.querySelector('#singup-password').value = ''

        console.log(userCredential)
    }catch (error) {
        console.log(error)
        if (error.code === 'auth/email-already-in-use') {
            alert('El correo electrónico ya está en uso')
        }else if (error.code === 'auth/weak-password') {
            alert('La contraseña es muy débil')
        }
    }
})  