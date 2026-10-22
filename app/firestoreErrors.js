// Traduce los códigos de error de Cloud Firestore a mensajes claros para el usuario
const messages = {
    'permission-denied': 'Firestore rechazó la operación. Revisa que la base de datos esté en modo de prueba y que sus reglas no hayan vencido',
    'unauthenticated': 'Tu sesión expiró, vuelve a iniciar sesión',
    'unavailable': 'No hay conexión con Firestore, revisa tu internet e intenta de nuevo',
    'deadline-exceeded': 'Firestore tardó demasiado en responder, intenta de nuevo',
    'resource-exhausted': 'Se alcanzó la cuota gratuita de Firestore, intenta más tarde',
    'invalid-argument': 'Los datos no son válidos o son demasiado grandes para guardarse',
    'not-found': 'No se encontró en Firestore: revisa que la base de datos esté creada y que el producto no se haya eliminado'
};

// Devuelve el mensaje correspondiente o uno genérico si el error es desconocido
export const getDbErrorMessage = (error) =>
    messages[error.code] || 'Ocurrió un error con la base de datos, intenta de nuevo';
