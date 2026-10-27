"""Genera los tres PDF de la entrega a partir del código del proyecto y de datos.json.

Uso (desde la carpeta src del proyecto):
    python entregables/_fuente/generar.py

Solo necesita Python 3 y Microsoft Edge o Google Chrome instalados; no instala nada.
Las capturas de pantalla se agregan guardando las imágenes en entregables/capturas/ con los
nombres que indica entregables/capturas/LEEME.txt y volviendo a ejecutar este script.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True   # no deja carpetas __pycache__ dentro del proyecto
sys.path.insert(0, str(Path(__file__).resolve().parent))
# La consola de Windows usa cp1252 y no imprime algunos símbolos
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import componentes as comp
import doc_bitacora
import doc_investigacion
import doc_manual

NAVEGADORES = [
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
]


def buscar_navegador():
    for ruta in NAVEGADORES:
        if os.path.exists(ruta):
            return ruta
    for nombre in ('msedge', 'chrome', 'google-chrome', 'chromium'):
        ruta = shutil.which(nombre)
        if ruta:
            return ruta
    sys.exit('No se encontró Microsoft Edge ni Google Chrome para generar los PDF.')


def a_pdf(navegador, html, nombre_pdf):
    """Escribe el HTML junto a las fuentes y lo imprime a PDF con el navegador sin interfaz."""
    temporal = comp.AQUI / f'_tmp_{nombre_pdf}.html'
    salida = comp.ENTREGABLES / nombre_pdf
    temporal.write_text(html, encoding='utf-8')
    perfil = tempfile.mkdtemp(prefix='pdf_perfil_')
    try:
        subprocess.run([
            navegador, '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
            '--run-all-compositor-stages-before-draw', '--virtual-time-budget=15000',
            f'--user-data-dir={perfil}', f'--print-to-pdf={salida}', temporal.as_uri(),
        ], check=True, timeout=240, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    finally:
        temporal.unlink(missing_ok=True)
        shutil.rmtree(perfil, ignore_errors=True)
    print(f'  ✔ {salida.name}  ({salida.stat().st_size // 1024} KB)')


def escribir_leeme_capturas(pendientes):
    lineas = ['CAPTURAS PARA EL MANUAL (documento B)', '',
              'Guarda cada captura en esta carpeta con el nombre indicado (.png, .jpg o .webp) y vuelve a ejecutar:',
              '    python entregables/_fuente/generar.py', '',
              'Si el archivo existe, el manual lo inserta en lugar del recuadro «CAPTURA PENDIENTE».', '']
    vistos = set()
    for slug, que in pendientes:
        if slug not in vistos:
            vistos.add(slug)
            lineas.append(f'  {slug}.png\n      {que}')
    if not vistos:
        lineas.append('(No hay capturas pendientes.)')
    (comp.CAPTURAS / 'LEEME.txt').write_text('\n'.join(lineas) + '\n', encoding='utf-8')


def main():
    datos = comp.cargar_datos()
    navegador = buscar_navegador()
    print('Generando PDF con', Path(navegador).name)

    comp.reiniciar_contadores()
    manual = doc_manual.construir(datos)
    a_pdf(navegador, comp.documento('Manual paso a paso - Gestor de productos', manual),
          'B_Manual_Paso_a_Paso.pdf')
    pendientes = list(comp.PENDIENTES)
    escribir_leeme_capturas(pendientes)

    comp.reiniciar_contadores()
    inv = doc_investigacion.construir(datos)
    a_pdf(navegador, comp.documento('Investigación de conceptos - Gestor de productos', inv),
          'C_Investigacion_de_Conceptos.pdf')

    cuerpo, css = doc_bitacora.construir(datos)
    a_pdf(navegador, comp.documento('Bitácora de trabajo en pareja - Gestor de productos', cuerpo, css),
          'D_Bitacora_Trabajo_en_Pareja.pdf')

    print(f'Capturas pendientes en el manual: {len({slug for slug, _ in pendientes})} '
          '(ver entregables/capturas/LEEME.txt)')


if __name__ == '__main__':
    main()
