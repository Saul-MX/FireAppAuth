"""Documento C: investigación de conceptos (3 a 5 cuartillas) con fuentes citadas en APA."""
import re
from componentes import portada, esc

# clave: (autor, año, título, url).  Las letras s. f.-a, s. f.-b… se asignan solas por orden alfabético del título.
REFS = {
    'fs_overview': ('Firebase', 's. f.', 'Cloud Firestore', 'https://firebase.google.com/docs/firestore'),
    'fs_model': ('Firebase', 's. f.', 'Cloud Firestore data model', 'https://firebase.google.com/docs/firestore/data-model'),
    'fs_struct': ('Firebase', 's. f.', 'Choose a data structure', 'https://firebase.google.com/docs/firestore/manage-data/structure-data'),
    'fs_add': ('Firebase', 's. f.', 'Add data to Cloud Firestore', 'https://firebase.google.com/docs/firestore/manage-data/add-data'),
    'fs_get': ('Firebase', 's. f.', 'Get data with Cloud Firestore', 'https://firebase.google.com/docs/firestore/query-data/get-data'),
    'fs_listen': ('Firebase', 's. f.', 'Get realtime updates with Cloud Firestore', 'https://firebase.google.com/docs/firestore/query-data/listen'),
    'fs_rules_start': ('Firebase', 's. f.', 'Get started with Cloud Firestore Security Rules', 'https://firebase.google.com/docs/firestore/security/get-started'),
    'fs_rules_cond': ('Firebase', 's. f.', 'Writing conditions for Cloud Firestore Security Rules', 'https://firebase.google.com/docs/firestore/security/rules-conditions'),
    'fs_quick': ('Firebase', 's. f.', 'Get started with Cloud Firestore', 'https://firebase.google.com/docs/firestore/quickstart'),
    'fs_quotas': ('Firebase', 's. f.', 'Usage and limits', 'https://firebase.google.com/docs/firestore/quotas'),
    'fs_billing': ('Firebase', 's. f.', 'Understand Cloud Firestore billing', 'https://firebase.google.com/docs/firestore/pricing'),
    'pricing': ('Firebase', 's. f.', 'Firebase Pricing', 'https://firebase.google.com/pricing'),
    'storage_faq': ('Firebase', 's. f.', 'FAQs about Cloud Storage for Firebase changes announced in September 2024', 'https://firebase.google.com/docs/storage/faqs-storage-changes-announced-sept-2024'),
    'hosting': ('Firebase', 's. f.', 'Firebase Hosting', 'https://firebase.google.com/docs/hosting'),
    'hosting_qs': ('Firebase', 's. f.', 'Get started with Firebase Hosting', 'https://firebase.google.com/docs/hosting/quickstart'),
    'hosting_cfg': ('Firebase', 's. f.', 'Configure Hosting behavior', 'https://firebase.google.com/docs/hosting/full-config'),
    'hosting_manage': ('Firebase', 's. f.', 'Manage live & preview channels, releases, and versions', 'https://firebase.google.com/docs/hosting/manage-hosting-resources'),
    'auth_faq': ('Firebase', 's. f.', 'Authentication FAQ and troubleshooting', 'https://firebase.google.com/docs/auth/faq-and-troubleshooting'),
    'auth_redirect': ('Firebase', 's. f.', 'Best practices for using signInWithRedirect on browsers that block third-party storage access', 'https://firebase.google.com/docs/auth/web/redirect-best-practices'),
    'api_keys': ('Firebase', 's. f.', 'Learn about using and managing API keys for Firebase', 'https://firebase.google.com/docs/projects/api-keys'),
    'privacy': ('Firebase', 's. f.', 'Privacy and Security in Firebase', 'https://firebase.google.com/support/privacy'),
    'mdn_input': ('MDN Web Docs', 's. f.', '<input type="file">', 'https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/file'),
    'mdn_reader': ('MDN Web Docs', 's. f.', 'FileReader: readAsDataURL() method', 'https://developer.mozilla.org/en-US/docs/Web/API/FileReader/readAsDataURL'),
    'mdn_b64': ('MDN Web Docs', 's. f.', 'Base64', 'https://developer.mozilla.org/en-US/docs/Glossary/Base64'),
    'mdn_canvas': ('MDN Web Docs', 's. f.', 'HTMLCanvasElement: toDataURL() method', 'https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toDataURL'),
    'mdn_img': ('MDN Web Docs', 's. f.', 'Image file type and format guide', 'https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Image_types'),
    'owasp': ('OWASP Foundation', 's. f.', 'Input Validation Cheat Sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html'),
    'progit': ('Chacon, S. y Straub, B', '2014', 'Pro Git (2.ª ed.): Git Branching - Basic Branching and Merging', 'https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging'),
    'gh_pr': ('GitHub', 's. f.', 'Acerca de las solicitudes de cambios', 'https://docs.github.com/es/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests'),
    'gh_ignore': ('GitHub', 's. f.', 'Ignorar archivos', 'https://docs.github.com/es/get-started/git-basics/ignoring-files'),
    'ey': ('EY México', 's. f.', 'Nueva Ley Federal de Protección de Datos Personales en Posesión de los Particulares', 'https://www.ey.com/es_mx/technical/tax/boletines-fiscales/nueva-ley-federal-proteccion-datos-personal-posesion-particulares'),
}


