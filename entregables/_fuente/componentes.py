"""Piezas compartidas por los tres documentos: estilos, portada, tablas, código y capturas.

El diseño replica el formato de «Funciones y actividades del equipo» (IEU):
barra naranja en la portada, tipografía DejaVu Sans, encabezados en negro,
subtítulos y viñetas en naranja y tablas con encabezado naranja.
"""
import html
import json
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parent          # entregables/_fuente
ENTREGABLES = AQUI.parent                       # entregables
RAIZ = ENTREGABLES.parent                       # src (código de la app)
CAPTURAS = ENTREGABLES / 'capturas'

NARANJA = '#ff4600'

CSS = """
@font-face{font-family:'DejaVu';src:url('fuentes/DejaVuSans.ttf');font-weight:400;font-style:normal}
@font-face{font-family:'DejaVu';src:url('fuentes/DejaVuSans-Bold.ttf');font-weight:700;font-style:normal}
@font-face{font-family:'DejaVu';src:url('fuentes/DejaVuSans-Oblique.ttf');font-weight:400;font-style:italic}
@font-face{font-family:'DejaVu';src:url('fuentes/DejaVuSans-BoldOblique.ttf');font-weight:700;font-style:italic}
@font-face{font-family:'DejaVuMono';src:url('fuentes/DejaVuSansMono.ttf');font-weight:400}
@font-face{font-family:'DejaVuMono';src:url('fuentes/DejaVuSansMono-Bold.ttf');font-weight:700}

@page{size:Letter;margin:25mm 24mm 22mm 24mm}
@page cover{size:Letter;margin:0}
@page sheet{size:Letter;margin:0}

*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font-family:'DejaVu',sans-serif;font-size:11.5pt;line-height:1.4;color:#212126;
     -webkit-print-color-adjust:exact;print-color-adjust:exact}
p{margin:0 0 10pt}
b,strong{font-weight:700}
a{color:#d33f00;text-decoration:none}

h1{font-size:17pt;line-height:1.25;margin:26pt 0 12pt;font-weight:700;break-after:avoid}
h1.first{margin-top:0}
h2{font-size:12.5pt;line-height:1.3;margin:18pt 0 6pt;font-weight:700;break-after:avoid}
h3{font-size:11.5pt;line-height:1.35;margin:0 0 7pt;font-weight:700;color:#ff4600;break-after:avoid}
h2.paso{break-before:page;margin-top:0}

ul{list-style:none;margin:0 0 10pt;padding-left:17pt}
ul li{position:relative}
ul li::before{content:'';position:absolute;left:-12pt;top:.56em;width:4.3pt;height:4.3pt;border-radius:50%;background:#ff4600}
ol{margin:0 0 10pt;padding-left:19pt}
ol li{padding-left:2pt;margin-bottom:3pt}
ol li::marker{color:#ff4600;font-weight:700}

code{font-family:'DejaVuMono',monospace;font-size:9pt;background:#f6f6f7;color:#b23400;padding:.5pt 3pt;border-radius:2pt}

table{width:100%;border-collapse:collapse;margin:8pt 0 14pt;font-size:10pt;line-height:1.35}
th{background:#ff4600;color:#fff;text-align:left;font-weight:700;padding:5.5pt 6pt}
td{padding:5pt 6pt;vertical-align:top}
tbody tr:nth-child(odd) td{background:#f6f6f7}
tr{break-inside:avoid}
table.chica{font-size:9pt;break-inside:avoid}
table.larga{break-inside:auto}
td.k{font-weight:700;color:#59595e;white-space:nowrap}

.note{border-left:3pt solid #ff4600;background:#f6f6f7;padding:7pt 11pt;margin:8pt 0 12pt;font-size:10.5pt;break-inside:avoid}
.note p{margin:0}
.note b.t{color:#ff4600}

/* ---------- Portada ---------- */
.cover{page:cover;position:relative;width:8.5in;height:11in;overflow:hidden;break-after:page;text-align:center}
.cover .cbar{position:absolute;left:0;top:0;bottom:0;width:25.5pt;background:#ff4600}
.cover .logo{position:absolute;left:256.5pt;top:45.4pt;width:98.9pt;height:auto}
.cover .abs{position:absolute;left:0;right:0;line-height:1.2}
.cover .org{top:219.5pt;font-weight:700;font-size:14pt}
.cover .carrera{top:241.5pt;font-size:11pt;color:#59595e}
.cover .etiqueta{top:296.5pt;font-weight:700;font-size:10.5pt;color:#ff4600}
.cover .titulo{top:318pt;font-weight:700;font-size:19pt}
.cover .subtitulo{top:350.5pt;font-size:12pt;color:#59595e}
.cover .integrantes{top:404.5pt;font-size:11pt}
.cover .integrantes .lbl{font-weight:700;margin-bottom:8.5pt}
.cover .integrantes div.n{margin-bottom:5.4pt}
.cover .meta{position:absolute;left:163pt;top:534pt;font-size:11pt;text-align:left}
.cover .meta div{display:flex;margin-bottom:8.4pt}
.cover .meta .l{width:70pt;font-weight:700;color:#59595e}
.cover .url{top:640pt;font-size:9.5pt;color:#59595e}

/* ---------- Código (capturas del código) ---------- */
.fig{margin:8pt 0 12pt;break-inside:avoid}
.code{border:1px solid #dcdce0;border-radius:4pt;overflow:hidden}
.code .fbar{background:#212126;color:#fff;font-size:7.6pt;padding:4.5pt 9pt;display:flex;justify-content:space-between;gap:10pt}
.code .fbar .r{color:#ffb08f}
.code .body{background:#f6f6f7;padding:6pt 0;font-family:'DejaVuMono',monospace;font-size:7.1pt;line-height:1.38}
.code .l{display:flex}
.code .ln{width:27pt;flex:none;text-align:right;padding-right:8pt;color:#a0a0a8;user-select:none}
.code .tx{flex:1;white-space:pre-wrap;overflow-wrap:anywhere;padding-right:8pt;min-height:1em}
.code .gap{color:#a0a0a8;padding:1pt 0 1pt 35pt}
.hc{color:#7b7b86}.hs{color:#13795b}.hk{color:#d33f00;font-weight:700}.hn{color:#5b4bd6}
.hf{color:#1f5fbf}.ht{color:#d33f00}.ha{color:#7a4fc0}
.term{background:#212126;color:#f2f2f4;border-radius:4pt;padding:9pt 12pt;font-family:'DejaVuMono',monospace;font-size:7.8pt;line-height:1.5;white-space:pre-wrap}
.term .p{color:#ff8a5c}.term .o{color:#a8a8b2}
.cap{font-size:8.5pt;color:#59595e;text-align:center;margin-top:4pt}

/* ---------- Capturas de consola ---------- */
.shot{border:1.4pt dashed #ff4600;border-radius:5pt;background:#fff6f1;text-align:center;padding:16pt 20pt;color:#59595e}
.shot .tag{display:inline-block;background:#ff4600;color:#fff;font-weight:700;font-size:7.5pt;letter-spacing:.5pt;padding:2pt 8pt;border-radius:9pt;margin-bottom:7pt}
.shot .que{font-size:9.5pt;line-height:1.4;color:#212126}
.shot .arch{font-family:'DejaVuMono',monospace;font-size:7.5pt;margin-top:6pt;color:#8a8a93}
.shotimg img{display:block;margin:0 auto;max-width:100%;max-height:300pt;border:1px solid #dcdce0;border-radius:3pt}

.tree{background:#f6f6f7;border-radius:4pt;padding:9pt 12pt;font-family:'DejaVuMono',monospace;font-size:8.6pt;line-height:1.55;white-space:pre-wrap;margin:6pt 0 12pt;break-inside:avoid}
.tree .v{color:#d33f00;font-weight:700}
.tree .d{color:#7b7b86}

.cols{display:flex;gap:14pt}.cols>div{flex:1}
.ref{padding-left:22pt;text-indent:-22pt;font-size:10pt;line-height:1.4;margin-bottom:7pt;overflow-wrap:anywhere}
"""


