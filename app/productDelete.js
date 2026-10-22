// Eliminación de productos con confirmación (ventana #delete-modal)
import { auth } from "./firebase.js";
import { deleteProduct } from "./productsDb.js";
import { getDbErrorMessage } from "./firestoreErrors.js";
import { showToast } from "./toast.js";

const deleteModal = document.querySelector('#delete-modal');
const deleteMessage = document.querySelector('#delete-message');
const confirmButton = document.querySelector('#delete-confirm');

let selected = null; // producto que se va a eliminar

const modal = () => bootstrap.Modal.getOrCreateInstance(deleteModal);

// Pide confirmación antes de eliminar
export const askDeleteProduct = (product) => {
    selected = product;
    const total = product.totalImagenes;
    const images = total === 1 ? 'su imagen' : total ? `sus ${total} imágenes` : 'sus imágenes';
    deleteMessage.textContent = `Se eliminará «${product.nombre}» junto con ${images}. Esta acción no se puede deshacer.`;
    confirmButton.disabled = false;
    confirmButton.textContent = 'Eliminar';
    modal().show();
};

// Cierra la confirmación sin eliminar nada (también se usa al cerrar sesión)
export const closeDeleteDialog = () => {
    selected = null;
    modal().hide();
};

confirmButton.addEventListener('click', async () => {
    if (!selected) return;
    const product = selected;
    confirmButton.disabled = true;
    confirmButton.textContent = 'Eliminando…';

    try {
        // Borra el documento del producto y su subcolección de imágenes
        await deleteProduct(auth.currentUser.uid, product.id);
        showToast(`Se eliminó «${product.nombre}»`);
    } catch (error) {
        console.error(error);
        showToast(getDbErrorMessage(error), 'error');
    } finally {
        if (selected === product) closeDeleteDialog();
    }
});
