
// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/13.0.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/13.0.0/firebase-auth.js";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyAcMzFHMrYSmZ09eoVOMNTJ1GTt1CAhBmM",
    authDomain: "k028-e7f83.firebaseapp.com",
    projectId: "k028-e7f83",
    storageBucket: "k028-e7f83.firebasestorage.app",
    messagingSenderId: "705611004597",
    appId: "1:705611004597:web:f86d2f6eab601b70f35cfc"
};

console.log("Hola nena");


// Initialize Firebase
export const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);