def esc(texto):
    return html.escape(str(texto), quote=False)


def cargar_datos():
    return json.loads((AQUI / 'datos.json').read_text(encoding='utf-8'))


def documento(titulo, cuerpo, css_extra=''):
    """Envuelve el cuerpo en una página HTML completa."""
    return (f'<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">'
            f'<title>{esc(titulo)}</title><style>{CSS}{css_extra}</style></head>'
            f'<body>{cuerpo}</body></html>')


# ---------------------------------------------------------------- portada
def portada(datos, etiqueta, titulo, subtitulo, extra_url=True):
    nombres = ''.join(f'<div class="n">{esc(n)}</div>' for n in datos['integrantes'])
    url = (f'<div class="abs url">Aplicación publicada: <a href="{datos["url_publica"]}">{datos["url_publica"]}</a></div>'
           if extra_url else '')
    return f"""
<section class="cover">
  <div class="cbar"></div>
  <img class="logo" src="logo.png" alt="IEU Universidad">
  <div class="abs org">INSTITUTO DE ESTUDIOS UNIVERSITARIOS</div>
  <div class="abs carrera">Ingeniería en Sistemas y Tecnologías de la Información</div>
  <div class="abs etiqueta">{esc(etiqueta)}</div>
  <div class="abs titulo">{esc(titulo)}</div>
  <div class="abs subtitulo">{esc(subtitulo)}</div>
  <div class="abs integrantes"><div class="lbl">Integrantes</div>{nombres}</div>
  <div class="meta">
    <div><span class="l">Materia:</span><span>{esc(datos['materia'])}</span></div>
    <div><span class="l">Docente:</span><span>{esc(datos['docente'])}</span></div>
    <div><span class="l">Fecha:</span><span>{esc(datos['fecha'])}</span></div>
  </div>
  {url}
</section>"""


