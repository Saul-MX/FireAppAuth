"""Documento D: bitácora de trabajo en pareja (una sola hoja)."""
from componentes import esc

CSS_HOJA = """
body{font-size:9pt;line-height:1.35}
.sheet{page:sheet;position:relative;width:8.5in;height:11in;overflow:hidden;padding:42pt 52pt 30pt 58pt}
.sheet .sbar{position:absolute;left:0;top:0;bottom:0;width:25.5pt;background:#ff4600}
.head{display:flex;gap:16pt;align-items:center;margin-bottom:14pt}
.head img{width:56pt;height:auto;flex:none}
.head .org{font-weight:700;font-size:9.5pt}
.head .car{font-size:8pt;color:#59595e;margin-bottom:6pt}
.head .eti{font-weight:700;font-size:8.5pt;color:#ff4600;margin-bottom:1pt}
.head .tit{font-weight:700;font-size:18pt;line-height:1.2}
.head .sub{font-size:9pt;color:#59595e}
.meta{display:grid;grid-template-columns:1fr 1fr;gap:3pt 18pt;font-size:8.5pt;margin-bottom:12pt;padding:8pt 10pt;background:#f6f6f7;border-left:3pt solid #ff4600}
.meta .k{font-weight:700;color:#59595e}
.sec{font-size:11pt;font-weight:700;margin:0 0 6pt}
.persona{margin-bottom:11pt;break-inside:avoid}
.persona .nom{background:#ff4600;color:#fff;font-weight:700;font-size:9.5pt;padding:5pt 8pt}
table.reg{width:100%;border-collapse:collapse;font-size:8.3pt;margin:0}
table.reg th{background:#fff;color:#59595e;font-weight:700;font-size:7.8pt;text-align:left;padding:4pt 6pt;border-bottom:1pt solid #ff4600}
table.reg td{padding:4.5pt 6pt;vertical-align:top;border-bottom:.5pt solid #e6e6ea}
table.reg tbody tr:nth-child(odd) td{background:#f6f6f7}
table.reg td.f{white-space:nowrap;width:52pt}
table.reg td.c{width:118pt}
table.reg td.c a{font-weight:700;text-decoration:underline}
table.reg td.c small{display:block;color:#59595e;font-size:7.3pt;margin-top:1pt}
table.reg td.vacio{height:21pt}
.pie{font-size:7.6pt;color:#59595e;margin-top:8pt;line-height:1.4}
"""


def construir(d):
    repo = d['repositorio'].rstrip('/')
    nombres = d['integrantes']
    por_persona = {n: [r for r in d['bitacora'] if r['integrante'] == n] for n in nombres}

    bloques = ''
    for nombre in nombres:
        filas = ''
        for r in por_persona[nombre]:
            enlace = f"{repo}/commit/{r['commit']}"
            filas += (f'<tr><td class="f">{esc(r["fecha"])}</td><td>{esc(r["actividad"])}</td>'
                      f'<td class="c"><a href="{enlace}">{esc(r["commit"])}</a>'
                      f'<small>{esc(r["mensaje"])}</small></td></tr>')
        if not por_persona[nombre]:
            # Sin registros: renglones en blanco para que el integrante los complete
            filas = '<tr><td class="f vacio"></td><td></td><td class="c"></td></tr>' * 4
        bloques += (f'<div class="persona"><div class="nom">{esc(nombre)}</div>'
                    f'<table class="reg"><thead><tr><th>Fecha</th><th>Actividad realizada</th><th>Commit</th></tr></thead>'
                    f'<tbody>{filas}</tbody></table></div>')

    cuerpo = f"""
<section class="sheet">
  <div class="sbar"></div>
  <div class="head">
    <img src="logo.png" alt="IEU Universidad">
    <div>
      <div class="org">INSTITUTO DE ESTUDIOS UNIVERSITARIOS</div>
      <div class="car">Ingeniería en Sistemas y Tecnologías de la Información</div>
      <div class="eti">ACTIVIDAD COLABORATIVA · BITÁCORA DE TRABAJO EN PAREJA</div>
      <div class="tit">Gestor de productos con Firebase</div>
    </div>
  </div>
  <div class="meta">
    <div><span class="k">Integrantes: </span>{esc(' y '.join(nombres))}</div>
    <div><span class="k">Fecha: </span>{esc(d['fecha'])}</div>
    <div><span class="k">Materia: </span>{esc(d['materia'])}</div>
    <div><span class="k">Docente: </span>{esc(d['docente'])}</div>
    <div><span class="k">Repositorio: </span><a href="{repo}">{esc(repo)}</a></div>
    <div><span class="k">Aplicación: </span><a href="{d['url_publica']}">{esc(d['url_publica'])}</a></div>
  </div>
  <div class="sec">Registro de actividades por integrante</div>
  {bloques}
  <div class="pie">Cada commit enlaza a <b>{esc(repo)}/commit/&lt;código&gt;</b>. Lo realizado por cada integrante debe
  corresponder a los commits hechos con su propia cuenta de GitHub.</div>
</section>"""
    return cuerpo, CSS_HOJA
