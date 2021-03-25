from kivy.tools.packaging.pyinstaller_hooks import get_deps_all, hookspath, runtime_hooks
from kivy_deps import sdl2, glew


# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['FreeCAD4K.py'],
             pathex=['C:\\Users\\Gus\\Desktop\\4KUI'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

a.datas += [('Code\FreeCAD4K.kv', 'C:\\Users\\Gus\\Desktop\\4KUI\\FreeCAD4K.kv', 'DATA')]       
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='FreeCAD4K',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='C:\\Users\\Gus\\Desktop\\4KUI\\icon.ico')
coll = COLLECT(exe, Tree('C:\\Users\\Gus\\Desktop\\4KUI\\'),	
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='FreeCAD4K')
app = BUNDLE(coll,
             name='FreeCAD4K.app',
             icon='icon.ico',
         bundle_identifier=None)