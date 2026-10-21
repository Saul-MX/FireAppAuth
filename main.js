// Punto de entrada: carga cada módulo de la carpeta app/ y vigila la sesión
import { onAuthStateChanged } from "https://www.gstatic.com/firebasejs/13.0.0/firebase-auth.js";
import { auth } from "./app/firebase.js";
import { loginChecker } from "./app/loginCheck.js";

// Cada import registra los eventos de su funcionalidad
import './app/signupForm.js';
import './app/signinForm.js';
import './app/googleLogin.js';
import './app/facebookLogin.js';
import './app/githubLogin.js';
import './app/twitterLogin.js';
import './app/logout.js';

// Se ejecuta al cargar la página y cada vez que se inicia o cierra sesión.
// user es el usuario autenticado o null si no hay sesión.
onAuthStateChanged(auth, (user) => {
    loginChecker(user);
});
