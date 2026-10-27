// Formulario para registrar y editar productos (ventana #product-modal).
// El mismo formulario sirve para ambos casos: editingId indica qué producto se está editando.
import { auth } from "./firebase.js";
import { createProduct, updateProduct, getProductImages } from "./productsDb.js";
import {
    resetImages, showImagesLoading, setSavedImages, getImages, getRemovedIds, isBusy, validateImageCount
} from "./imagePicker.js";
import { getDbErrorMessage } from "./firestoreErrors.js";
import { showToast } from "./toast.js";

const productModal = document.querySelector('#product-modal');
const productForm = document.querySelector('#product-form');
const modalEyebrow = document.querySelector('#product-modal-eyebrow');
const modalTitle = document.querySelector('#product-modal-title');
const submitButton = document.querySelector('#product-submit');
const feedback = document.querySelector('#product-feedback');

let editingId = null; // id del producto en edición; null cuando se registra uno nuevo
let saving = false;   // true mientras se guarda en Firestore
let formSession = 0;  // cambia al reiniciar el formulario para ignorar respuestas atrasadas

const modal = () => bootstrap.Modal.getOrCreateInstance(productModal);

// Muestra un error general del formulario (cadena vacía = ocultarlo)
const showError = (message) => {
    feedback.textContent = message;
    feedback.hidden = !message;
};

const submitLabel = () => (editingId ? 'Guardar cambios' : 'Guardar producto');

// Bloquea el botón mientras se guarda para evitar registros duplicados
const setSaving = (value) => {
    saving = value;
    submitButton.disabled = value;
    submitButton.textContent = value ? 'Guardando…' : submitLabel();
};

// Deja el formulario vacío y en modo "nuevo producto"
const resetForm = () => {
    formSession++;
    editingId = null;
    productForm.reset();
    resetImages();
    showError('');
    setSaving(false);
    modalEyebrow.textContent = 'Agrega un artículo a tu catálogo';
    modalTitle.textContent = 'Nuevo producto';
};

// Abre el formulario vacío para registrar un producto
const openCreateForm = () => {
    resetForm();
    modal().show();
};

// Cierra y limpia el formulario (también se usa al cerrar sesión)
export const closeProductForm = () => {
    resetForm();
    modal().hide();
};

// Abre el formulario con los datos de un producto para editarlo
export const openEditForm = async (product) => {
    resetForm();
    editingId = product.id;
    modalEyebrow.textContent = 'Actualiza la información';
    modalTitle.textContent = 'Editar producto';
    submitButton.textContent = submitLabel();

    productForm['product-name'].value = product.nombre ?? '';
    productForm['product-description'].value = product.descripcion ?? '';
    productForm['product-price'].value = product.precio ?? '';
    productForm['product-category'].value = product.categoria ?? '';
    productForm['product-stock'].value = product.existencias ?? '';
    modal().show();

    // Se leen de Firestore las imágenes guardadas para editar exactamente esas
    const session = formSession;
    showImagesLoading();
    try {
        const images = await getProductImages(auth.currentUser.uid, product.id);
        if (session === formSession) setSavedImages(images);
    } catch (error) {
        console.error(error);
        if (session !== formSession) return;
        closeProductForm();
        showToast(getDbErrorMessage(error), 'error');
    }
};

// Lee y valida los campos. Devuelve el objeto que se guarda en Firestore o null si hay un error.
const readProduct = () => {
    const nombre = productForm['product-name'].value.trim();
    const descripcion = productForm['product-description'].value.trim();
    const precio = Number(productForm['product-price'].value);
    const categoria = productForm['product-category'].value;
    const existencias = Number(productForm['product-stock'].value);

    let error = '';
    if (!nombre || !descripcion) {
        error = 'Escribe el nombre y la descripción del producto.';
    } else if (!Number.isFinite(precio) || precio < 0) {
        error = 'El precio debe ser un número igual o mayor a 0.';
    } else if (!categoria) {
        error = 'Elige una categoría.';
    } else if (!Number.isInteger(existencias) || existencias < 0) {
        error = 'Las existencias deben ser un número entero igual o mayor a 0.';
    }

    showError(error);
    if (error) return null;
    // El precio se guarda redondeado a centavos
    return { nombre, descripcion, precio: Math.round(precio * 100) / 100, categoria, existencias };
};

productForm.addEventListener('submit', async (e) => {
    // Evita que el formulario recargue la página
    e.preventDefault();
    if (saving) return;
    showError('');

    if (isBusy()) {
        showError('Espera a que terminen de cargarse las imágenes.');
        return;
    }
    // Primero los campos y después las imágenes (de 1 a 5)
    const product = readProduct();
    if (!product || !validateImageCount()) return;

    const session = formSession;
    const productId = editingId;
    setSaving(true);

    try {
        // Siempre con el uid del usuario autenticado: users/{uid}/products
        const uid = auth.currentUser.uid;
        if (productId) {
            await updateProduct(uid, productId, product, getImages(), getRemovedIds());
        } else {
            await createProduct(uid, product, getImages());
        }
        if (session !== formSession) return;

        setSaving(false);
        modal().hide();
        showToast(productId ? 'Cambios guardados' : 'Producto registrado');
    } catch (error) {
        console.error(error);
        if (session !== formSession) return;
        setSaving(false);
        showError(getDbErrorMessage(error));
    }
});

// Mientras se guarda no se permite cerrar la ventana
productModal.addEventListener('hide.bs.modal', (e) => {
    if (saving) e.preventDefault();
});

// Al cerrarse (Cancelar, X o Esc) se limpia para la próxima vez
productModal.addEventListener('hidden.bs.modal', resetForm);

// Al abrirse, el cursor queda en el nombre
productModal.addEventListener('shown.bs.modal', () => productForm['product-name'].focus());

// Botones "Nuevo producto" (encabezado y lista vacía)
document.querySelectorAll('[data-new-product]').forEach((button) => {
    button.addEventListener('click', openCreateForm);
});
