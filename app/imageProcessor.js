// Procesa cada imagen en el navegador antes de guardarla en Firestore:
// 1) la lee con FileReader, 2) la redimensiona en un <canvas> y
// 3) la comprime y la convierte a Base64 (Data URL).
// Firestore limita cada documento a 1 MiB, por eso cada imagen se deja en máximo 300 KB.

const MAX_SIDE = 800;                          // px máximos del lado más largo
const MAX_IMAGE_BYTES = 300 * 1024;            // tamaño máximo del texto Base64 que se guarda
const QUALITIES = [0.8, 0.7, 0.6, 0.5, 0.4];   // calidades a probar, de mejor a menor

// WebP pesa menos que JPEG con la misma calidad, pero algunos navegadores (como Safari)
// no lo generan desde canvas y devuelven PNG; en ese caso se usa JPEG.
const OUTPUT_TYPE = (() => {
    const canvas = document.createElement('canvas');
    canvas.width = canvas.height = 1;
    return canvas.toDataURL('image/webp').startsWith('data:image/webp') ? 'image/webp' : 'image/jpeg';
})();

// Lee el archivo original como Data URL (texto Base64)
const readFile = (file) => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = () => reject(reader.error);
    reader.readAsDataURL(file);
});

// Carga el Data URL en un <img> para poder dibujarlo en el canvas
const loadImage = (src) => new Promise((resolve, reject) => {
    const image = new Image();
    image.onload = () => resolve(image);
    image.onerror = () => reject(new Error('El navegador no pudo leer la imagen'));
    image.src = src;
});

// Redimensiona y comprime una imagen; devuelve los datos listos para Firestore
export const processImage = async (file) => {
    const image = await loadImage(await readFile(file));
    const { naturalWidth: width, naturalHeight: height } = image;
    if (!width || !height) throw new Error('La imagen no tiene medidas válidas');

    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    // Escala para que el lado más largo mida como máximo MAX_SIDE (nunca se agranda)
    let scale = Math.min(1, MAX_SIDE / Math.max(width, height));

    while (true) {
        canvas.width = Math.max(1, Math.round(width * scale));
        canvas.height = Math.max(1, Math.round(height * scale));
        // Fondo blanco: JPEG no tiene transparencia y esas zonas saldrían negras
        context.fillStyle = '#fff';
        context.fillRect(0, 0, canvas.width, canvas.height);
        context.drawImage(image, 0, 0, canvas.width, canvas.height);

        // Baja la calidad poco a poco hasta que el resultado quepa en el límite
        for (const quality of QUALITIES) {
            const data = canvas.toDataURL(OUTPUT_TYPE, quality);
            if (data.length <= MAX_IMAGE_BYTES) {
                return {
                    data,                         // Data URL: "data:image/webp;base64,..."
                    nombreArchivo: file.name,
                    originalSize: file.size       // bytes del archivo original (solo para mostrarlo)
                };
            }
        }

        // Ni con la calidad más baja cupo: se reduce la medida un 20 % y se intenta de nuevo
        scale *= 0.8;
    }
};
