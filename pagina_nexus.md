# Borrador para la pagina de Nexus Mods

(Esto no se distribuye con el mod — es solo para copiar y pegar al crear la pagina.)

## Titulo sugerido
Traduccion al Espanol (No Oficial) / Spanish Translation (Unofficial)

## Resumen corto (summary)
Traduccion fan-made completa al espanol: toda la interfaz y los ~39.000 dialogos de
personajes, traducidos a mano cuidando el tono de cada personaje. No es traduccion
automatica.

## Descripcion completa

**Little Witch in the Woods no tiene espanol oficial.** Esta es una traduccion fan-made
completa y no oficial, hecha a mano (no con traduccion automatica), que cubre:

- La interfaz completa del juego: menus, objetos, misiones, enciclopedia, correo,
  tutoriales...
- **Los ~39.000 dialogos** de todos los personajes de la historia principal y las
  secundarias.

Los nombres propios (Ellie, Virgil, Wisteria, etc.) se dejan sin traducir a proposito.

### Como funciona

En vez de repartir los archivos del juego ya modificados, este mod incluye un pequeno
instalador en Python que aplica la traduccion sobre TU PROPIA copia del juego,
emparejando cada texto por su identificador interno (no por su posicion). Eso tiene una
ventaja importante: **cuando el juego reciba una actualizacion, no hay que esperar a un
nuevo mod** — basta con volver a ejecutar el instalador para que la traduccion se
reaplique sobre los textos nuevos.

### Instalacion

1. Instala [Python 3.10+](https://www.python.org/downloads/) si no lo tienes (marca
   "Add Python to PATH" durante la instalacion).
2. Descarga y descomprime este mod en cualquier carpeta.
3. Abre una terminal ahi y ejecuta `pip install -r requirements.txt` (una sola vez).
4. Haz doble clic en `instalar.bat`.

Instrucciones completas, como revertir a ingles, y que hacer tras una actualizacion de
Steam: ver `LEEME.md` dentro del archivo descargado.

### Codigo fuente
https://github.com/mbmarlon/LWIW-Traduccion-Espanol (repo publico — el instalador es
texto plano, revisable antes de ejecutarlo).

### Requisitos
- Windows
- Python 3.10 o superior

### Compatibilidad
Compatible con la version actual del juego (build verificado: 7.0.3.0). Si el juego
recibe una actualizacion y algun texto vuelve a aparecer en ingles, vuelve a ejecutar
el instalador con `--actualizar-backup` (ver LEEME.md).

### Creditos
Traduccion: [TU NOMBRE / NICK AQUI] — decisiones de glosario, tono y direccion.
Redaccion del grueso del texto asistida por Claude (Anthropic).

## Etiqueta de IA obligatoria en Nexus
Marcar como **"AI-Generated Content"** (no "AI Assisted" — esa es solo para "limited AI
involvement" y Nexus puede pedirte que demuestres desarrollo humano si la usas mal).
"AI-Generated Content" incluye explicitamente "translations" en su propia definicion,
asi que es la etiqueta correcta aqui. No es un mod prohibido: Nexus permite contenido
con IA, solo exige que se etiquete bien.

## Categoria sugerida
Traducciones / Translations

## Etiquetas sugeridas
spanish, espanol, translation, traduccion, localization, texto, dialogo
