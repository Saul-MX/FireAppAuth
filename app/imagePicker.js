// Selección, validación y vista previa de las imágenes del producto.
// Reglas: mínimo 1 y máximo 5 imágenes, solo archivos de imagen y de máximo 10 MB cada uno.
// Las imágenes ya procesadas se quedan en memoria hasta que se envía el formulario.
import { processImage } from "./imageProcessor.js";

const MIN_IMAGES = 1;
const MAX_IMAGES = 5;
const MAX_FILE_MB = 10;
const MAX_FILE_SIZE = MAX_FILE_MB * 1024 * 1024; // peso máximo del archivo original

const input = document.querySelector('#product-images');
const dropzone = document.querySelector('#image-dropzone');
const dropzoneText = document.querySelector('#image-dropzone-text');
const previews = document.querySelector('#image-previews');
const counter = document.querySelector('#image-counter');
const feedback = document.querySelector('#image-feedback');

const REMOVE_ICON = '<svg aria-hidden="true" viewBox="0 0 16 16" fill="none"><path d="m4.5 4.5 7 7m0-7-7 7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" /></svg>';

let images = [];    // imágenes actuales: guardadas en Firestore (con id) o nuevas (sin id)
let savedIds = [];  // ids de las imágenes que ya tenía el producto al abrir el formulario
let busy = false;   // true mientras se procesan o se cargan imágenes
let session = 0;    // cambia al reiniciar para descartar trabajos de un formulario anterior

// Muestra el peso en KB o MB
const formatSize = (bytes) => bytes < 1024 * 1024
    ? `${Math.max(1, Math.round(bytes / 1024))} KB`
    : `${(bytes / 1024 / 1024).toFixed(1)} MB`;

const fileNames = (files) => files.map((file) => `«${file.name}»`).join(', ');

// Muestra un mensaje de error en la sección de imágenes (cadena vacía = ocultarlo)
const showError = (message) => {
    feedback.textContent = message;
    feedback.hidden = !message;
    if (message) feedback.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
};

// Bloquea la selección mientras se procesan o cargan imágenes
const setBusy = (value, text = 'Procesando imágenes…') => {
    busy = value;
    input.disabled = value;
    dropzone.classList.toggle('is-busy', value);
    dropzoneText.textContent = value ? text : 'Haz clic o arrastra tus imágenes aquí';
};

// Dibuja la vista previa de cada imagen con su peso y un botón para quitarla
const render = () => {
    counter.textContent = `${images.length} / ${MAX_IMAGES}`;

    previews.replaceChildren(...images.map((image, index) => {
        const item = document.createElement('li');
        item.className = 'image-preview';
        item.title = image.nombreArchivo;

        const img = document.createElement('img');
        img.src = image.data;
        img.alt = `Vista previa de ${image.nombreArchivo}`;

        // Las nuevas muestran cuánto pesaba el original y cuánto pesa ya comprimida
        const size = document.createElement('span');
        size.className = 'image-size';
        size.textContent = image.originalSize
            ? `${formatSize(image.originalSize)} → ${formatSize(image.data.length)}`
            : formatSize(image.data.length);

        const remove = document.createElement('button');
        remove.type = 'button';
        remove.className = 'image-remove';
        remove.innerHTML = REMOVE_ICON;
        remove.setAttribute('aria-label', `Quitar ${image.nombreArchivo}`);
        remove.addEventListener('click', () => {
            images.splice(index, 1);
            showError('');
            render();
        });

        item.append(img, size, remove);

        // La primera imagen (orden 0) es la portada del producto
        if (index === 0) {
            const badge = document.createElement('span');
            badge.className = 'image-badge';
            badge.textContent = 'Portada';
            item.append(badge);
        }
        return item;
    }));
};

