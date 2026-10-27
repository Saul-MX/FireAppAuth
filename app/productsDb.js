// Operaciones con Cloud Firestore para los productos del usuario.
// Todas las rutas se arman con el uid del usuario autenticado:
//   users/{uid}/products/{productId}                  → nombre, descripcion, precio, categoria, existencias...
//   users/{uid}/products/{productId}/images/{imageId} → data (Base64), nombreArchivo, orden
// La app solo consulta esa ruta, así cada usuario ve y administra únicamente sus productos.
// Las imágenes van en una subcolección (un documento por imagen) para que ningún documento
// se acerque al límite de 1 MiB y para que escuchar la lista de productos no descargue imágenes.
import {
    collection, doc, getDocs, onSnapshot, orderBy, query, serverTimestamp, writeBatch
} from "https://www.gstatic.com/firebasejs/13.0.0/firebase-firestore.js";
import { db } from "./firebase.js";

// Referencias a las colecciones del usuario
const productsCollection = (uid) => collection(db, 'users', uid, 'products');
const imagesCollection = (uid, productId) => collection(db, 'users', uid, 'products', productId, 'images');

// Campos que se guardan de cada imagen (orden 0 = portada)
const imageFields = (image, orden) => ({
    data: image.data,
    nombreArchivo: image.nombreArchivo,
    orden
});

// Escucha en tiempo real (onSnapshot) los productos del usuario, del más nuevo al más antiguo.
// Firestore vuelve a llamar a onChange cada vez que se crea, edita o elimina un producto.
// Devuelve la función que detiene la escucha (se usa al cerrar sesión).
export const listenProducts = (uid, onChange, onError) =>
    onSnapshot(query(productsCollection(uid), orderBy('fechaCreacion', 'desc')), onChange, onError);

// Lectura única (getDocs) de las imágenes de un producto, en su orden
export const getProductImages = async (uid, productId) => {
    const snapshot = await getDocs(query(imagesCollection(uid, productId), orderBy('orden')));
    return snapshot.docs.map((image) => ({ ...image.data(), id: image.id }));
};

// Registra un producto con sus imágenes.
// Se usa un lote (writeBatch): el producto y todas sus imágenes se escriben juntos,
// así que o se guarda todo o no se guarda nada (no quedan productos sin imágenes).
export const createProduct = async (uid, product, images) => {
    const batch = writeBatch(db);
    // doc() sin id genera un id automático, como addDoc, pero sin escribir todavía
    const productRef = doc(productsCollection(uid));

    batch.set(productRef, {
        ...product,
        totalImagenes: images.length,
        fechaCreacion: serverTimestamp(),
        fechaActualizacion: serverTimestamp()
    });

    // Cada imagen es un documento independiente dentro de la subcolección images
    images.forEach((image, index) => {
        batch.set(doc(imagesCollection(uid, productRef.id)), imageFields(image, index));
    });

    await batch.commit();
};

// Actualiza un producto y sincroniza sus imágenes en un solo lote:
// borra las que el usuario quitó, reordena las que conservó y agrega las nuevas.
export const updateProduct = async (uid, productId, product, images, removedIds) => {
    const batch = writeBatch(db);

    batch.update(doc(productsCollection(uid), productId), {
        ...product,
        totalImagenes: images.length,
        fechaActualizacion: serverTimestamp()
    });

    removedIds.forEach((imageId) => {
        batch.delete(doc(imagesCollection(uid, productId), imageId));
    });

    images.forEach((image, index) => {
        if (image.id) {
            // Ya estaba guardada: solo cambia su posición
            batch.update(doc(imagesCollection(uid, productId), image.id), { orden: index });
        } else {
            batch.set(doc(imagesCollection(uid, productId)), imageFields(image, index));
        }
    });

    await batch.commit();
};

// Elimina un producto junto con todas sus imágenes.
// Firestore NO borra las subcolecciones al borrar un documento, por eso primero
// se leen las imágenes y se eliminan en el mismo lote que el producto.
export const deleteProduct = async (uid, productId) => {
    const images = await getDocs(imagesCollection(uid, productId));
    const batch = writeBatch(db);

    images.forEach((image) => batch.delete(image.ref));
    batch.delete(doc(productsCollection(uid), productId));

    await batch.commit();
};
