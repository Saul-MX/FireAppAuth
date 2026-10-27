"""Documento B: manual paso a paso del gestor de productos."""
from componentes import (portada, tabla, lista, nota, arbol, codigo, terminal, captura, esc)


def construir(d):
    url, repo, proyecto = d['url_publica'], d['repositorio'], d['proyecto_firebase']
    h = [portada(d, 'ACTIVIDAD COLABORATIVA · GESTOR DE PRODUCTOS', 'Manual paso a paso',
                 'Firebase Authentication, Cloud Firestore y Hosting')]

    # ------------------------------------------------------------ Introducción
    h.append(f"""
<h1 class="first">Introducción</h1>
<p>En esta actividad ampliamos la aplicación de autenticación que vimos en clase (FireApp) para
convertirla en un gestor de productos por usuario. La aplicación usa tres servicios de Firebase:
<b>Authentication</b> para saber quién entró, <b>Cloud Firestore</b> para guardar sus productos y
<b>Firebase Hosting</b> para publicarla en internet.</p>
<p>Este manual explica, paso por paso, cómo quedó construida y cómo se puede reproducir. Cada paso tiene
una explicación breve, capturas del código real del proyecto y, donde corresponde, capturas de las consolas
de Firebase.</p>
{tabla(['Dato', 'Valor'], [
        ['<b>Aplicación publicada</b>', f'<a href="{url}">{url}</a>'],
        ['<b>Repositorio</b>', f'<a href="{repo}">{repo}</a>'],
        ['<b>Proyecto de Firebase</b>', proyecto],
        ['<b>Tecnologías</b>', 'HTML, JavaScript modular (ES modules), Bootstrap 5.3.8 y SDK de Firebase 13.0.0 cargado por CDN'],
        ['<b>Acceso</b>', 'Correo y contraseña, Google, Facebook, GitHub y X'],
    ], chica=True, anchos=['30%', '70%'])}
<h2>Estructura del proyecto</h2>
<p>Cada funcionalidad vive en su propio archivo dentro de la carpeta <code>app/</code>, y
<code>main.js</code> los carga todos:</p>
{tabla(['Archivo', 'Qué hace'], [
        ['<code>main.js</code>', 'Punto de entrada: importa cada módulo y vigila la sesión con <code>onAuthStateChanged</code>.'],
        ['<code>app/firebase.js</code>', 'Configuración e inicialización de Firebase (Authentication y Firestore).'],
        ['<code>app/signupForm.js</code>, <code>signinForm.js</code>', 'Registro e inicio de sesión con correo y contraseña.'],
        ['<code>app/googleLogin.js</code>, <code>facebookLogin.js</code>, <code>githubLogin.js</code>, <code>twitterLogin.js</code>', 'Inicio de sesión con cada proveedor OAuth.'],
        ['<code>app/logout.js</code>', 'Cierre de sesión.'],
        ['<code>app/loginCheck.js</code>', 'Oculta Signin/Signup y muestra el módulo de productos (y al revés).'],
        ['<code>app/authErrors.js</code>, <code>firestoreErrors.js</code>', 'Mensajes de error claros para Authentication y Firestore.'],
        ['<code>app/imagePicker.js</code>', 'Selección, validación (1 a 5) y vista previa de las imágenes.'],
        ['<code>app/imageProcessor.js</code>', 'Redimensiona y comprime cada imagen con canvas y la convierte a Base64.'],
        ['<code>app/productForm.js</code>', 'Formulario de registro y de edición.'],
        ['<code>app/productsDb.js</code>', 'Todas las operaciones con Firestore (crear, leer, editar y eliminar).'],
        ['<code>app/productList.js</code>', 'Lista en tiempo real con imágenes; la limpia al cerrar sesión.'],
        ['<code>app/productDelete.js</code>', 'Confirmación y eliminación de un producto.'],
        ['<code>app/toast.js</code>', 'Avisos breves en pantalla.'],
    ], chica=True, larga=True, anchos=['44%', '56%'])}
""")

    # ------------------------------------------------------------ Desarrollo
    h.append('<h1>Desarrollo</h1>')

    # Paso 1
    h.append(f"""
<h2>Paso 1. Activación de Firestore y estructura de datos</h2>
<h3>Objetivo: crear la base de datos y definir dónde se guarda cada dato</h3>
<p>La base de datos se crea en la consola de Firebase, en <b>Build → Firestore Database → Create database</b>.
Se elige la ubicación de los datos y, en el paso de reglas, el <b>modo de prueba</b> (<i>Start in test mode</i>),
que permite leer y escribir mientras se desarrolla. Al terminar, Firestore queda listo para recibir datos.</p>
{captura('firestore-crear', 'Consola de Firebase → Firestore Database → Create database, con «Start in test mode» seleccionado.', 'Creación de la base de datos de Firestore en modo de prueba.')}
<p>Las reglas del modo de prueba dejan el acceso abierto durante un tiempo limitado. Es suficiente para esta
actividad, pero no es seguro para producción: cualquiera que conozca el proyecto podría leer y modificar los datos.
En la investigación (documento C) se explica qué cambiaría con reglas de seguridad; aquí solo se mencionan y no se
implementan.</p>
{captura('firestore-reglas', 'Firestore Database → pestaña Rules, mostrando las reglas del modo de prueba y su fecha de vencimiento.', 'Reglas del modo de prueba en la consola.')}

<h2>Estructura de datos</h2>
<p>Cada usuario guarda sus productos dentro de su propia ruta, construida con el <b>uid</b> que le asigna
Authentication. Las imágenes van en una subcolección del producto, con un documento por imagen:</p>
{arbol('''users/{uid}/products/{productId}
    nombre, descripcion, precio, categoria, existencias,
    totalImagenes, fechaCreacion, fechaActualizacion

users/{uid}/products/{productId}/images/{imageId}
    data (Base64), nombreArchivo, orden''')}
{tabla(['Campo', 'Tipo', 'Descripción'], [
        ['<code>nombre</code>', 'string', 'Nombre del producto (máximo 80 caracteres).'],
        ['<code>descripcion</code>', 'string', 'Descripción (máximo 500 caracteres).'],
        ['<code>precio</code>', 'number', 'Precio en pesos, redondeado a centavos.'],
        ['<code>categoria</code>', 'string', 'Una de las categorías del formulario.'],
        ['<code>existencias</code>', 'number', 'Número entero igual o mayor a 0.'],
        ['<code>totalImagenes</code>', 'number', 'Cantidad de imágenes (de 1 a 5); evita leer la subcolección solo para contarlas.'],
        ['<code>fechaCreacion</code>, <code>fechaActualizacion</code>', 'timestamp', 'Se escriben con <code>serverTimestamp()</code>.'],
        ['<code>data</code> (imagen)', 'string', 'Data URL en Base64 de la imagen ya comprimida (máximo 300 KB).'],
        ['<code>nombreArchivo</code> (imagen)', 'string', 'Nombre original del archivo.'],
        ['<code>orden</code> (imagen)', 'number', 'Posición de la imagen; 0 es la portada.'],
    ], chica=True, anchos=['34%', '14%', '52%'])}
<p><b>¿Por qué una subcolección para las imágenes?</b> Firestore limita cada documento a 1 MiB. Si las cinco
imágenes fueran un campo del producto, un solo documento podría acercarse a ese límite y, además, escuchar la lista
de productos descargaría todas las imágenes. Con una subcolección cada imagen es un documento independiente
(de unos 300 KB como máximo) y la lista de productos se mantiene ligera.</p>
{codigo('app/firebase.js', (1, 22), 'Inicialización de Firebase: Authentication y Firestore (getFirestore).')}
{captura('firestore-estructura', 'Firestore Database → Data: users → {uid} → products → {id} → images, con los campos de cada documento visibles.', 'Datos guardados: producto y subcolección images.')}
""")

    # Paso 2
    h.append(f"""
<h2 class="paso">Paso 2. Formulario y validación de imágenes</h2>
<h3>Objetivo: capturar los datos del producto y validar de 1 a 5 imágenes antes de guardar</h3>
<p>El formulario es una ventana modal de Bootstrap con nombre, descripción, precio, categoría y existencias. Todos
son obligatorios y llevan restricciones de HTML (<code>required</code>, <code>min</code>, <code>maxlength</code>).
Las imágenes se eligen con un <code>input type="file"</code> con <code>multiple</code> y
<code>accept="image/*"</code>, dentro de una zona donde también se pueden arrastrar archivos.</p>
{codigo('index.html', (340, 356), 'Campos del formulario de productos.')}
{codigo('index.html', (384, 397), 'Zona de selección de imágenes, mensaje de error y vista previa.')}

<h2>Reglas de validación</h2>
{tabla(['Regla', 'Valor', 'Mensaje cuando no se cumple'], [
        ['Cantidad', 'De 1 a 5 imágenes', '«Agrega al menos 1 imagen del producto.» / «Puedes subir máximo 5 imágenes por producto…»'],
        ['Tipo de archivo', 'Solo <code>image/*</code>', '«Solo se permiten imágenes: …no es una imagen.»'],
        ['Peso del original', 'Máximo 10 MB cada una', '«Cada imagen debe pesar máximo 10 MB…»'],
        ['Peso guardado', 'Máximo 300 KB (Base64)', 'No hay mensaje: la imagen se reduce automáticamente (paso 3).'],
    ], chica=True, anchos=['20%', '27%', '53%'])}
<p>La validación ocurre en dos momentos. Al <b>elegir los archivos</b>, <code>validateFiles</code> revisa el tipo, el
peso y que, sumando las que ya estaban, no se pase de 5; si un archivo no cumple, no se agrega ninguno y se explica el
motivo. Al <b>guardar</b>, <code>validateImageCount</code> comprueba que haya entre 1 y 5, así que subir 0 o más de 5
siempre muestra un mensaje claro. Cada imagen aceptada aparece con su vista previa, su peso antes y después de
comprimirla y un botón para quitarla; la primera es la portada.</p>
{codigo('app/imagePicker.js', (91, 118), 'validateFiles: tipo, peso y cantidad al elegir los archivos.')}
{codigo('app/imagePicker.js', (204, 214), 'validateImageCount: mínimo 1 y máximo 5 antes de guardar.')}
{captura('app-validacion-max', 'La aplicación mostrando el mensaje de error al seleccionar más de 5 imágenes (por ejemplo, 6).', 'Error al pasarse del máximo de 5 imágenes.')}
{captura('app-vista-previa', 'El formulario con varias imágenes cargadas: contador (por ejemplo 3 / 5), vista previa, peso y etiqueta «Portada».', 'Vista previa de las imágenes antes de guardar.')}
{nota('Esta validación sirve para dar respuesta inmediata al usuario, pero no sustituye a una validación en el servidor: '
      'un usuario con conocimientos podría saltarse el navegador. Se explica en el documento C.', 'Importante')}
""")

    # Paso 3
    h.append(f"""
<h2 class="paso">Paso 3. Procesamiento y guardado de imágenes</h2>
<h3>Objetivo: reducir cada imagen en el navegador y guardarla como Base64 en Firestore</h3>
<p>Antes de guardarse, cada imagen pasa por <code>imageProcessor.js</code>, que trabaja en tres etapas:</p>
{lista([
        '<b>Lectura.</b> <code>FileReader</code> lee el archivo como Data URL y se carga en un <code>&lt;img&gt;</code>.',
        '<b>Redimensionado.</b> Se dibuja en un <code>&lt;canvas&gt;</code> con el lado más largo de 800 px como máximo (nunca se agranda).',
        '<b>Compresión.</b> <code>canvas.toDataURL()</code> la exporta en WebP (o JPEG si el navegador no lo soporta) probando calidades de 0.8 a 0.4 hasta que el texto Base64 mida 300 KB o menos; si ni así cabe, reduce las dimensiones 20 % y repite.',
    ], ordenada=True)}
{codigo('app/imageProcessor.js', (1, 16), 'Límites y formato de salida (WebP con respaldo a JPEG).')}
{codigo('app/imageProcessor.js', (34, 68), 'processImage: redimensiona y comprime hasta cumplir el límite.')}
<p>Base64 aumenta el tamaño aproximadamente un tercio (3 bytes se escriben con 4 caracteres). Por eso el límite de
300 KB se mide sobre el texto ya codificado: 300 KB de Base64 equivalen a unos 225 KB de imagen real, muy por debajo del
límite de 1 MiB por documento.</p>

<h2>Guardado en Firestore</h2>
<p><code>createProduct</code> usa un <b>lote</b> (<code>writeBatch</code>): el producto y cada una de sus imágenes se
escriben juntos, así que o se guarda todo o no se guarda nada y nunca queda un producto sin imágenes.
<code>doc()</code> sin identificador genera uno automático; cada imagen es un documento de la subcolección
<code>images</code> con su <code>orden</code> (0 es la portada).</p>
{codigo('app/productsDb.js', [(13, 15), (36, 57)], 'createProduct: producto e imágenes en un solo lote.')}
{codigo('app/productForm.js', (117, 147), 'Envío del formulario: valida los campos, valida las imágenes y guarda con el uid del usuario.')}
{captura('firestore-imagenes', 'Firestore → un documento de la subcolección images abierto, con los campos data (Base64), nombreArchivo y orden.', 'Una imagen guardada como documento de la subcolección images.')}
""")

    # Paso 4
    h.append(f"""
<h2 class="paso">Paso 4. Lectura, edición y eliminación filtrando por uid</h2>
<h3>Objetivo: que cada usuario vea y administre solo sus propios productos</h3>
<p>El filtro por usuario se logra desde el código: todas las rutas se construyen con el uid del usuario autenticado
(<code>auth.currentUser.uid</code>) y la aplicación solo consulta <code>users/{{uid}}/products</code>. Nunca consulta
la colección de otro usuario.</p>
<h2>Lectura</h2>
<p><code>listenProducts</code> usa <code>onSnapshot</code> sobre una consulta ordenada con <code>orderBy</code>: la lista
se actualiza en tiempo real cuando se crea, edita o elimina un producto, sin recargar la página.
<code>getProductImages</code> usa <code>getDocs</code> (lectura única) para traer las imágenes de cada producto, y
<code>productList.js</code> guarda en caché las que ya leyó, comparando <code>fechaActualizacion</code>, para ahorrar
lecturas de la cuota gratuita.</p>
{codigo('app/productsDb.js', [(13, 15), (24, 34)], 'Rutas por uid, escucha en tiempo real y lectura de imágenes.')}
{codigo('app/productList.js', (174, 196), 'showProducts: empieza a escuchar users/{uid}/products del usuario con sesión.')}
{captura('app-lista', 'La sección «Mis productos» con las tarjetas: imagen principal, miniaturas, categoría, existencias, precio y botones Editar y Eliminar.', 'Listado de productos con sus imágenes.')}

<h2>Edición</h2>
<p>Al pulsar <b>Editar</b>, el formulario se abre con los datos del producto y sus imágenes guardadas (leídas con
<code>getDocs</code>). <code>updateProduct</code> actualiza el producto y sincroniza las imágenes en un solo lote: borra
las que se quitaron, reordena las que se conservaron y agrega las nuevas.</p>
{codigo('app/productsDb.js', (59, 84), 'updateProduct: actualiza el producto y sincroniza sus imágenes.')}

<h2>Eliminación</h2>
<p>Firestore <b>no borra las subcolecciones</b> al eliminar un documento. Por eso <code>deleteProduct</code> primero lee
las imágenes y las elimina en el mismo lote que el producto; así no quedan imágenes huérfanas. Antes se pide
confirmación al usuario.</p>
{codigo('app/productsDb.js', (86, 97), 'deleteProduct: elimina las imágenes y el producto.')}
{codigo('app/productDelete.js', (32, 48), 'Confirmación de eliminación usando el uid del usuario autenticado.')}

<h2>Cierre de sesión: no quedan productos del usuario anterior</h2>
<p><code>main.js</code> vigila la sesión con <code>onAuthStateChanged</code>. Con sesión llama a
<code>showProducts(user)</code>; sin sesión llama a <code>clearProducts()</code>, que detiene la escucha de Firestore,
vacía la lista y la caché, y cierra el formulario y los diálogos. <code>loginCheck.js</code> oculta Signin/Signup y
muestra el módulo de productos al entrar, y hace lo contrario al salir.</p>
{codigo('main.js', (19, 30), 'onAuthStateChanged: muestra los productos del usuario o limpia la pantalla.')}
{codigo('app/productList.js', (198, 214), 'clearProducts: detiene la escucha y borra todo lo del usuario anterior.')}
{codigo('app/loginCheck.js', (6, 16), 'Muestra u oculta las secciones según haya sesión.')}
{captura('firestore-dos-usuarios', 'Firestore → colección users con al menos dos uid distintos, cada uno con su propia subcolección products.', 'Cada usuario tiene sus productos bajo su propio uid.')}
""")

    # Paso 5
    h.append(f"""
<h2 class="paso">Paso 5. Firebase CLI, firebase init hosting y firebase deploy</h2>
<h3>Objetivo: publicar la aplicación en {url}</h3>
<p>Firebase Hosting sirve los archivos del proyecto desde internet con HTTPS. Se publica desde la terminal con
Firebase CLI:</p>
{lista([
        '<b>Instalar Node.js</b> (incluye <code>npm</code>) y comprobarlo con <code>node --version</code>.',
        '<b>Instalar Firebase CLI:</b> <code>npm install -g firebase-tools</code> y comprobar con <code>firebase --version</code>.',
        '<b>Iniciar sesión:</b> <code>firebase login</code> abre el navegador para autenticarse con la cuenta de Google dueña del proyecto.',
        '<b>Inicializar Hosting</b> desde la carpeta del proyecto: <code>firebase init hosting</code>.',
        '<b>Publicar:</b> <code>firebase deploy --only hosting</code>.',
    ], ordenada=True)}
{terminal([
        '$ npm install -g firebase-tools',
        '$ firebase --version',
        '$ firebase login',
        '$ firebase init hosting',
        '$ firebase deploy --only hosting',
        '',
        '=== Deploying to \'' + proyecto + '\'...',
        '✔  hosting[' + proyecto + ']: release complete',
        '✔  Deploy complete!',
        'Hosting URL: ' + url,
    ], 'Comandos de Firebase CLI y resultado esperado del deploy.')}
{captura('cli-instalacion', 'La terminal con firebase --version y firebase login completado.', 'Instalación de Firebase CLI e inicio de sesión.')}
<p>Al ejecutar <code>firebase init hosting</code> la CLI hace estas preguntas; en nuestro caso las respuestas fueron:</p>
{tabla(['Pregunta de la CLI', 'Respuesta'], [
        ['Please select an option', 'Use an existing project → <code>' + proyecto + '</code>'],
        ['What do you want to use as your public directory?', '<code>.</code> (el <code>index.html</code> está en la raíz del proyecto; la CLI propone <code>public</code> por defecto)'],
        ['Configure as a single-page app?', 'No'],
        ['Set up automatic builds and deploys with GitHub?', 'No'],
    ], chica=True, anchos=['50%', '50%'])}
{captura('cli-init', 'La terminal ejecutando firebase init hosting con las preguntas y respuestas.', 'Inicialización de Hosting con firebase init hosting.')}
<p>La CLI genera dos archivos: <code>firebase.json</code>, con la configuración de Hosting, y
<code>.firebaserc</code>, que guarda el proyecto por defecto. En <code>firebase.json</code>, <code>public</code> es la
carpeta que se publica (aquí la raíz), <code>ignore</code> evita subir archivos que no deben ser públicos
(<code>firebase.json</code>, archivos ocultos, <code>node_modules</code>, registros y los PDF de la carpeta
<code>entregables</code>) y <code>headers</code> con <code>Cache-Control: no-cache</code> hace que el navegador revise
siempre si hay una versión nueva.</p>
{codigo('firebase.json', (1, 24), 'Configuración de Firebase Hosting.')}
{codigo('.firebaserc', (1, 5), 'Proyecto de Firebase asociado a la carpeta.')}
{captura('cli-deploy', 'La terminal al terminar firebase deploy --only hosting, con «Deploy complete!» y la Hosting URL.', 'Despliegue terminado con la URL pública.')}
<h2>Verificación en la consola y versiones</h2>
<p>En <b>Build → Hosting</b> aparece el dominio publicado y el <i>Release history</i>. Cada <code>deploy</code> crea una
versión nueva; si algo sale mal, la opción <b>Roll back</b> vuelve a servir una versión anterior.</p>
{captura('hosting-panel', 'Consola de Firebase → Hosting: dominios .web.app y .firebaseapp.com y la tabla Release history.', 'Panel de Hosting con la versión publicada.')}
{captura('app-publicada', 'El navegador abriendo la URL pública https://' + proyecto + '.web.app con la aplicación funcionando (se ve el candado de HTTPS).', 'La aplicación publicada en Internet.')}
""")

    # Paso 6
    h.append(f"""
<h2 class="paso">Paso 6. Verificación de dominios autorizados</h2>
<h3>Objetivo: comprobar que el inicio de sesión funciona desde el sitio publicado</h3>
<p>Google, Facebook, GitHub y X abren una ventana emergente (<code>signInWithPopup</code>). Firebase solo permite
hacerlo desde los <b>dominios autorizados</b> del proyecto: si el dominio desde el que se abre la aplicación no está
en la lista, el inicio de sesión falla con el error <code>auth/unauthorized-domain</code>. Por eso, después de
publicar, hay que revisarlos:</p>
{lista([
        'Abrir <b>Authentication → Settings → Authorized domains</b> en la consola de Firebase.',
        'Comprobar que estén <b>' + proyecto + '.web.app</b> y <b>' + proyecto + '.firebaseapp.com</b>. Normalmente ya vienen incluidos; si falta alguno, usar <b>Add domain</b>.',
        '<code>localhost</code> solo se necesita para probar en la computadora; en proyectos creados después del 28 de abril de 2025 no se agrega por defecto.',
        'Abrir <b>Authentication → Sign-in method</b> y confirmar que estén habilitados Correo/Contraseña, Google, Facebook, GitHub y X.',
        'En las consolas de Facebook, GitHub y X debe estar registrada la URI de redirección que muestra Firebase: <code>https://' + proyecto + '.firebaseapp.com/__/auth/handler</code> (es el <code>authDomain</code> de <code>app/firebase.js</code>).',
        'Probar desde la URL pública al menos dos proveedores.',
    ], ordenada=True)}
{captura('auth-dominios', 'Authentication → Settings → Authorized domains, mostrando ' + proyecto + '.web.app y ' + proyecto + '.firebaseapp.com.', 'Dominios autorizados del proyecto.')}
{captura('auth-proveedores', 'Authentication → Sign-in method, con los proveedores habilitados (Correo, Google, Facebook, GitHub y X).', 'Proveedores de inicio de sesión habilitados.')}
{nota('Una app de Facebook en modo de desarrollo solo deja entrar a cuentas con algún rol en la app (administrador, '
      'desarrollador o probador). Para la demostración conviene agregar como probador a la persona que inicie sesión '
      'o usar proveedores que ya se hayan probado.', 'Antes de la demostración')}
<h2>Lista de verificación posterior a la publicación</h2>
{tabla(['Comprobación', 'Resultado'], [
        ['☐ La URL pública abre con HTTPS y se ve la pantalla de bienvenida', ''],
        ['☐ Inicio de sesión con correo y contraseña', ''],
        ['☐ Inicio de sesión con Google', ''],
        ['☐ Inicio de sesión con al menos otro proveedor (Facebook, GitHub o X)', ''],
        ['☐ Crear un producto con 1 imagen y con 5 imágenes', ''],
        ['☐ Error claro al intentar subir 0 imágenes y más de 5', ''],
        ['☐ Editar y eliminar un producto (se eliminan también sus imágenes)', ''],
        ['☐ Cerrar sesión, entrar con otro usuario y no ver los productos del anterior', ''],
    ], chica=True, anchos=['75%', '25%'])}
""")

    # Anexo
    h.append(f"""
<h2 class="paso">Anexo. Guía para la demostración</h2>
<h3>Por qué esta solución es válida para un proyecto escolar y por qué en producción se usaría Cloud Storage</h3>
<p>Firestore es una base de datos de documentos: no está pensada para guardar archivos y cada documento tiene un límite
de 1 MiB. El servicio diseñado para archivos es Cloud Storage for Firebase, pero desde el 3 de febrero de 2026 exige el
plan Blaze, que se vincula a una cuenta de facturación. Para que nadie necesite tarjeta, guardamos imágenes pequeñas en
Base64 dentro de Firestore, que funciona en el plan gratuito.</p>
{tabla(['', 'Firestore + Base64 (esta actividad)', 'Cloud Storage (producción)'], [
        ['<b>Plan</b>', 'Spark (sin costo, sin método de pago).', 'Blaze (pago por uso, con cuenta de facturación).'],
        ['<b>Tamaño</b>', 'Cada imagen se reduce a 800 px y 300 KB como máximo para no acercarse al límite de 1 MiB por documento.', 'Pensado para archivos grandes: se pueden guardar las fotos originales.'],
        ['<b>Peso real</b>', 'Base64 agrega aproximadamente un tercio al tamaño.', 'Se guarda el archivo binario tal cual.'],
        ['<b>Entrega</b>', 'La imagen viaja dentro del documento y cada lectura de producto o imagen cuenta contra la cuota.', 'Cada archivo tiene su propia URL y se sirve de forma eficiente.'],
        ['<b>Escalabilidad</b>', 'Válida para pocas imágenes pequeñas; no escala bien.', 'Escala a miles de archivos y usuarios.'],
    ], chica=True, anchos=['16%', '42%', '42%'])}
<h2>Flujo de la demostración</h2>
<p>La demostración es en vivo, con la URL pública de Hosting (no desde localhost), y participan los dos integrantes.</p>
{tabla(['#', 'Qué se muestra', 'Responsable'], [
        ['1', 'Inicio de sesión con al menos dos proveedores.', ''],
        ['2', 'Creación de un producto con imágenes: el mínimo (1), el máximo (5) y el error al pasarse de 5.', ''],
        ['3', 'Edición y eliminación de un producto.', ''],
        ['4', 'Cierre de sesión y acceso con otro usuario, comprobando que no aparecen los productos del anterior.', ''],
        ['5', 'Consola de Firestore con los datos guardados.', ''],
    ], chica=True, anchos=['6%', '70%', '24%'])}

<h1>Conclusiones</h1>
<p>Con este trabajo convertimos una aplicación que solo iniciaba sesión en un gestor de productos completo y publicado
en internet. Lo más importante fue entender cómo se conectan los tres servicios: Authentication identifica a la persona,
el uid se usa para armar la ruta <code>users/{{uid}}/products</code> y Firestore guarda ahí la información de cada usuario.</p>
<p>También aprendimos las limitaciones de las decisiones que tomamos. Guardar imágenes en Base64 dentro de Firestore es
una solución práctica para un proyecto escolar, pero obliga a reducirlas y a cuidar el límite de 1 MiB; en un proyecto
real se usaría Cloud Storage. Del mismo modo, el modo de prueba es cómodo para desarrollar, pero deja los datos abiertos,
y en producción habría que protegerlos con reglas de seguridad y con validación también en el servidor.</p>
<p>Por último, publicar con Firebase Hosting nos mostró que terminar el código no es terminar el proyecto: hubo que
instalar la CLI, desplegar, revisar los dominios autorizados de los proveedores y probar todo desde la URL pública. Dejar
cada funcionalidad en su propio archivo y comentada nos facilitó repartir el trabajo y explicarlo en la demostración.</p>
""")
    return ''.join(h)
