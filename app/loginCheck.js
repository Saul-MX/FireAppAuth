// Muestra u oculta los elementos .logged-in / .logged-out según haya sesión o no
// (opciones del navbar, pantalla de bienvenida y módulo de productos)
const loggedOutLinks = document.querySelectorAll('.logged-out')
const loggedInLinks = document.querySelectorAll('.logged-in')

export const loginChecker = user => {
    if (user) {
        // Sesión activa: se muestran Logout y los productos; se ocultan Signin/Signup y la bienvenida
        loggedInLinks.forEach(link => link.style.display = 'block')
        loggedOutLinks.forEach(link => link.style.display = 'none')
    } else {
        // Sin sesión: se muestran Signin/Signup y la bienvenida; se ocultan Logout y los productos
        loggedInLinks.forEach(link => link.style.display = 'none')
        loggedOutLinks.forEach(link => link.style.display = 'block')
    }
}
