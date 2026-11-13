# Web ConiTech

Sitio estático (HTML + CSS + JS, sin dependencias ni build). Se publica subiendo la carpeta tal cual
(Netlify, Vercel, GitHub Pages, Hostinger, cPanel…).

```
index.html            Página única con todas las secciones
css/styles.css        Estilos (variables de marca al inicio)
js/main.js            Menú móvil, pestañas, visor de capturas, formulario → WhatsApp
assets/img/marca/     Favicon, icono e imagen para redes (og-image)
assets/img/clientes/  Logos de clientes
assets/img/capturas/  Capturas de los módulos (.webp, 1440×900)
_capturas-fuente/     Script que genera las capturas de muestra (no se publica)
imagenes/             Originales que entregaste (no se publica)
```

## Reemplazar capturas por pantallazos reales
Las capturas actuales son maquetas con datos de ejemplo. Para usar las reales, guarda tu pantallazo
con el **mismo nombre** en `assets/img/capturas/` (ej. `viaticos.webp`). Si es PNG/JPG, cambia la
extensión también en `index.html`. Tamaño recomendado: 1440×900 (proporción 16:10).
Tapa o difumina datos sensibles de tus clientes antes de publicarlas.

## Cambiar el número de WhatsApp
Busca `51941393854` en `index.html` y en `js/main.js`.

## Vista previa local
```
python -m http.server 5510
```
y abre http://localhost:5510
