const loggedOutLinks = document.querySelectorAll('.logged-out')
const loggedInLinks = document.querySelectorAll('.logged-in')



export const loginChecker = user => {
    if (user) {
        loggedInLinks.forEach(link => link.style.display = 'block')
        loggedOutLinks.forEach(link => link.style.display = 'none')
    } else {
        loggedInLinks.forEach(link => link.style.display = 'none')
        loggedOutLinks.forEach(link => link.style.display = 'block')
    }
}