# ---------------------------------------------------------------- tablas y listas
def tabla(encabezados, filas, chica=False, anchos=None, larga=False):
    cols = ''
    if anchos:
        cols = '<colgroup>' + ''.join(f'<col style="width:{a}">' for a in anchos) + '</colgroup>'
    th = ''.join(f'<th>{e}</th>' for e in encabezados)
    trs = ''
    for fila in filas:
        trs += '<tr>' + ''.join(f'<td>{c}</td>' for c in fila) + '</tr>'
    clase = ('chica ' if chica else '') + ('larga' if larga else '')
    return f'<table class="{clase.strip()}">{cols}<thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'


def lista(items, ordenada=False):
    tag = 'ol' if ordenada else 'ul'
    return f'<{tag}>' + ''.join(f'<li>{i}</li>' for i in items) + f'</{tag}>'


def nota(texto, titulo='Nota'):
    return f'<div class="note"><p><b class="t">{esc(titulo)}.</b> {texto}</p></div>'


def arbol(texto):
    """Estructura de datos en texto; lo que va entre llaves se resalta en naranja."""
    seguro = esc(texto)
    seguro = re.sub(r'\{([^}]*)\}', r'<span class="v">{\1}</span>', seguro)
    return f'<div class="tree">{seguro}</div>'


# ---------------------------------------------------------------- resaltado de código
_JS = re.compile(r"""
 (?P<c>//.*$)
|(?P<s>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`)
|(?P<k>\b(?:import|from|export|const|let|var|function|return|if|else|for|of|in|while|await|async|new|try|catch|finally|throw|null|true|false|typeof|class|break|continue|default|this)\b)
|(?P<n>\b\d+(?:\.\d+)?\b)
|(?P<f>\b[A-Za-z_$][\w$]*(?=\())
""", re.X)
_HTML = re.compile(r'(?P<c><!--.*?-->)|(?P<t></?[A-Za-z][\w-]*)|(?P<s>"[^"]*")|(?P<a>\b[A-Za-z-]+(?==))')


