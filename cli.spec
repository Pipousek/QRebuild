# cli_qr_rebuilder.spec
block_cipher = None

a = Analysis(
    ['cli/main.py'],
    pathex=['.'],
    binaries=[
        ('.venv/Lib/site-packages/pyzbar/libiconv.dll', '.'),
        ('.venv/Lib/site-packages/pyzbar/libzbar-64.dll', '.'),
    ],
    datas=[
        ('./core', './cli/core'),
        ('./img/logo.ico', 'img')
    ],
    hiddenimports=[],
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='QRebuild-CLI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['img/logo.ico'],
)