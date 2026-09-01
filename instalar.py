#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instalador de la traduccion al espanol (fan-made) de Little Witch in the Woods.

Que hace:
  1. Localiza tu instalacion del juego (auto-detecta o te la pide).
  2. La primera vez, guarda una copia de seguridad de los bundles originales
     en ingles dentro de esta misma carpeta (_backup_original\\).
  3. Aplica la traduccion (textos de interfaz + dialogos de personajes) sobre
     esa copia de seguridad y escribe el resultado en tu carpeta del juego.

Como el emparejamiento es por ID (no por posicion), sobrevive a actualizaciones
del juego: si Steam actualiza LWIW, basta con volver a ejecutar este script.

Uso:
  python instalar.py                    Instala/reaplica la traduccion
  python instalar.py --ruta "C:\\...\\Little Witch in the Woods"
                                         Indica la carpeta del juego a mano
  python instalar.py --actualizar-backup
                                         Usalo SOLO justo despues de que Steam
                                         actualice el juego (antes de aplicar,
                                         refresca la copia de seguridad con los
                                         bundles nuevos que Steam acaba de poner)
  python instalar.py --restaurar        Devuelve el juego a su ingles original
"""
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

MOD_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(MOD_DIR, "data")
BACKUP_DIR = os.path.join(MOD_DIR, "_backup_original")
REL_BUNDLES = os.path.join("LWIW_Data", "StreamingAssets", "aa", "StandaloneWindows64")

BUNDLE_UI = "localization-string-tables-english(en)_assets_all.bundle"
BUNDLE_DLG = "dialoguedb_assets_all.bundle"


def log(msg):
    print(msg)


# ---------------------------------------------------------------------------
# 1. Localizar la carpeta del juego
# ---------------------------------------------------------------------------

def es_carpeta_de_juego_valida(ruta):
    return os.path.isfile(os.path.join(ruta, REL_BUNDLES, BUNDLE_UI)) and \
        os.path.isfile(os.path.join(ruta, REL_BUNDLES, BUNDLE_DLG))


def candidatos_steam():
    """Busca 'Little Witch in the Woods' en todas las bibliotecas de Steam."""
    rutas = []
    steam_paths = set()

    if sys.platform == "win32":
        try:
            import winreg
            for hive, subkey in (
                (winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam"),
            ):
                try:
                    with winreg.OpenKey(hive, subkey) as k:
                        val, _ = winreg.QueryValueEx(k, "SteamPath" if hive == winreg.HKEY_CURRENT_USER else "InstallPath")
                        steam_paths.add(os.path.normpath(val))
                except OSError:
                    continue
        except ImportError:
            pass

    for base in ("C:\\Program Files (x86)\\Steam", "C:\\Program Files\\Steam"):
        if os.path.isdir(base):
            steam_paths.add(base)

    libraryfolders_encontrados = set()
    for sp in steam_paths:
        lf = os.path.join(sp, "steamapps", "libraryfolders.vdf")
        if os.path.isfile(lf):
            libraryfolders_encontrados.add(lf)

    bibliotecas = set(steam_paths)
    for lf in libraryfolders_encontrados:
        try:
            with open(lf, encoding="utf-8", errors="ignore") as f:
                contenido = f.read()
            for linea in contenido.splitlines():
                linea = linea.strip()
                if linea.startswith('"path"'):
                    partes = linea.split('"')
                    if len(partes) >= 4:
                        bibliotecas.add(partes[3].replace("\\\\", "\\"))
        except OSError:
            continue

    for b in bibliotecas:
        candidato = os.path.join(b, "steamapps", "common", "Little Witch in the Woods")
        rutas.append(os.path.normpath(candidato))

    # Fallback: unidades comunes, por si libraryfolders.vdf no aparecio
    for letra in "CDEFGH":
        for sub in ("SteamLibrary\\steamapps\\common", "Steam\\steamapps\\common", "Program Files (x86)\\Steam\\steamapps\\common"):
            rutas.append(f"{letra}:\\{sub}\\Little Witch in the Woods")

    vistos = set()
    unicos = []
    for r in rutas:
        rn = os.path.normpath(r)
        if rn not in vistos:
            vistos.add(rn)
            unicos.append(rn)
    return unicos


def localizar_juego(ruta_manual=None):
    if ruta_manual:
        if es_carpeta_de_juego_valida(ruta_manual):
            return ruta_manual
        log(f"ERROR: no encuentro los bundles del juego en '{ruta_manual}'.")
        log("Verifica que sea la carpeta que contiene LWIW.exe.")
        sys.exit(1)

    for candidato in candidatos_steam():
        if es_carpeta_de_juego_valida(candidato):
            log(f"Juego encontrado automaticamente en: {candidato}")
            return candidato

    log("No pude localizar el juego automaticamente.")
    log("Pega la ruta completa de la carpeta donde esta LWIW.exe")
    log(r'(ejemplo: E:\SteamLibrary\steamapps\common\Little Witch in the Woods)')
    while True:
        ruta = input("> ").strip().strip('"')
        if es_carpeta_de_juego_valida(ruta):
            return ruta
        log("Esa carpeta no parece ser la del juego (no encuentro los bundles esperados). Intenta de nuevo.")


# ---------------------------------------------------------------------------
# 2. Copia de seguridad
# ---------------------------------------------------------------------------

def asegurar_backup(juego_dir, refrescar=False):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    origen = os.path.join(juego_dir, REL_BUNDLES)
    for nombre in (BUNDLE_UI, BUNDLE_DLG):
        destino = os.path.join(BACKUP_DIR, nombre)
        if refrescar or not os.path.isfile(destino):
            with open(os.path.join(origen, nombre), "rb") as fsrc, open(destino, "wb") as fdst:
                fdst.write(fsrc.read())
            log(f"  copia de seguridad guardada: {nombre}")


def backup_existe():
    return os.path.isfile(os.path.join(BACKUP_DIR, BUNDLE_UI)) and \
        os.path.isfile(os.path.join(BACKUP_DIR, BUNDLE_DLG))


# ---------------------------------------------------------------------------
# 3. Aplicar traduccion
# ---------------------------------------------------------------------------

def aplicar_interfaz(juego_dir):
    import UnityPy
    with open(os.path.join(DATA_DIR, "memoria_traduccion.json"), encoding="utf-8") as f:
        memoria = json.load(f)

    env = UnityPy.load(os.path.join(BACKUP_DIR, BUNDLE_UI))
    aplicadas = 0
    pendientes = 0
    for obj in env.objects:
        if obj.type.name != "MonoBehaviour":
            continue
        tree = obj.read_typetree()
        tabla = tree.get("m_Name", "")
        d = memoria.get(tabla, {})
        cambiadas = 0
        for e in tree.get("m_TableData", []):
            en = e.get("m_Localized", "")
            if not en.strip():
                continue
            es = d.get(str(e["m_Id"]))
            if es is None:
                pendientes += 1
            elif es != en:
                e["m_Localized"] = es
                cambiadas += 1
        if cambiadas:
            obj.save_typetree(tree)
            aplicadas += cambiadas

    destino = os.path.join(juego_dir, REL_BUNDLES, BUNDLE_UI)
    with open(destino, "wb") as f:
        f.write(env.file.save(packer="lz4"))
    log(f"Interfaz: {aplicadas} cadenas traducidas aplicadas ({pendientes} sin traducir, se quedan en ingles)")


def aplicar_dialogos(juego_dir):
    import UnityPy
    with open(os.path.join(DATA_DIR, "memoria_dialogos.json"), encoding="utf-8") as f:
        memoria = json.load(f)

    env = UnityPy.load(os.path.join(BACKUP_DIR, BUNDLE_DLG))
    objetivo = None
    for obj in env.objects:
        if obj.type.name != "MonoBehaviour":
            continue
        tree = obj.read_typetree()
        if tree.get("m_Name") == "DialogueDB_en":
            objetivo = (obj, tree)
            break
    if objetivo is None:
        log("ERROR: no encuentro DialogueDB_en dentro del bundle de dialogos.")
        return
    obj, tree = objetivo

    por_texto = {}
    for c in tree.get("conversations", []):
        cid = c["id"]
        for e in c.get("dialogueEntries", []):
            clave = f"{cid}:{e['id']}"
            if clave not in memoria:
                continue
            for f in e.get("fields", []):
                if f.get("title") == "en" and f.get("value", "").strip():
                    por_texto.setdefault(f["value"], memoria[clave])

    aplicadas = 0
    reutilizadas = 0
    sin_traducir = 0
    for c in tree.get("conversations", []):
        cid = c["id"]
        for e in c.get("dialogueEntries", []):
            clave = f"{cid}:{e['id']}"
            for f in e.get("fields", []):
                if f.get("title") != "en":
                    continue
                en = f.get("value", "")
                if not en.strip():
                    continue
                es = memoria.get(clave)
                if es is None:
                    es = por_texto.get(en)
                    if es is not None:
                        reutilizadas += 1
                if es is None:
                    sin_traducir += 1
                elif es != en:
                    f["value"] = es
                    aplicadas += 1

    obj.save_typetree(tree)
    destino = os.path.join(juego_dir, REL_BUNDLES, BUNDLE_DLG)
    with open(destino, "wb") as f:
        f.write(env.file.save(packer="lz4"))
    total = aplicadas + sin_traducir
    pct = (aplicadas * 100 // total) if total else 100
    log(f"Dialogos: {aplicadas} lineas aplicadas ({reutilizadas} reutilizadas de repeticiones), "
        f"{sin_traducir} sin traducir todavia ({pct}% del dialogo en espanol)")


# ---------------------------------------------------------------------------
# 4. Restaurar ingles original
# ---------------------------------------------------------------------------

def restaurar(juego_dir):
    if not backup_existe():
        log("No hay copia de seguridad guardada todavia; no hay nada que restaurar.")
        sys.exit(1)
    destino_dir = os.path.join(juego_dir, REL_BUNDLES)
    for nombre in (BUNDLE_UI, BUNDLE_DLG):
        with open(os.path.join(BACKUP_DIR, nombre), "rb") as fsrc, \
             open(os.path.join(destino_dir, nombre), "wb") as fdst:
            fdst.write(fsrc.read())
        log(f"  restaurado: {nombre}")
    log("Juego devuelto a su version original en ingles.")


# ---------------------------------------------------------------------------

def comprobar_unitypy():
    try:
        import UnityPy  # noqa: F401
    except ImportError:
        log("Falta el paquete UnityPy. Instalalo con:")
        log("    pip install -r requirements.txt")
        log("(o bien:  pip install UnityPy==1.25.3 )")
        sys.exit(1)


def main():
    args = sys.argv[1:]
    ruta_manual = None
    if "--ruta" in args:
        i = args.index("--ruta")
        if i + 1 >= len(args):
            log("Falta la ruta despues de --ruta")
            sys.exit(1)
        ruta_manual = args[i + 1]

    comprobar_unitypy()
    juego_dir = localizar_juego(ruta_manual)

    if "--restaurar" in args:
        restaurar(juego_dir)
        return

    refrescar = "--actualizar-backup" in args
    if refrescar:
        log("Actualizando la copia de seguridad con los bundles actuales del juego...")
        log("(usa esta opcion SOLO si el juego se acaba de actualizar por Steam)")
    asegurar_backup(juego_dir, refrescar=refrescar)

    log("Aplicando traduccion...")
    aplicar_interfaz(juego_dir)
    aplicar_dialogos(juego_dir)
    log("")
    log("Listo. Si en algun momento Steam actualiza el juego y ves textos en ingles")
    log("que antes estaban en espanol, vuelve a ejecutar:")
    log("    python instalar.py --actualizar-backup")


if __name__ == "__main__":
    main()
