# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = ['services.supabase.supabase_service', 'encodings.idna',]
hiddenimports += collect_submodules('esptool')
hiddenimports += collect_submodules('ui.views')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets'), ('config', 'config'), ('styles', 'styles'), ('.env', '.')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['qtawesome', 'PIL'],
    noarchive=False,
    optimize=2,
)

excluded_dlls = {
    "Qt6Pdf.dll",
    "Qt6Qml.dll",
    "Qt6QmlMeta.dll",
    "Qt6QmlModels.dll",
    "Qt6QmlWorkerScript.dll",
    "Qt6Quick.dll",
    "Qt6VirtualKeyboard.dll",
    "opengl32sw.dll"
}

a.binaries = [
    item for item in a.binaries
    if item[0].replace("\\", "/").split("/")[-1] not in excluded_dlls
]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PlantERA',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets/img/logo/plantera_logo.ico'],
)
