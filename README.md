# LWIW-Traduccion-Espanol

Codigo fuente abierto de la traduccion al espanol (no oficial) de **Little Witch in the
Woods**. Este repositorio existe para que cualquiera pueda revisar exactamente que hace
el instalador antes de ejecutarlo — no distribuye archivos binarios del juego, solo
texto traducido y un script en Python que lo aplica sobre tu propia copia legal del
juego.

La pagina del mod (con instrucciones para el publico general) esta en Nexus Mods.

Traduccion hecha con ayuda de Claude (Anthropic): las decisiones de glosario, tono,
genero de personajes y el criterio de que se traduce o no fueron humanas; el grueso del
texto de los ~39.000 dialogos fue redactado por el modelo bajo esa direccion y revisado
por lotes.

---

# Traduccion al espanol (no oficial) — Little Witch in the Woods

Traduccion fan-made, completa, de **Little Witch in the Woods** al espanol: interfaz
completa y los ~39.000 dialogos de todos los personajes. No es una traduccion automatica:
esta hecha a mano, cuidando el tono y la voz de cada personaje.

No afiliada a los desarrolladores. Uso bajo tu propia responsabilidad — aunque el
instalador no toca tus partidas guardadas, haz una copia de tus saves si quieres ir
sobre seguro antes de instalar nada.

## Que traduce

- **Interfaz completa** (menus, objetos, misiones, enciclopedia, tutoriales, correo...).
- **Todos los dialogos** de personajes: historia principal y secundarias.

Los nombres propios (Ellie, Virgil, Wisteria, etc.) se dejan sin traducir a proposito.

## Requisitos

- Windows (el juego solo esta disponible para Windows).
- [Python 3.10 o mas nuevo](https://www.python.org/downloads/) instalado y accesible
  desde la terminal (al instalarlo, marca la casilla **"Add Python to PATH"**).
- Conexion a internet la primera vez, para instalar una libreria (`UnityPy`).

## Instalacion

1. Descarga este repositorio (boton **Code > Download ZIP**, o `git clone`) y pegalo
   donde quieras (no hace falta que este dentro de la carpeta del juego).
2. Abre una terminal en esta carpeta y ejecuta una vez:
   ```
   pip install -r requirements.txt
   ```
3. Ejecuta:
   ```
   python instalar.py
   ```
   (o haz doble clic en `instalar.bat`)
   - El instalador intenta encontrar tu instalacion de Steam automaticamente.
   - Si no la encuentra, te pedira que pegues la ruta de la carpeta del juego
     (la que contiene `LWIW.exe`), por ejemplo:
     `E:\SteamLibrary\steamapps\common\Little Witch in the Woods`
4. Espera a que termine (tarda menos de un minuto) y abre el juego. Deberia verse
   todo en espanol desde el menu principal.

La primera vez que lo ejecutas, el instalador guarda una copia de seguridad de los
archivos originales en ingles dentro de la carpeta `_backup_original\` (junto a este
script). Gracias a eso, **puedes volver a ejecutar el instalador cuantas veces quieras**
sin miedo a acumular errores: siempre parte de esa copia limpia.

## Si Steam actualiza el juego

Las actualizaciones de Steam sobrescriben los archivos traducidos y el juego vuelve a
mostrarse en ingles. Para arreglarlo:

```
python instalar.py --actualizar-backup
```

Esto le dice al instalador "los archivos que Steam acaba de poner son la nueva version
en ingles, guardalos como referencia" y luego vuelve a aplicar la traduccion sobre ellos.
**Usa esta opcion unicamente justo despues de una actualizacion** (no en una instalacion
normal), porque si la usas cuando el juego ya esta en espanol, guardaria el espanol como
si fuera el "original" y perderias la referencia al ingles.

Como el emparejamiento de textos es por identificador interno (no por posicion en el
archivo), la traduccion sobrevive a la mayoria de actualizaciones sin necesidad de
retraducir nada — si acaso, alguna linea nueva que el update haya anadido se queda en
ingles hasta la siguiente version de este paquete.

## Para volver al ingles original

```
python instalar.py --restaurar
```

o haz doble clic en **`restaurar.bat`**.

## Notas tecnicas

- El juego no trae tildes/eñes en el atlas de fuentes, pero las renderiza igualmente
  via su sistema de fallback de fuentes — se ven bien en pantalla (`Configuración`,
  `Créditos`, `ñá¿¡éíúü`).
- El instalador no modifica partidas guardadas, solo los archivos de texto del juego
  (`localization-string-tables-english(en)_assets_all.bundle` y
  `dialoguedb_assets_all.bundle`, dentro de `LWIW_Data\StreamingAssets\aa\StandaloneWindows64\`).
- Si algo sale mal, `python instalar.py --restaurar` deja el juego exactamente como
  estaba antes de instalar nada.
- Edicion de los bundles con [UnityPy](https://github.com/K0lb3/UnityPy).

## Problemas conocidos / si algo no funciona

- Si el instalador no encuentra el juego automaticamente, pega la ruta manualmente
  cuando te la pida (o usa `python instalar.py --ruta "TU_RUTA_AQUI"`).
- Si `pip install -r requirements.txt` falla, prueba `pip install UnityPy==1.25.3`
  directamente.

## Licencia

Traduccion y script publicados libremente para la comunidad. No redistribuye archivos
del juego, solo texto traducido y codigo propio.
