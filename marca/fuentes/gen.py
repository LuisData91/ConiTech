"""Genera las fuentes HTML/SVG del kit oficial de marca ConiTech (opción 1: Azul marino + Naranja)."""
NAVY_A, NAVY_B, ORANGE = '#0B2A5B', '#1E40AF', '#F97316'
TXT, TECH, SUB = '#0B1E3F', '#1D4ED8', '#475569'
LIGHT_A, LIGHT_B, TECH_DARK, SUB_DARK = '#3B82F6', '#1D4ED8', '#60A5FA', '#CBD5E1'
BG_DARK = '#0B1220'

def icon(a=NAVY_A, b=NAVY_B, gid='g'):
    blocks = ''.join(f'<rect x="{x}" y="{y}" width="46" height="46" rx="12"/>' for x, y in
                     [(30,30),(85,30),(140,30),(30,85),(30,140),(85,140),(140,140)])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">'
            f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/>'
            f'<stop offset="1" stop-color="{b}"/></linearGradient></defs><g fill="url(#{gid})">{blocks}</g>'
            f'<rect x="150" y="85" width="46" height="46" rx="12" fill="{ORANGE}" transform="rotate(14 173 108)"/>'
            f'<rect x="128" y="104" width="12" height="6" rx="3" fill="{ORANGE}" opacity=".55"/>'
            f'<rect x="112" y="104" width="8" height="6" rx="3" fill="{ORANGE}" opacity=".3"/></svg>')

CSS = '''<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@600&display=block" rel="stylesheet">
<style>html,body{margin:0;background:transparent}
.w{display:flex;align-items:center;justify-content:center;gap:34px;width:1500px;height:300px}
.i svg{width:150px;height:150px;display:block}
.n{font:700 104px 'Space Grotesk';letter-spacing:-3px;line-height:1}
.bar{width:4px;height:96px;border-radius:2px;background:#F97316}
.s{font:600 40px 'Inter';line-height:1.15;letter-spacing:.5px}
.sq{display:grid;place-items:center;width:540px;height:540px}.sq svg{width:400px;height:400px;transform:translateX(-26px)}
</style>'''
page = lambda body: f'<!doctype html><html><head><meta charset="utf-8">{CSS}</head><body>{body}</body></html>'
def logo(dark=False):
    ic = icon(LIGHT_A, LIGHT_B, 'gd') if dark else icon()
    c1, c2, sub = ('#FFFFFF', TECH_DARK, SUB_DARK) if dark else (TXT, TECH, SUB)
    return (f'<div class="w"><div class="i">{ic}</div><div class="n" style="color:{c1}">Coni<span style="color:{c2}">Tech</span></div>'
            f'<div class="bar"></div><div class="s" style="color:{sub}">Software &amp;<br>Automation</div></div>')
files = {
  'logo-claro':  page(logo()),                                            # transparente, para fondos claros
  'logo-blanco': page(logo(True)),                                        # transparente, para fondos oscuros
  'logo-fondo-oscuro': page(f'<div style="background:{BG_DARK}">{logo(True)}</div>'),
  'icono': page(f'<div class="sq" style="width:512px;height:512px"><div style="width:512px;height:512px">{icon()}</div></div>').replace('.sq svg{width:400px;height:400px;transform:translateX(-26px)}','.sq svg{width:512px;height:512px}'),
  'perfil-claro': page(f'<div class="sq" style="background:#fff">{icon()}</div>'),
  'perfil-oscuro': page(f'<div class="sq" style="background:{BG_DARK}">{icon(LIGHT_A, LIGHT_B, "gd")}</div>'),
}
for name, html in files.items():
    open(f'{name}.html', 'w', encoding='utf8').write(html)
open('icono.svg', 'w', encoding='utf8').write(icon())

# --- Versión apilada (icono arriba, "ConiTech" abajo) para redes sociales ---
# El contenido se mantiene dentro del área segura del recorte circular de las redes.
STACK_CSS = '''<style>.st{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px}
.st svg{width:190px;height:190px;display:block;transform:translateX(-12px)}
.st .n{font-size:76px;letter-spacing:-2px}</style>'''
def stack(dark=False, size=540, bg='transparent'):
    ic = icon(LIGHT_A, LIGHT_B, 'gs') if dark else icon(gid='gs')
    c1, c2 = ('#FFFFFF', TECH_DARK) if dark else (TXT, TECH)
    return (f'{STACK_CSS}<div class="st" style="width:{size}px;height:{size}px;background:{bg}">{ic}'
            f'<div class="n" style="color:{c1}">Coni<span style="color:{c2}">Tech</span></div></div>')
stacked = {
  'redes-perfil-claro':  page(stack(False, bg='#FFFFFF')),
  'redes-perfil-oscuro': page(stack(True,  bg=BG_DARK)),
  'logo-apilado-claro':  page(stack(False)),
  'logo-apilado-blanco': page(stack(True)),
}
for name, html in stacked.items():
    open(f'{name}.html', 'w', encoding='utf8').write(html)
