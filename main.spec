# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import sysconfig
from PyInstaller.utils.hooks import copy_metadata

proj_dir = os.path.dirname(os.path.abspath(sys.argv[0])) 
# site-packages of the running interpreter (pixi, conda or venv alike)
site_packages = sysconfig.get_paths()["purelib"]
icon_filepath = os.path.normpath(os.path.join(proj_dir, "src/digest/assets/icons/digest_logo.ico"))
dist_info_path = os.path.join(proj_dir, "src/digestai.egg-info")

a = Analysis(
    [os.path.normpath(os.path.join(proj_dir,'src/digest/main.py'))],
    pathex=[os.path.normpath(site_packages), os.path.normpath('src/digest')],
    binaries=[],
    datas=copy_metadata("digestai") + copy_metadata("onnxruntime") + copy_metadata("onnx") + [
            (
                os.path.normpath(os.path.join(proj_dir, 'src/digest/subgraph_analysis/database.zip')), 
                os.path.normpath("digest/subgraph_analysis")
            ),
            (
                os.path.normpath(os.path.join(proj_dir, 'src/digest/gui_config.yaml')), 
                os.path.normpath(".")
            ),
        ],
    hiddenimports=['clickablelabel'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='digest',
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
    icon=icon_filepath
)