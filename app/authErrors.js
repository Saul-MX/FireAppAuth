// Traduce los códigos de error de Firebase (auth/...) a mensajes claros para el usuario.
// Los mensajes de credenciales son genéricos a propósito: no revelan si un correo
// está registrado o no, para no dar pistas a un atacante.
const messages = {
    'auth/invalid-email': 'El correo electrónico no es válido',
    'auth/missing-password': 'Escribe una contraseña',
    'auth/weak-password': 'La contraseña es muy débil, usa al menos 6 caracteres',
    'auth/email-already-in-use': 'El correo electrónico ya está registrado',
    'auth/invalid-credential': 'Correo o contraseña incorrectos',
    'auth/wrong-password': 'Correo o contraseña incorrectos',
    'auth/user-not-found': 'Correo o contraseña incorrectos',
    'auth/too-many-requests': 'Demasiados intentos, espera un momento e intenta de nuevo',
    'auth/network-request-failed': 'Sin conexión, revisa tu internet',
    'auth/popup-blocked': 'El navegador bloqueó la ventana emergente, permítela e intenta de nuevo',
    'auth/account-exists-with-different-credential': 'Ya existe una cuenta con este correo usando otro método de inicio de sesión'
};

// Devuelve el mensaje correspondiente o uno genérico si el error es desconocido
export const getErrorMessage = (error) =>
    messages[error.code] || 'Ocurrió un error inesperado, intenta de nuevo'

// Errores que no requieren avisar al usuario (él mismo cerró o canceló la ventana)
export const isCancelled = (error) =>
    error.code === 'auth/popup-closed-by-user' || error.code === 'auth/cancelled-popup-request'
