"""Genera las capturas de muestra de los módulos ConiTech.

Cada pantalla es un HTML (maqueta con datos de ejemplo) que se renderiza con
Chrome headless y se guarda en ../assets/img/capturas/<nombre>.webp.
Para usar capturas reales, reemplaza esos .webp con el mismo nombre.

Uso:  python generar.py
"""
import pathlib
import subprocess
import tempfile

from PIL import Image

AQUI = pathlib.Path(__file__).parent
SALIDA = AQUI.parent / "assets" / "img" / "capturas"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
W, H = 1440, 900

BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1440px;height:900px;font:14px Inter,Segoe UI,Arial,sans-serif;color:#0B1E3F;background:#F1F5F9;display:flex;overflow:hidden}
.side{width:236px;background:#0B1220;color:#CBD5E1;padding:22px 16px;display:flex;flex-direction:column;gap:4px}
.brand{display:flex;align-items:center;gap:10px;font:700 19px 'Space Grotesk',Segoe UI,sans-serif;color:#fff;margin:0 6px 26px}
.brand b{color:#60A5FA}
.logo{width:30px;height:30px;border-radius:8px;background:linear-gradient(135deg,#3B82F6,#1D4ED8);position:relative}
.logo:after{content:'';position:absolute;right:-5px;top:9px;width:11px;height:11px;border-radius:3px;background:#F97316}
.nav{padding:10px 12px;border-radius:8px;font-size:14px;display:flex;align-items:center;gap:10px}
.nav i{width:16px;height:16px;border-radius:4px;background:#334155;display:inline-block}
.nav.on{background:#1E293B;color:#fff}.nav.on i{background:#F97316}
.main{flex:1;display:flex;flex-direction:column}
.top{height:64px;background:#fff;border-bottom:1px solid #E2E8F0;display:flex;align-items:center;justify-content:space-between;padding:0 28px}
.top h1{font:700 20px 'Space Grotesk',Segoe UI,sans-serif}
.crumb{color:#64748B;font-size:13px;margin-top:2px}
.user{display:flex;align-items:center;gap:10px;color:#475569;font-size:13px}
.av{width:34px;height:34px;border-radius:50%;background:#DBEAFE;color:#1D4ED8;display:grid;place-items:center;font-weight:700}
.content{padding:24px 28px;display:flex;flex-direction:column;gap:18px;flex:1}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.kpi{background:#fff;border:1px solid #E2E8F0;border-radius:12px;padding:16px 18px}
.kpi small{color:#64748B;font-size:12.5px}.kpi b{display:block;font:700 26px 'Space Grotesk',Segoe UI,sans-serif;margin-top:6px}
.kpi em{font-style:normal;font-size:12px;color:#16A34A}
.card{background:#fff;border:1px solid #E2E8F0;border-radius:12px;padding:18px}
.card h2{font:700 15px 'Space Grotesk',Segoe UI,sans-serif;margin-bottom:14px;display:flex;justify-content:space-between;align-items:center}
table{width:100%;border-collapse:collapse;font-size:13px}
th{text-align:left;color:#64748B;font-weight:600;font-size:12px;padding:9px 10px;border-bottom:1px solid #E2E8F0;background:#F8FAFC}
td{padding:11px 10px;border-bottom:1px solid #F1F5F9}
.chip{display:inline-block;padding:3px 10px;border-radius:999px;font-size:11.5px;font-weight:600}
.ok{background:#DCFCE7;color:#15803D}.wait{background:#FEF3C7;color:#B45309}.bad{background:#FEE2E2;color:#B91C1C}.info{background:#DBEAFE;color:#1D4ED8}
.btn{background:#F97316;color:#fff;border-radius:8px;padding:8px 14px;font-size:13px;font-weight:600}
.btn2{background:#fff;color:#1D4ED8;border:1px solid #BFDBFE;border-radius:8px;padding:7px 13px;font-size:13px;font-weight:600}
.row{display:flex;gap:18px}.grow{flex:1}
.field{display:flex;flex-direction:column;gap:6px;font-size:12.5px;color:#475569}
.input{border:1px solid #CBD5E1;border-radius:8px;padding:9px 11px;color:#0B1E3F;background:#fff;font-size:13.5px}
.r{text-align:right}.mono{font-variant-numeric:tabular-nums}
"""

FUENTES = ('<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700'
           '&family=Inter:wght@400;600&display=block" rel="stylesheet">')


def app(menu_activo, titulo, ruta, cuerpo, extra_css=""):
    menu = ["Inicio", "Viáticos", "Conciliación", "Matrícula", "WhatsApp",
            "Inventario", "Facturación", "Automatizaciones", "Reportes BI"]
    nav = "".join(f'<div class="nav{" on" if m == menu_activo else ""}"><i></i>{m}</div>' for m in menu)
    return f"""<!doctype html><html><head><meta charset="utf-8">{FUENTES}
<style>{BASE_CSS}{extra_css}</style></head><body>
<aside class="side"><div class="brand"><span class="logo"></span><span>Coni<b>Tech</b></span></div>{nav}</aside>
<div class="main"><div class="top"><div><h1>{titulo}</h1><div class="crumb">{ruta}</div></div>
<div class="user">Administración<span class="av">AD</span></div></div>
<div class="content">{cuerpo}</div></div></body></html>"""


def kpis(items):
    return '<div class="kpis">' + "".join(
        f'<div class="kpi"><small>{a}</small><b>{b}</b><em>{c}</em></div>' for a, b, c in items) + "</div>"


def tabla(cab, filas, derecha=()):
    th = "".join(f'<th class="{"r" if i in derecha else ""}">{c}</th>' for i, c in enumerate(cab))
    tr = "".join("<tr>" + "".join(f'<td class="{"r mono" if i in derecha else ""}">{c}</td>'
                                  for i, c in enumerate(f)) + "</tr>" for f in filas)
    return f"<table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>"


ESTADO = {"Aprobado": "ok", "Pendiente": "wait", "Observado": "bad", "En revisión": "info",
          "Conciliado": "ok", "Diferencia": "bad", "Sin match": "wait",
          "Matriculado": "ok", "Pago pendiente": "wait", "Reserva": "info",
          "Aceptado SUNAT": "ok", "Enviado": "info", "Rechazado": "bad",
          "Éxito": "ok", "Reintento": "wait"}


def chip(t):
    return f'<span class="chip {ESTADO.get(t, "info")}">{t}</span>'


# ---------------------------------------------------------------- pantallas
def viaticos():
    filas = [
        ["RV-0241", "Carlos Mendoza", "Visita cliente Arequipa", "S/ 1,200.00", "S/ 1,148.50", chip("Aprobado")],
        ["RV-0240", "Lucía Paredes", "Capacitación Trujillo", "S/ 850.00", "S/ 862.30", chip("En revisión")],
        ["RV-0239", "Jorge Salas", "Auditoría Piura", "S/ 1,500.00", "S/ 1,212.00", chip("Pendiente")],
        ["RV-0238", "Ana Quispe", "Feria comercial Cusco", "S/ 2,000.00", "S/ 1,985.40", chip("Aprobado")],
        ["RV-0237", "Miguel Torres", "Supervisión de obra Ica", "S/ 600.00", "S/ 655.00", chip("Observado")],
        ["RV-0236", "Rosa Huamán", "Reunión proveedores Lima", "S/ 300.00", "S/ 287.90", chip("Aprobado")],
        ["RV-0235", "Pedro Castillo", "Instalación Chiclayo", "S/ 1,100.00", "S/ 1,030.00", chip("Aprobado")],
    ]
    detalle = """<div class="card" style="width:400px"><h2>Detalle RV-0240 <span class="chip info">En revisión</span></h2>
    <div style="display:flex;flex-direction:column;gap:10px;font-size:13px">
    <div style="display:flex;justify-content:space-between"><span>Anticipo entregado</span><b>S/ 850.00</b></div>
    <div style="display:flex;justify-content:space-between"><span>Total comprobantes (6)</span><b>S/ 862.30</b></div>
    <div style="display:flex;justify-content:space-between;color:#B45309"><span>Saldo a reembolsar</span><b>S/ 12.30</b></div>
    <hr style="border:0;border-top:1px solid #E2E8F0">
    <div style="display:flex;justify-content:space-between"><span>🧾 Factura · Hotel Libertador</span><span>S/ 420.00</span></div>
    <div style="display:flex;justify-content:space-between"><span>🧾 Boleta · Transporte</span><span>S/ 180.00</span></div>
    <div style="display:flex;justify-content:space-between"><span>🧾 Factura · Alimentación</span><span>S/ 162.30</span></div>
    <div style="display:flex;justify-content:space-between"><span>🧾 Declaración jurada · Movilidad</span><span>S/ 100.00</span></div>
    <hr style="border:0;border-top:1px solid #E2E8F0">
    <b style="font-size:12.5px;color:#64748B">Flujo de aprobación</b>
    <div>✅ Colaborador — envió 10/11</div><div>✅ Jefe de área — aprobó 11/11</div><div>⏳ Contabilidad — en revisión</div>
    <div style="display:flex;gap:8px;margin-top:6px"><span class="btn">Aprobar</span><span class="btn2">Observar</span></div></div></div>"""
    cuerpo = kpis([("Anticipos entregados", "S/ 48,350", "Mes actual"), ("Por rendir", "S/ 6,120", "9 colaboradores"),
                   ("Rendido y aprobado", "S/ 39,870", "▲ 12% vs mes anterior"), ("Observados", "3", "Requieren corrección")])
    cuerpo += f"""<div class="row"><div class="card grow"><h2>Rendiciones de viáticos <span class="btn">+ Nueva rendición</span></h2>
    {tabla(["Código", "Colaborador", "Motivo", "Anticipo", "Rendido", "Estado"], filas, derecha=(3, 4))}</div>{detalle}</div>"""
    return app("Viáticos", "Viáticos y rendiciones", "Finanzas / Viáticos / Rendiciones", cuerpo)


def conciliacion():
    banco = [["03/11", "TRANSF. CLIENTE 0045", "12,500.00", chip("Conciliado")],
             ["04/11", "PAGO PROV. 2231", "-3,240.00", chip("Conciliado")],
             ["05/11", "COMISIÓN MANT. CTA", "-25.00", chip("Sin match")],
             ["06/11", "DEPÓSITO EFECTIVO", "4,800.00", chip("Conciliado")],
             ["07/11", "TRANSF. CLIENTE 0051", "7,150.00", chip("Diferencia")],
             ["08/11", "PAGO PLANILLA", "-18,600.00", chip("Conciliado")],
             ["09/11", "ITF", "-2.35", chip("Sin match")]]
    sistema = [["03/11", "Cobro F001-1203", "12,500.00", chip("Conciliado")],
               ["04/11", "Pago OC-2231", "-3,240.00", chip("Conciliado")],
               ["06/11", "Cobro B002-0877", "4,800.00", chip("Conciliado")],
               ["07/11", "Cobro F001-1210", "7,105.00", chip("Diferencia")],
               ["08/11", "Planilla Oct-2026", "-18,600.00", chip("Conciliado")],
               ["10/11", "Cobro F001-1215", "2,300.00", chip("Sin match")]]
    cuerpo = """<div class="row" style="align-items:flex-end">
    <div class="field" style="width:260px">Cuenta bancaria<div class="input">BCP Soles · 194-2283xxx-0-41</div></div>
    <div class="field" style="width:200px">Periodo<div class="input">Noviembre 2026</div></div>
    <div class="field" style="width:260px">Extracto<div class="input">📄 extracto_nov_2026.xlsx</div></div>
    <div class="grow"></div><span class="btn">⚡ Conciliar automáticamente</span></div>"""
    cuerpo += kpis([("Movimientos banco", "214", "Importados del extracto"), ("Conciliados automáticamente", "198", "92.5% del total"),
                    ("Con diferencia", "4", "S/ 45.00 por revisar"), ("Sin coincidencia", "12", "Comisiones e ITF")])
    cuerpo += f"""<div class="row"><div class="card grow"><h2>Extracto bancario</h2>
    {tabla(["Fecha", "Descripción", "Importe", "Estado"], banco, derecha=(2,))}</div>
    <div class="card grow"><h2>Registros del sistema</h2>
    {tabla(["Fecha", "Documento", "Importe", "Estado"], sistema, derecha=(2,))}</div></div>"""
    return app("Conciliación", "Conciliación bancaria", "Finanzas / Bancos / Conciliación", cuerpo)


def matricula():
    pasos = "".join(f'<div style="display:flex;align-items:center;gap:8px;color:{c}"><span style="width:26px;height:26px;border-radius:50%;display:grid;place-items:center;background:{b};color:#fff;font-weight:700;font-size:12px">{n}</span>{t}</div>'
                    for n, t, b, c in [(1, "Alumno", "#16A34A", "#0B1E3F"), (2, "Apoderado", "#16A34A", "#0B1E3F"),
                                       (3, "Grado y sección", "#F97316", "#0B1E3F"), (4, "Pago", "#CBD5E1", "#94A3B8"),
                                       (5, "Confirmación", "#CBD5E1", "#94A3B8")])
    filas = [["2026-0412", "Valentina Rojas Díaz", "3° Primaria A", "Mamá · 9xx xxx 214", chip("Matriculado")],
             ["2026-0411", "Mateo Gutiérrez León", "1° Secundaria B", "Papá · 9xx xxx 873", chip("Pago pendiente")],
             ["2026-0410", "Camila Flores Ruiz", "Inicial 5 años", "Mamá · 9xx xxx 552", chip("Matriculado")],
             ["2026-0409", "Sebastián Vega Ortiz", "5° Primaria A", "Papá · 9xx xxx 108", chip("Reserva")],
             ["2026-0408", "Luciana Chávez Paz", "2° Secundaria A", "Mamá · 9xx xxx 761", chip("Matriculado")]]
    form = f"""<div class="card" style="width:470px"><h2>Nueva matrícula 2027</h2>
    <div style="display:flex;justify-content:space-between;margin-bottom:18px;font-size:12.5px">{pasos}</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
    <div class="field">Nivel<div class="input">Primaria</div></div><div class="field">Grado<div class="input">4° grado</div></div>
    <div class="field">Sección<div class="input">B · 6 vacantes</div></div><div class="field">Turno<div class="input">Mañana</div></div>
    <div class="field" style="grid-column:span 2">Alumno<div class="input">Diego Alonso Ramos Salazar · DNI 7xxxxxx3</div></div>
    <div class="field" style="grid-column:span 2">Documentos<div class="input">✅ DNI  ✅ Libreta de notas  ⏳ Constancia de no adeudo</div></div>
    </div><div style="display:flex;gap:8px;margin-top:16px;justify-content:flex-end"><span class="btn2">Anterior</span><span class="btn">Continuar al pago</span></div></div>"""
    vac = "".join(f'<div style="margin-bottom:10px"><div style="display:flex;justify-content:space-between;font-size:12.5px"><span>{g}</span><span>{o}/{t}</span></div><div style="height:8px;background:#E2E8F0;border-radius:4px;margin-top:4px"><div style="height:8px;width:{o*100//t}%;background:{"#F97316" if o/t>.9 else "#1D4ED8"};border-radius:4px"></div></div></div>'
                  for g, o, t in [("Inicial", 52, 60), ("1° – 3° Primaria", 88, 90), ("4° – 6° Primaria", 79, 90), ("Secundaria", 121, 150)])
    cuerpo = kpis([("Matriculados 2027", "340", "▲ 18% vs 2026"), ("Vacantes disponibles", "50", "De 390 en total"),
                   ("Pagos pendientes", "27", "Recordatorio enviado"), ("Matrícula en línea", "76%", "Sin colas en secretaría")])
    cuerpo += f"""<div class="row">{form}<div class="grow" style="display:flex;flex-direction:column;gap:18px">
    <div class="card"><h2>Ocupación por nivel</h2>{vac}</div>
    <div class="card"><h2>Últimas matrículas</h2>{tabla(["Código", "Alumno", "Grado", "Apoderado", "Estado"], filas[:4])}</div></div></div>"""
    return app("Matrícula", "Registro de matrícula", "Académico / Matrícula 2027", cuerpo)


def whatsapp():
    css = """.phone{width:300px;height:560px;border-radius:34px;background:#0B1220;padding:12px;margin:0 auto}
    .scr{background:#EFEAE2;border-radius:24px;height:100%;overflow:hidden;display:flex;flex-direction:column}
    .wh{background:#075E54;color:#fff;padding:14px;font-weight:600;font-size:13px}
    .msg{background:#fff;margin:14px;border-radius:0 10px 10px 10px;padding:10px 12px;font-size:12.5px;line-height:1.45;box-shadow:0 1px 1px #0001}
    .msg small{display:block;text-align:right;color:#94A3B8;font-size:10.5px;margin-top:4px}"""
    camp = [["Recordatorio de pensión – Nov", "1,240", "1,231", "1,102", chip("Éxito")],
            ["Invitación reunión de padres", "860", "858", "790", chip("Éxito")],
            ["Promoción matrícula 2027", "3,500", "2,140", "—", chip("Enviado")],
            ["Aviso de corte de servicio", "95", "95", "88", chip("Éxito")]]
    cuerpo = kpis([("Mensajes enviados (mes)", "12,480", "▲ 34% vs mes anterior"), ("Tasa de entrega", "98.7%", "Números validados"),
                   ("Leídos", "86%", "Promedio por campaña"), ("Respuestas", "1,034", "Derivadas a asesores")])
    cuerpo += f"""<div class="row"><div class="grow" style="display:flex;flex-direction:column;gap:18px">
    <div class="card"><h2>Nueva campaña <span class="btn">Programar envío</span></h2>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
    <div class="field">Lista de contactos<div class="input">Apoderados 2026 · 1,240 contactos</div></div>
    <div class="field">Fecha y hora<div class="input">15/11/2026 · 09:00 a. m.</div></div>
    <div class="field" style="grid-column:span 2">Mensaje (variables: {{nombre}}, {{monto}}, {{fecha}})
    <div class="input" style="height:74px">Hola {{nombre}} 👋, te recordamos que la pensión de noviembre por {{monto}} vence el {{fecha}}. Puedes pagar por Yape o transferencia.</div></div>
    </div></div>
    <div class="card"><h2>Campañas recientes</h2>{tabla(["Campaña", "Destinatarios", "Entregados", "Leídos", "Estado"], camp, derecha=(1, 2, 3))}</div></div>
    <div class="card" style="width:360px"><h2>Vista previa</h2><div class="phone"><div class="scr"><div class="wh">Colegio · Administración</div>
    <div class="msg">Hola <b>María</b> 👋, te recordamos que la pensión de noviembre por <b>S/ 450.00</b> vence el <b>20/11</b>. Puedes pagar por Yape o transferencia.<small>09:00 ✓✓</small></div>
    <div class="msg" style="margin-left:60px;border-radius:10px 0 10px 10px;background:#D9FDD3">¡Gracias! Ya realicé el pago 🙌<small>09:12</small></div>
    </div></div></div></div>"""
    return app("WhatsApp", "Mensajes masivos de WhatsApp", "Comunicaciones / Campañas", cuerpo, css)


def facturacion():
    items = [["PRD-0102", "Cemento Portland Tipo I 42.5 kg", "120", "S/ 29.50", "S/ 3,540.00"],
             ["PRD-0215", "Fierro corrugado 1/2\" x 9 m", "80", "S/ 38.90", "S/ 3,112.00"],
             ["PRD-0333", "Ladrillo King Kong 18 huecos (millar)", "3", "S/ 1,150.00", "S/ 3,450.00"]]
    stock = [["Cemento Portland 42.5 kg", "1,840", "500", chip("Éxito").replace("Éxito", "Normal")],
             ["Fierro 1/2\" x 9 m", "260", "300", chip("Reintento").replace("Reintento", "Stock bajo")],
             ["Ladrillo King Kong", "42", "20", chip("Éxito").replace("Éxito", "Normal")],
             ["Arena gruesa m³", "18", "25", chip("Rechazado").replace("Rechazado", "Reponer")]]
    docs = [["F001-00012845", "Constructora Andina SAC", "S/ 11,906.72", chip("Aceptado SUNAT")],
            ["B001-00045122", "Cliente varios", "S/ 236.00", chip("Aceptado SUNAT")],
            ["F001-00012844", "Inversiones Del Sur EIRL", "S/ 4,520.00", chip("Enviado")]]
    cuerpo = kpis([("Ventas del día", "S/ 18,742", "▲ 9% vs ayer"), ("Comprobantes emitidos", "64", "Facturas y boletas"),
                   ("Aceptados por SUNAT", "100%", "Envío automático"), ("Productos con stock bajo", "7", "Alerta de reposición")])
    cuerpo += f"""<div class="row"><div class="card grow"><h2>Factura electrónica F001-00012845 <span class="chip ok">Aceptado SUNAT</span></h2>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:14px">
    <div class="field">Cliente<div class="input">Constructora Andina SAC</div></div>
    <div class="field">RUC<div class="input">20xxxxxxx81</div></div><div class="field">Forma de pago<div class="input">Crédito 30 días</div></div></div>
    {tabla(["Código", "Descripción", "Cant.", "P. unit.", "Importe"], items, derecha=(2, 3, 4))}
    <div style="display:flex;justify-content:flex-end;margin-top:12px;gap:28px;font-size:13px"><span>Op. gravada <b>S/ 10,090.44</b></span><span>IGV 18% <b>S/ 1,816.28</b></span><span style="font-size:15px">Total <b>S/ 11,906.72</b></span></div>
    <div style="display:flex;gap:8px;margin-top:14px"><span class="btn2">📄 PDF</span><span class="btn2">XML</span><span class="btn2">CDR</span><span class="btn2">Enviar por WhatsApp</span></div></div>
    <div style="width:430px;display:flex;flex-direction:column;gap:18px">
    <div class="card"><h2>Inventario · Almacén central</h2>{tabla(["Producto", "Stock", "Mín.", "Estado"], stock, derecha=(1, 2))}</div>
    <div class="card"><h2>Últimos comprobantes</h2>{tabla(["Serie", "Cliente", "Total", "SUNAT"], docs, derecha=(2,))}</div></div></div>"""
    return app("Facturación", "Inventario y facturación electrónica", "Ventas / Facturación electrónica", cuerpo)


def bots():
    css = """.flow{display:flex;align-items:center;gap:0;padding:26px 6px}
    .node{background:#fff;border:1.5px solid #CBD5E1;border-radius:12px;padding:14px 16px;width:200px;font-size:12.5px;color:#475569}
    .node b{display:block;color:#0B1E3F;font-size:13.5px;margin:4px 0}
    .node.t{border-color:#F97316;background:#FFF7ED}.node.e{border-color:#16A34A;background:#F0FDF4}
    .arr{flex:1;height:2px;background:#94A3B8;position:relative;min-width:24px}
    .arr:after{content:'';position:absolute;right:-1px;top:-4px;border:5px solid transparent;border-left-color:#94A3B8}
    .tag{font-size:10.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#94A3B8}"""
    log = [["13/11 08:00:02", "Descarga de reporte del portal bancario", "18 s", chip("Éxito")],
           ["13/11 08:00:20", "Lectura de 214 movimientos", "3 s", chip("Éxito")],
           ["13/11 08:00:23", "Registro en ERP y conciliación", "41 s", chip("Éxito")],
           ["13/11 08:01:04", "Envío de resumen por correo y WhatsApp", "2 s", chip("Éxito")],
           ["12/11 08:00:01", "Descarga de reporte del portal bancario", "1 min", chip("Reintento")]]
    bots_ = [["Bot de conciliación diaria", "Todos los días 8:00 a. m.", "98.9%", chip("Éxito").replace("Éxito", "Activo")],
             ["Bot de cobranza por WhatsApp", "Lun a vie 9:00 a. m.", "100%", chip("Éxito").replace("Éxito", "Activo")],
             ["Descarga de comprobantes SUNAT", "Cada 6 horas", "97.4%", chip("Éxito").replace("Éxito", "Activo")],
             ["Consolidado de ventas a Excel", "Viernes 6:00 p. m.", "100%", chip("Enviado").replace("Enviado", "Programado")]]
    cuerpo = kpis([("Bots activos", "12", "Trabajando 24/7"), ("Tareas ejecutadas (mes)", "8,940", "Sin intervención manual"),
                   ("Horas ahorradas (mes)", "186 h", "≈ 1 colaborador a tiempo completo"), ("Tasa de éxito", "99.2%", "Con reintentos automáticos")])
    cuerpo += f"""<div class="card"><h2>Flujo · Bot de conciliación diaria <span class="chip ok">Activo</span></h2><div class="flow">
    <div class="node t"><span class="tag">Disparador</span><b>⏰ Todos los días 8:00</b>Se ejecuta solo, sin abrir la PC</div><div class="arr"></div>
    <div class="node"><span class="tag">Paso 1</span><b>🏦 Portal bancario</b>Descarga el extracto del día</div><div class="arr"></div>
    <div class="node"><span class="tag">Paso 2</span><b>⚙️ Procesa y valida</b>Cruza contra facturas y pagos</div><div class="arr"></div>
    <div class="node"><span class="tag">Paso 3</span><b>🗂️ Registra en ERP</b>Marca lo conciliado</div><div class="arr"></div>
    <div class="node e"><span class="tag">Fin</span><b>📲 Notifica</b>Resumen por correo y WhatsApp</div></div></div>
    <div class="row"><div class="card grow"><h2>Mis bots</h2>{tabla(["Bot", "Programación", "Éxito", "Estado"], bots_, derecha=(2,))}</div>
    <div class="card grow"><h2>Registro de ejecución</h2>{tabla(["Hora", "Acción", "Duración", "Resultado"], log, derecha=(2,))}</div></div>"""
    return app("Automatizaciones", "Bots y automatizaciones", "Operaciones / Automatizaciones", cuerpo, css)


def bi():
    meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov"]
    ventas = [62, 58, 71, 69, 77, 74, 82, 88, 85, 93, 98]
    meta = [65, 65, 70, 70, 75, 75, 80, 80, 85, 85, 90]
    bw, gap, h0 = 46, 18, 230
    barras = "".join(f'<rect x="{40 + i * (bw + gap)}" y="{h0 - v * 2}" width="{bw}" height="{v * 2}" rx="6" fill="{"#F97316" if i == len(ventas) - 1 else "#1D4ED8"}"/>'
                     f'<text x="{40 + i * (bw + gap) + bw / 2}" y="{h0 + 18}" font-size="11" fill="#64748B" text-anchor="middle">{m}</text>'
                     for i, (v, m) in enumerate(zip(ventas, meses)))
    linea = " ".join(f"{40 + i * (bw + gap) + bw / 2},{h0 - v * 2}" for i, v in enumerate(meta))
    svg = (f'<svg width="100%" viewBox="0 0 760 250">'
           + "".join(f'<line x1="30" x2="750" y1="{h0 - k * 2}" y2="{h0 - k * 2}" stroke="#F1F5F9"/>' for k in (25, 50, 75, 100))
           + barras + f'<polyline points="{linea}" fill="none" stroke="#0B1E3F" stroke-width="2" stroke-dasharray="5 4"/></svg>')
    areas = [("Lima", 42, "#1D4ED8"), ("Arequipa", 19, "#3B82F6"), ("Trujillo", 15, "#60A5FA"), ("Piura", 13, "#93C5FD"), ("Otros", 11, "#CBD5E1")]
    acc, segs = 0, ""
    for _, p, c in areas:
        segs += f'<circle r="70" cx="90" cy="90" fill="none" stroke="{c}" stroke-width="34" stroke-dasharray="{p * 4.398:.1f} 439.8" stroke-dashoffset="{-acc * 4.398:.1f}" transform="rotate(-90 90 90)"/>'
        acc += p
    dona = (f'<div style="display:flex;align-items:center;gap:20px"><svg width="180" height="180">{segs}</svg><div style="font-size:12.5px;display:flex;flex-direction:column;gap:8px">'
            + "".join(f'<div><span style="display:inline-block;width:10px;height:10px;border-radius:3px;background:{c};margin-right:8px"></span>{n} <b>{p}%</b></div>' for n, p, c in areas)
            + "</div></div>")
    top = [["Línea Construcción", "S/ 412,300", "▲ 14%"], ["Línea Educación", "S/ 286,900", "▲ 9%"],
           ["Servicios", "S/ 164,200", "▲ 21%"], ["Retail", "S/ 98,450", "▼ 3%"]]
    cuerpo = """<div class="row" style="gap:10px"><span class="btn2">Periodo: 2026</span><span class="btn2">Sede: Todas</span><span class="btn2">Línea: Todas</span><div class="grow"></div><span class="chip ok" style="align-self:center">Actualizado hoy 07:00</span></div>"""
    cuerpo += kpis([("Ventas acumuladas", "S/ 961,850", "▲ 16% vs 2025"), ("Margen bruto", "34.8%", "▲ 2.1 pts"),
                    ("Ticket promedio", "S/ 1,284", "▲ 6%"), ("Cumplimiento de meta", "108%", "Noviembre")])
    cuerpo += f"""<div class="row"><div class="card grow"><h2>Ventas mensuales vs meta (miles S/) </h2>{svg}</div>
    <div class="card" style="width:400px"><h2>Ventas por sede</h2>{dona}</div></div>
    <div class="card"><h2>Ranking por línea de negocio</h2>{tabla(["Línea", "Ventas", "Variación"], top, derecha=(1, 2))}</div>"""
    return app("Reportes BI", "Reportes en BI · Gerencia", "Reportes / Tablero gerencial", cuerpo)


def web():
    return f"""<!doctype html><html><head><meta charset="utf-8">{FUENTES}<style>
*{{box-sizing:border-box;margin:0;padding:0}}body{{width:1440px;height:900px;font-family:Inter,Segoe UI,sans-serif;background:#E2E8F0;padding:34px 60px;overflow:hidden}}
.win{{background:#fff;border-radius:14px;box-shadow:0 30px 60px #0f172a26;overflow:hidden;height:832px}}
.bar{{height:42px;background:#F1F5F9;display:flex;align-items:center;gap:8px;padding:0 16px;border-bottom:1px solid #E2E8F0}}
.d{{width:12px;height:12px;border-radius:50%}}.url{{margin-left:20px;background:#fff;border-radius:6px;padding:5px 14px;font-size:12.5px;color:#64748B;width:420px}}
nav{{display:flex;justify-content:space-between;align-items:center;padding:20px 56px}}
.lg{{font:700 22px 'Space Grotesk',sans-serif;color:#14532D}}.lk{{display:flex;gap:28px;font-size:14px;color:#334155}}
.hero{{display:grid;grid-template-columns:1.1fr 1fr;gap:40px;padding:36px 56px;align-items:center}}
h1{{font:700 52px/1.05 'Space Grotesk',sans-serif;color:#0F172A}}h1 span{{color:#16A34A}}
p{{color:#475569;font-size:17px;line-height:1.6;margin:18px 0 26px}}
.b{{display:inline-block;background:#16A34A;color:#fff;padding:13px 22px;border-radius:10px;font-weight:600;margin-right:10px}}
.b2{{display:inline-block;border:1.5px solid #CBD5E1;padding:12px 22px;border-radius:10px;font-weight:600;color:#0F172A}}
.img{{height:360px;border-radius:20px;background:linear-gradient(135deg,#BBF7D0,#86EFAC 45%,#22C55E);position:relative;overflow:hidden}}
.img:before{{content:'';position:absolute;width:260px;height:260px;border-radius:50%;background:#ffffff55;right:-40px;top:-40px}}
.img:after{{content:'';position:absolute;width:200px;height:120px;border-radius:16px;background:#fff;left:30px;bottom:30px;box-shadow:0 10px 30px #0002}}
.cards{{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;padding:10px 56px}}
.c{{border:1px solid #E2E8F0;border-radius:14px;padding:18px}}.c b{{display:block;font-size:15px;margin:10px 0 6px}}.c small{{color:#64748B;font-size:13px}}
.ic{{width:38px;height:38px;border-radius:10px;background:#DCFCE7}}
.wa{{position:absolute;right:96px;bottom:70px;width:56px;height:56px;border-radius:50%;background:#25D366;box-shadow:0 8px 20px #0003}}
</style></head><body><div class="win"><div class="bar"><span class="d" style="background:#F87171"></span><span class="d" style="background:#FBBF24"></span><span class="d" style="background:#34D399"></span><span class="url">🔒 www.tunegocio.pe</span></div>
<nav><span class="lg">🌿 Tu Negocio</span><div class="lk"><span>Inicio</span><span>Servicios</span><span>Nosotros</span><span>Blog</span><span>Contacto</span></div><span class="b" style="margin:0;padding:10px 18px">Reservar cita</span></nav>
<div class="hero"><div><h1>Tu marca, <span>visible</span> y vendiendo las 24 horas</h1><p>Sitio web rápido, adaptable a celulares, con formulario de contacto, botón de WhatsApp, catálogo y posicionamiento en Google.</p>
<span class="b">Ver catálogo</span><span class="b2">Escríbenos</span></div><div class="img"></div></div>
<div class="cards"><div class="c"><div class="ic"></div><b>Catálogo en línea</b><small>Productos con precios y fotos</small></div><div class="c"><div class="ic"></div><b>Reservas</b><small>Agenda de citas automática</small></div>
<div class="c"><div class="ic"></div><b>Pagos</b><small>Yape, Plin y tarjetas</small></div><div class="c"><div class="ic"></div><b>SEO</b><small>Aparece en Google</small></div></div>
</div><div class="wa"></div></body></html>"""


PANTALLAS = {"viaticos": viaticos, "conciliacion": conciliacion, "matricula": matricula, "whatsapp": whatsapp,
             "inventario-facturacion": facturacion, "bots": bots, "reportes-bi": bi, "paginas-web": web}


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for nombre, fn in PANTALLAS.items():
            html = pathlib.Path(tmp) / f"{nombre}.html"
            png = pathlib.Path(tmp) / f"{nombre}.png"
            html.write_text(fn(), encoding="utf-8")
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                            f"--window-size={W},{H}", "--virtual-time-budget=4000",
                            f"--screenshot={png}", html.as_uri()], check=True, capture_output=True)
            Image.open(png).convert("RGB").save(SALIDA / f"{nombre}.webp", "WEBP", quality=86, method=6)
            print("ok", nombre)


if __name__ == "__main__":
    main()