// Revisa los archivos elegidos antes de procesarlos: tipo, peso y cantidad.
// Devuelve el mensaje de error, o una cadena vacía si todo está bien.
const validateFiles = (files) => {
    const notImages = files.filter((file) => !file.type.startsWith('image/'));
    if (notImages.length) {
        const verb = notImages.length === 1 ? 'no es una imagen' : 'no son imágenes';
        return `Solo se permiten imágenes: ${fileNames(notImages)} ${verb}.`;
    }

    const tooLarge = files.filter((file) => file.size > MAX_FILE_SIZE);
    if (tooLarge.length) {
        const verb = tooLarge.length === 1 ? 'pesa' : 'pesan';
        return `Cada imagen debe pesar máximo ${MAX_FILE_MB} MB: ${fileNames(tooLarge)} ${verb} más.`;
    }

    if (images.length + files.length > MAX_IMAGES) {
        const available = MAX_IMAGES - images.length;
        if (images.length === 0) {
            return `Puedes subir máximo ${MAX_IMAGES} imágenes por producto y seleccionaste ${files.length}.`;
        }
        if (available === 0) {
            return `El producto ya tiene ${MAX_IMAGES} imágenes, el máximo permitido. Quita alguna para agregar otra.`;
        }
        return `Puedes subir máximo ${MAX_IMAGES} imágenes por producto. Ya tienes ${images.length}, solo puedes agregar ${available} más.`;
    }

    return '';
};

// Valida, procesa y agrega a la vista previa las imágenes elegidas.
// Si algún archivo no cumple, no se agrega ninguno y se explica el motivo.
const addFiles = async (fileList) => {
    const files = [...fileList];
    input.value = ''; // permite volver a elegir los mismos archivos
    if (!files.length || busy) return;

    const error = validateFiles(files);
    showError(error);
    if (error) return;

    const current = session;
    setBusy(true);
    try {
        const processed = [];
        // Una por una para no saturar la memoria con fotos grandes
        for (const file of files) {
            try {
                processed.push(await processImage(file));
            } catch {
                throw new Error(`No se pudo leer «${file.name}». Prueba con una imagen JPG, PNG o WebP.`);
            }
        }
        if (current !== session) return; // el formulario se cerró mientras tanto
        images.push(...processed);
        render();
    } catch (error) {
        if (current === session) showError(error.message);
    } finally {
        if (current === session) setBusy(false);
    }
};

input.addEventListener('change', () => addFiles(input.files));

// Arrastrar y soltar archivos sobre la zona de imágenes
dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('is-dragging');
});
dropzone.addEventListener('dragleave', () => dropzone.classList.remove('is-dragging'));
dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('is-dragging');
    addFiles(e.dataTransfer.files);
});

// Si un archivo se suelta fuera de la zona, evita que el navegador lo abra y se salga de la app
['dragover', 'drop'].forEach((type) => {
    window.addEventListener(type, (e) => {
        if (e.dataTransfer?.types.includes('Files')) e.preventDefault();
    });
});

// Deja la sección vacía (producto nuevo o al cerrar el formulario)
export const resetImages = () => {
    session++;
    images = [];
    savedIds = [];
    setBusy(false);
    showError('');
    render();
};

// Estado de espera mientras se leen de Firestore las imágenes guardadas
export const showImagesLoading = () => setBusy(true, 'Cargando imágenes guardadas…');

// Carga las imágenes que ya tiene el producto (modo edición)
export const setSavedImages = (saved) => {
    images = [...saved];
    savedIds = saved.map((image) => image.id);
    setBusy(false);
    render();
};

// Imágenes en el orden en que se guardarán (la primera es la portada)
export const getImages = () => [...images];

// Ids de las imágenes guardadas que el usuario quitó al editar
export const getRemovedIds = () => savedIds.filter((id) => !images.some((image) => image.id === id));

// true mientras no se debe guardar porque hay imágenes en proceso
export const isBusy = () => busy;

// Valida la cantidad antes de guardar (mínimo 1, máximo 5) y muestra el error si no se cumple
export const validateImageCount = () => {
    let error = '';
    if (images.length < MIN_IMAGES) {
        error = `Agrega al menos ${MIN_IMAGES} imagen del producto.`;
    } else if (images.length > MAX_IMAGES) {
        error = `Puedes subir máximo ${MAX_IMAGES} imágenes por producto.`;
    }
    showError(error);
    return !error;
};
