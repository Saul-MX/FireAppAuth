// Muestra u oculta las opciones del navbar según haya sesión o no
const loggedOutLinks = document.querySelectorAll('.logged-out')
const loggedInLinks = document.querySelectorAll('.logged-in')

export const loginChecker = user => {
    if (user) {
        // Sesión activa: se muestra Logout y se ocultan Signin/Signup
        loggedInLinks.forEach(link => link.style.display = 'block')
        loggedOutLinks.forEach(link => link.style.display = 'none')
    } else {
        // Sin sesión: se muestran Signin/Signup y se oculta Logout
        loggedInLinks.forEach(link => link.style.display = 'none')
        loggedOutLinks.forEach(link => link.style.display = 'block')
    }
}