def _sufijos(claves):
    """Asigna -a, -b… a las fuentes citadas del mismo autor y año, según el orden alfabético del título."""
    grupos = {}
    for clave in claves:
        autor, anio, titulo, _ = REFS[clave]
        grupos.setdefault((autor, anio), []).append((titulo.lower(), clave))
    sufijo = {}
    for (autor, anio), items in grupos.items():
        items.sort()
        for i, (_, clave) in enumerate(items):
            sufijo[clave] = f'-{chr(97 + i)}' if len(items) > 1 else ''
    return sufijo


SUFIJO = {}
USADAS = []
EN_TEXTO = {'Chacon, S. y Straub, B': 'Chacon y Straub'}


def c(*claves):
    """Cita en el texto: (Firebase, s. f.-a, s. f.-c; MDN Web Docs, s. f.)."""
    grupos = []
    for clave in claves:
        if clave not in USADAS:
            USADAS.append(clave)
        autor, anio, _, _ = REFS[clave]
        autor = EN_TEXTO.get(autor, autor)   # en el texto solo apellidos: (Chacon y Straub, 2014)
        etiqueta = f'{anio}{SUFIJO[clave]}'
        if grupos and grupos[-1][0] == autor:
            grupos[-1][1].append(etiqueta)
        else:
            grupos.append((autor, [etiqueta]))
    return '(' + '; '.join(f'{a}, {", ".join(e)}' for a, e in grupos) + ')'


def referencias():
    filas = []
    for clave in USADAS:
        autor, anio, titulo, url = REFS[clave]
        filas.append((autor.lower(), titulo.lower(), clave))
    filas.sort()
    html = ''
    for _, _, clave in filas:
        autor, anio, titulo, url = REFS[clave]
        html += (f'<p class="ref">{esc(autor)}. ({anio}{SUFIJO[clave]}). <i>{esc(titulo)}</i>. '
                 f'Recuperado el 27 de octubre de 2026, de <a href="{url}">{esc(url)}</a></p>')
    return html


def construir(d):
    """Dos pasadas: la primera descubre qué fuentes se citan; la segunda asigna las letras (s. f.-a…)."""
    USADAS.clear()
    SUFIJO.clear()
    SUFIJO.update(_sufijos(REFS))
    _cuerpo(d)
    citadas = list(USADAS)
    USADAS.clear()
    SUFIJO.clear()
    SUFIJO.update(_sufijos(citadas))
    html = _cuerpo(d)
    sin_citar = [k for k in REFS if k not in USADAS]
    if sin_citar:
        print('  AVISO: fuentes definidas pero no citadas en el texto:', sin_citar)
    return html