def _resaltar_linea(linea, lenguaje):
    patron = _HTML if lenguaje == 'html' else _JS
    salida, pos = [], 0
    for m in patron.finditer(linea):
        salida.append(esc(linea[pos:m.start()]))
        clase = 'h' + m.lastgroup
        salida.append(f'<span class="{clase}">{esc(m.group())}</span>')
        pos = m.end()
    salida.append(esc(linea[pos:]))
    return ''.join(salida)


_contador = {'fig': 0}


def codigo(ruta, rangos, pie=None):
    """Captura del código real: lee el archivo del proyecto y muestra las líneas indicadas."""
    lineas = (RAIZ / ruta).read_text(encoding='utf-8').splitlines()
    lenguaje = 'html' if ruta.endswith('.html') else 'js'
    if isinstance(rangos, tuple):
        rangos = [rangos]
    cuerpo, etiquetas = '', []
    # Quita la sangría común (index.html anida mucho) para que el fragmento no se pegue a la derecha
    seleccion = [lineas[n - 1].rstrip() for (a, b) in rangos for n in range(a, b + 1)]
    comun = min((len(s) - len(s.lstrip(' ')) for s in seleccion if s.strip()), default=0)
    for idx, (a, b) in enumerate(rangos):
        if idx:
            cuerpo += '<div class="l gap">…</div>'
        for n in range(a, b + 1):
            linea = lineas[n - 1].rstrip()
            sangria = max(0, len(linea) - len(linea.lstrip(' ')) - comun)
            # La sangría se pasa a padding para que las líneas partidas queden alineadas con la primera
            cuerpo += (f'<div class="l"><span class="ln">{n}</span>'
                       f'<span class="tx" style="padding-left:{sangria + 2}ch;text-indent:-2ch">'
                       f'{_resaltar_linea(linea.lstrip(" "), lenguaje)}</span></div>')
        etiquetas.append(f'{a}–{b}' if a != b else str(a))
    _contador['fig'] += 1
    leyenda = f'Figura {_contador["fig"]}. {esc(pie)}' if pie else ''
    return (f'<div class="fig"><div class="code"><div class="fbar"><span>{esc(ruta)}</span>'
            f'<span class="r">líneas {", ".join(etiquetas)}</span></div><div class="body">{cuerpo}</div></div>'
            f'<div class="cap">{leyenda}</div></div>')


def terminal(lineas, pie=None):
    """Comandos de terminal: las líneas que empiezan con $ se resaltan como comando."""
    cuerpo = ''
    for linea in lineas:
        if linea.startswith('$ '):
            cuerpo += f'<span class="p">$</span> {esc(linea[2:])}\n'
        else:
            cuerpo += f'<span class="o">{esc(linea)}</span>\n'
    _contador['fig'] += 1
    leyenda = f'Figura {_contador["fig"]}. {esc(pie)}' if pie else ''
    return f'<div class="fig"><div class="term">{cuerpo.rstrip()}</div><div class="cap">{leyenda}</div></div>'


# ---------------------------------------------------------------- capturas de consola
PENDIENTES = []   # (archivo, qué capturar): se vuelca en capturas/LEEME.txt


def captura(slug, que, pie):
    """Inserta la imagen capturas/<slug>.png|jpg si existe; si no, un recuadro de captura pendiente."""
    _contador['fig'] += 1
    leyenda = f'Figura {_contador["fig"]}. {esc(pie)}'
    for ext in ('png', 'jpg', 'jpeg', 'webp'):
        archivo = CAPTURAS / f'{slug}.{ext}'
        if archivo.exists():
            return (f'<div class="fig shotimg"><img src="{archivo.as_uri()}" alt="{esc(pie)}">'
                    f'<div class="cap">{leyenda}</div></div>')
    PENDIENTES.append((slug, que))
    return (f'<div class="fig"><div class="shot"><div class="tag">CAPTURA PENDIENTE</div>'
            f'<div class="que">{esc(que)}</div><div class="arch">capturas/{slug}.png</div></div>'
            f'<div class="cap">{leyenda}</div></div>')


def reiniciar_contadores():
    _contador['fig'] = 0
    PENDIENTES.clear()
