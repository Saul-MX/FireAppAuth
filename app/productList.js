// Listado en tiempo real de los productos del usuario con sesión activa, con sus imágenes.
// showProducts() empieza a escuchar users/{uid}/products al iniciar sesión y
// clearProducts() deja de escuchar y limpia la pantalla al cerrarla.
import { listenProducts, getProductImages } from "./productsDb.js";
import { openEditForm, closeProductForm } from "./productForm.js";
import { askDeleteProduct, closeDeleteDialog } from "./productDelete.js";
import { getDbErrorMessage } from "./firestoreErrors.js";

const list = document.querySelector('#product-list');
const template = document.querySelector('#product-template');
const statusMessage = document.querySelector('#products-status');
const emptyState = document.querySelector('#products-empty');
const productCount = document.querySelector('#products-count');
const userName = document.querySelector('#products-user');
const userPath = document.querySelector('#products-path');

const currency = new Intl.NumberFormat('es-MX', { style: 'currency', currency: 'MXN' });
const dateFormat = new Intl.DateTimeFormat('es-MX', { dateStyle: 'medium', timeStyle: 'short' });

let unsubscribe = null;       // detiene la escucha de Firestore
let currentUid = null;        // uid del usuario cuyos productos están en pantalla
let products = [];            // productos del último snapshot, del más nuevo al más antiguo
const cards = new Map();      // productId → tarjeta en pantalla
const imageCache = new Map(); // productId → { version, images } imágenes ya leídas

const showStatus = (message) => {
    statusMessage.textContent = message;
    statusMessage.hidden = !message;
};

const formatDate = (timestamp) => (timestamp?.toDate ? dateFormat.format(timestamp.toDate()) : '');

// Escribe los datos del producto en su tarjeta (textContent evita que se inyecte HTML)
const fillCard = (card, product) => {
    const stock = Number(product.existencias) || 0;
    const stockLabel = card.querySelector('.product-stock');
    stockLabel.textContent = stock === 0 ? 'Agotado' : `${stock} en existencia`;
    stockLabel.dataset.level = stock === 0 ? 'out' : stock <= 5 ? 'low' : 'ok';

    const total = product.totalImagenes || 0;
    const photoCount = card.querySelector('.product-photo-count');
    photoCount.textContent = total === 1 ? '1 imagen' : `${total} imágenes`;
    photoCount.hidden = !total;

    // Fecha de registro, o de la última edición si el producto se modificó
    const edited = product.fechaActualizacion?.toMillis?.() - product.fechaCreacion?.toMillis?.() > 0;
    card.querySelector('.product-date').textContent = edited
        ? `Editado: ${formatDate(product.fechaActualizacion)}`
        : `Registrado: ${formatDate(product.fechaCreacion)}`;

    card.querySelector('.product-category').textContent = product.categoria;
    card.querySelector('.product-name').textContent = product.nombre;
    card.querySelector('.product-description').textContent = product.descripcion;
    card.querySelector('.product-price').textContent = currency.format(Number(product.precio) || 0);
    card.querySelector('.product-cover img').alt = product.nombre;
};

// Muestra la portada y las miniaturas de un producto.
// images = null mientras se leen de Firestore (se ve un esqueleto de carga)
const renderGallery = (productId, images, emptyText = 'Sin imágenes') => {
    const card = cards.get(productId);
    if (!card) return;

    const cover = card.querySelector('.product-cover img');
    const thumbs = card.querySelector('.product-thumbs');
    card.classList.toggle('is-loading', images === null);
    card.querySelector('.product-cover-note').textContent = images?.length === 0 ? emptyText : '';
    thumbs.replaceChildren();

    if (!images?.length) {
        cover.removeAttribute('src');
        return;
    }

    // Al tocar una miniatura, esa imagen pasa a ser la principal
    const select = (index) => {
        cover.src = images[index].data;
        [...thumbs.children].forEach((thumb, i) => thumb.classList.toggle('is-active', i === index));
    };

    if (images.length > 1) {
        images.forEach((image, index) => {
            const thumb = document.createElement('button');
            thumb.type = 'button';
            thumb.className = 'product-thumb';
            thumb.setAttribute('aria-label', `Ver imagen ${index + 1} de ${images.length}`);

            const img = document.createElement('img');
            img.src = image.data;
            img.alt = '';

            thumb.append(img);
            thumb.addEventListener('click', () => select(index));
            thumbs.append(thumb);
        });
    }
    select(0);
};