def _cuerpo(d):
    P = d['proyecto_firebase']
    cuerpo = portada(d, 'ACTIVIDAD COLABORATIVA · GESTOR DE PRODUCTOS', 'Investigación de conceptos',
                     'Firebase, Firestore y almacenamiento de datos', extra_url=False)

    cuerpo += f"""
<h1 class="first">Introducción</h1>
<p>Para construir el gestor de productos tuvimos que entender conceptos que no se ven cuando solo se escribe código.
Esta investigación reúne los dieciséis temas de la actividad, agrupados en seis bloques. Cada afirmación se apoya en
documentación oficial, citada con formato APA y listada al final.</p>

<h1>Desarrollo</h1>
<h2>1. Datos en Cloud Firestore</h2>
<p><b>Cloud Firestore.</b> Es una base de datos NoSQL alojada en la nube a la que las aplicaciones acceden directamente
{c('fs_overview')}. Guarda la información en documentos, con campos y valores, agrupados en colecciones; una colección
solo contiene documentos y estos pueden tener subcolecciones {c('fs_model')}. A diferencia de una base relacional, no hay
tablas con columnas fijas ni uniones (<i>joins</i>): cada documento puede tener su propia forma y las relaciones se
expresan con la ruta o con referencias.</p>
<p><b>Modelado de datos.</b> Hay tres opciones: anidar datos en el documento (sencillo, pero poco escalable si crecen),
usar subcolecciones (el documento padre no crece aunque la lista crezca, pero eliminarlas no es fácil) y usar colecciones
raíz (útiles en relaciones de muchos a muchos) {c('fs_struct')}. Elegimos subcolecciones para las imágenes porque pueden
multiplicarse y así cada una queda lejos del límite por documento.</p>
<p><b>Operaciones CRUD.</b> <code>collection()</code> y <code>doc()</code> crean referencias; <code>addDoc</code> crea un
documento con identificador automático y <code>setDoc</code> lo crea o reemplaza con un identificador elegido
{c('fs_add')}; <code>updateDoc</code> modifica solo los campos indicados y <code>deleteDoc</code> elimina. Para leer,
<code>getDoc</code> y <code>getDocs</code> traen los datos una vez, y <code>query</code> con <code>where</code> y
<code>orderBy</code> filtra y ordena {c('fs_get')}. Nosotros agrupamos las escrituras con <code>writeBatch</code> para que
se hagan todas o ninguna.</p>

<h2>2. Tiempo real y usuarios</h2>
<p><b>onSnapshot frente a lecturas únicas.</b> Una lectura única obtiene los datos una sola vez; <code>onSnapshot</code>
registra un oyente que recibe un primer <i>snapshot</i> y otro cada vez que los datos cambian {c('fs_get', 'fs_listen')}.
Las escrituras locales lo activan de inmediato y <code>hasPendingWrites</code> indica que aún no llegan al servidor
{c('fs_listen')}. Con oyentes se cobra una lectura cada vez que un documento del resultado se agrega o modifica
{c('fs_billing')}. Usamos <code>onSnapshot</code> para la lista de productos y <code>getDocs</code> para las imágenes.</p>
<p><b>uid y datos por usuario.</b> Authentication asigna a cada cuenta un identificador único, el uid. Lo usamos para
armar la ruta <code>users/{{uid}}/products</code>, de modo que la aplicación solo consulta los datos de quien inició
sesión. Esto organiza la información, pero no la protege: con reglas abiertas cualquiera podría pedir otra ruta. La
protección real son las reglas, que comparan <code>request.auth.uid</code> con el uid de la ruta {c('fs_rules_cond')}.</p>

<h2>3. Seguridad, límites y almacenamiento</h2>
<p><b>Modo de prueba.</b> Sirve para empezar con las bibliotecas web y móviles, pero permite que cualquiera lea y
sobrescriba los datos {c('fs_quick')}. Equivale a la regla <code>allow read, write: if true</code>, que la documentación
advierte que nunca debe usarse en producción {c('fs_rules_start')}; además, la consola le agrega una fecha de vencimiento
(30 días) y después se rechazan las solicitudes. Con reglas de seguridad se pasaría de «cualquiera» a «solo el dueño»:
<code>request.auth != null &amp;&amp; request.auth.uid == userId</code> {c('fs_rules_cond')}. Es solo teoría; no lo
implementamos.</p>
<p><b>Límites y cuotas.</b> Un documento puede pesar hasta 1 MiB; la cuota gratuita diaria incluye 50,000 lecturas,
20,000 escrituras y 20,000 eliminaciones, además de 1 GiB de almacenamiento {c('fs_quotas')}. El plan Spark no tiene costo
ni pide método de pago; Blaze cobra por uso e incluye lo gratuito de Spark {c('pricing')}. Cada documento leído, escrito
o eliminado consume cuota, y una consulta cuenta al menos una lectura aunque no devuelva resultados {c('fs_billing')}; por
eso guardamos en memoria las imágenes ya leídas.</p>
<p><b>Cloud Storage frente a Firestore.</b> Firestore está optimizado para muchos documentos pequeños {c('fs_model')}; los
archivos van en Cloud Storage, que desde el 3 de febrero de 2026 exige el plan Blaze, incluso para el bucket
predeterminado {c('storage_faq')}. Guardar archivos grandes en una base de datos choca con el límite de 1 MiB y encarece
cada lectura. Por eso en este proyecto escolar usamos Base64 en Firestore, y en producción usaríamos Storage.</p>

<h2>4. Archivos en el navegador</h2>
<p><b>File API, FileReader, Data URL y Base64.</b> Un <code>input type="file"</code> con <code>multiple</code> devuelve una
<code>FileList</code> de objetos <code>File</code> con nombre, tamaño y tipo {c('mdn_input')}.
<code>FileReader.readAsDataURL()</code> lee un archivo y entrega una Data URL con los datos en Base64 {c('mdn_reader')}.
Base64 escribe 3 bytes con 4 caracteres, así que el resultado pesa aproximadamente un tercio más {c('mdn_b64')}: 300 KB de
texto son unos 225 KB de imagen.</p>
<p><b>Compresión y redimensionado con canvas.</b> <code>canvas.toDataURL(tipo, calidad)</code> exporta el dibujo; la
calidad (de 0 a 1) aplica a JPEG y WebP, y si el navegador no soporta el tipo pedido devuelve PNG {c('mdn_canvas')}. JPEG
comprime con pérdida y es adecuado para fotografías, pero no admite transparencia; PNG es sin pérdida y sí la admite; WebP
puede ser con o sin pérdida y, en promedio, es entre 25 % y 35 % más pequeño que un JPEG de calidad visual similar
{c('mdn_img')}. Redimensionamos a 800 px y bajamos la calidad hasta cumplir 300 KB.</p>
<p><b>Validación en el cliente.</b> Validamos cantidad (1 a 5), tipo y peso antes de guardar. Sin embargo, el atributo
<code>accept</code> solo sugiere tipos y no los valida {c('mdn_input')}, y OWASP indica que la validación del navegador
puede eludirse y debe repetirse en el servidor {c('owasp')}. Un usuario avanzado podría escribir directo en Firestore; en
un sistema real habría que validar también con reglas de seguridad o funciones en la nube.</p>

<h2>5. Publicación</h2>
<p><b>Firebase Hosting.</b> Está optimizado para aplicaciones web estáticas y de una sola página; sirve el contenido desde
una CDN global, incluye SSL sin configuración (HTTPS automático) y permite revertir con un clic {c('hosting')}. Cada
<code>deploy</code> crea una versión, y un <i>rollback</i> crea un nuevo lanzamiento que sirve la versión anterior
{c('hosting_manage')}. El sitio queda en <code>{P}.web.app</code> y <code>{P}.firebaseapp.com</code> {c('hosting_qs')}.</p>
<p><b>Firebase CLI.</b> <code>firebase login</code> autentica la cuenta de Google. Después,
<code>firebase init hosting</code> pregunta el proyecto y la carpeta pública (por defecto <code>public</code>) y genera
<code>firebase.json</code> y <code>.firebaserc</code>, y <code>firebase deploy --only hosting</code> publica
{c('hosting_qs')}. En <code>firebase.json</code>, <code>public</code>
indica la carpeta que se despliega e <code>ignore</code> excluye archivos, por defecto el propio <code>firebase.json</code>,
los archivos ocultos y <code>node_modules</code> {c('hosting_cfg')}. Nuestro proyecto usa <code>"."</code> porque el
<code>index.html</code> está en la raíz.</p>
<p><b>Dominios autorizados.</b> Los proveedores OAuth abren una ventana desde el dominio de la aplicación, y ese dominio
debe estar en <i>Authentication → Settings → Authorized domains</i>, donde figuran <code>{P}.firebaseapp.com</code> y
<code>{P}.web.app</code>; <code>localhost</code> ya no se agrega por defecto en proyectos nuevos {c('auth_faq')}. Además,
Facebook, GitHub y X necesitan registrar la URI de redirección <code>https://&lt;authDomain&gt;/__/auth/handler</code>
{c('auth_redirect')}. Si falta alguno, tras publicar el sitio el inicio de sesión falla con
<code>auth/unauthorized-domain</code>.</p>

<h2>6. Colaboración y privacidad</h2>
<p><b>Trabajo colaborativo con Git.</b> Una rama aísla el trabajo de cada integrante (<code>git checkout -b</code>) y
<code>git merge</code> lo une; si dos ramas cambian la misma parte de un archivo hay un conflicto: Git pausa la fusión y hay
que editar el archivo, marcarlo con <code>git add</code> y confirmar {c('progit')}. Una <i>pull request</i> propone
integrar cambios y permite revisarlos y comentarlos antes de fusionarlos {c('gh_pr')}. El archivo <code>.gitignore</code>
evita subir archivos locales {c('gh_ignore')}; por eso <code>.env</code> y las claves privadas nunca se versionan: lo que
se sube queda en el historial. La <code>apiKey</code> web de Firebase es la excepción: solo identifica el proyecto y puede
ir en el código, mientras que los datos los protegen las reglas de seguridad y App Check {c('api_keys')}.</p>
<p><b>Privacidad y protección de datos.</b> Guardamos el uid, el correo o nombre que entrega cada proveedor y los datos de
los productos. Authentication procesa contraseñas, correos, teléfonos, <i>user agents</i> e IP, y el desarrollador suele
ser el responsable de los datos (<i>data controller</i>) mientras que Google es el encargado del tratamiento
{c('privacy')}. En México aplica la nueva Ley Federal de Protección de Datos Personales en Posesión de los Particulares,
vigente desde el 21 de marzo de 2025 y supervisada por la Secretaría Anticorrupción y Buen Gobierno {c('ey')}. Los datos
se protegen con contraseñas manejadas por Authentication (nosotros no las guardamos), HTTPS de Hosting, rutas por uid y,
en producción, reglas de seguridad.</p>

<h1>Conclusiones</h1>
<p>El gestor de productos nos obligó a unir conceptos que parecían separados: autenticación, modelado de datos, límites
del servicio, manejo de archivos en el navegador y publicación. La principal enseñanza es que cada decisión tiene un costo.
Base64 en Firestore evita la tarjeta, pero limita el tamaño; el modo de prueba facilita el desarrollo, pero deja los datos
abiertos; y la validación del navegador mejora la experiencia, pero no es seguridad. Conocer esos límites nos permite
justificar por qué la solución sirve en la escuela y qué cambiaríamos en producción.</p>

<h1 style="break-before:page" class="first">Referencias</h1>
{referencias()}
"""
    return cuerpo
