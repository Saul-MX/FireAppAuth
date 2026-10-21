import { onAuthStateChanged } from "https://www.gstatic.com/firebasejs/13.0.0/firebase-auth.js";
import { auth } from "./firebase.js";
import { loginChecker } from "./loginCheck.js";

import './firebase.js';
import './singupForm.js';
import './signinForm.js';
import './googleLogin.js';
import './githubLogin.js';
import './twitterLogin.js';
import './logout.js';
import './loginCheck.js';

// Escuchar cambios en la autenticación
onAuthStateChanged(auth, async (user) => {
    loginChecker(user);
});