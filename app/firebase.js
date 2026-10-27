// Configuración e inicialización de Firebase (SDK modular v13 desde CDN)
import { initializeApp } from "https://www.gstatic.com/firebasejs/13.0.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/13.0.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/13.0.0/firebase-firestore.js";

// Datos del proyecto obtenidos en la consola de Firebase.
// Son públicos: identifican al proyecto, no dan acceso por sí solos.
// La protección real está en los dominios autorizados y las reglas de seguridad.
const firebaseConfig = {
    apiKey: "AIzaSyAcMzFHMrYSmZ09eoVOMNTJ1GTt1CAhBmM",
    authDomain: "k028-e7f83.firebaseapp.com",
    projectId: "k028-e7f83",
    storageBucket: "k028-e7f83.firebasestorage.app",
    messagingSenderId: "705611004597",
    appId: "1:705611004597:web:f86d2f6eab601b70f35cfc"
};

// Inicializa la app y exporta las instancias de autenticación y de Cloud Firestore
// para que el resto de los módulos las reutilicen
export const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);