// Crea una tarjeta a partir del <template id="product-template"> y conecta sus botones
const createCard = (productId) => {
    const card = template.content.firstElementChild.cloneNode(true);
    const findProduct = () => products.find((product) => product.id === productId);

    card.querySelector('.product-edit').addEventListener('click', () => {
        const product = findProduct();
        if (product) openEditForm(product);
    });
    card.querySelector('.product-delete').addEventListener('click', () => {
        const product = findProduct();
        if (product) askDeleteProduct(product);
    });
    return card;
};

// Sincroniza las tarjetas con el último snapshot: crea, actualiza, ordena y quita
const renderList = () => {
    const ids = new Set(products.map((product) => product.id));

    // Quita las tarjetas de productos eliminados
    cards.forEach((card, id) => {
        if (ids.has(id)) return;
        card.remove();
        cards.delete(id);
        imageCache.delete(id);
    });

    products.forEach((product, index) => {
        let card = cards.get(product.id);
        if (!card) {
            card = createCard(product.id);
            cards.set(product.id, card);
            renderGallery(product.id, imageCache.get(product.id)?.images ?? null);
        }
        fillCard(card, product);
        // Solo se mueve si no está en su posición (el más nuevo va primero)
        if (list.children[index] !== card) list.insertBefore(card, list.children[index] ?? null);
    });

    showStatus('');
    emptyState.hidden = products.length > 0;
    productCount.textContent = products.length === 1 ? '1 producto' : `${products.length} productos`;
};

// Lee las imágenes de los productos nuevos o modificados.
// La versión es fechaActualizacion: si no cambió, se reutilizan las ya leídas (ahorra lecturas).
const loadImages = (uid) => {
    products.forEach(async (product) => {
        const version = product.fechaActualizacion?.toMillis?.() ?? 0;
        const cached = imageCache.get(product.id);
        // Espera a que Firestore confirme la escritura y no repite la lectura de la misma versión
        if (product.pending || cached?.version === version) return;

        // Mientras llegan las nuevas se siguen mostrando las anteriores (si las hay)
        const entry = { version, images: cached?.images ?? null };
        imageCache.set(product.id, entry);
        if (!entry.images) renderGallery(product.id, null);

        try {
            const images = await getProductImages(uid, product.id);
            // Se descarta si mientras tanto cambió la sesión o llegó una versión más nueva
            if (uid !== currentUid || imageCache.get(product.id) !== entry) return;
            entry.images = images;
            renderGallery(product.id, images);
        } catch (error) {
            console.error(error);
            if (imageCache.get(product.id) !== entry) return;
            imageCache.delete(product.id); // se vuelve a intentar con el siguiente cambio
            renderGallery(product.id, [], 'No se pudieron cargar las imágenes');
        }
    });
};

// Empieza a escuchar users/{uid}/products del usuario que inició sesión
export const showProducts = (user) => {
    clearProducts();
    currentUid = user.uid;
    userName.textContent = user.displayName || user.email || 'tu cuenta';
    userPath.textContent = `users/${user.uid}/products`;
    productCount.textContent = 'Cargando…';
    showStatus('Cargando tus productos…');

    unsubscribe = listenProducts(user.uid, (snapshot) => {
        products = snapshot.docs.map((doc) => ({
            // 'estimate' da una fecha aproximada mientras Firestore confirma la escritura
            ...doc.data({ serverTimestamps: 'estimate' }),
            id: doc.id,
            pending: doc.metadata.hasPendingWrites
        }));
        renderList();
        loadImages(user.uid);
    }, (error) => {
        console.error(error);
        showStatus(`No se pudieron cargar tus productos. ${getDbErrorMessage(error)}`);
    });
};

// Deja de escuchar y borra de la pantalla todo lo del usuario anterior
export const clearProducts = () => {
    unsubscribe?.();
    unsubscribe = null;
    currentUid = null;
    products = [];
    cards.clear();
    imageCache.clear();
    list.replaceChildren();
    productCount.textContent = '';
    userName.textContent = '';
    userPath.textContent = '';
    emptyState.hidden = true;
    showStatus('');
    closeProductForm();
    closeDeleteDialog();
};
