# -*- mode: python -*-

block_cipher = None


a = Analysis(['tdr_reader_v3.2.1.py'],
             pathex=['C:\\Users\\g801781\\Desktop\\python_work\\UI\\tdr_reader_v3.2.1'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [('PyQt5/Qt/plugins/styles/qwindowsvistastyle.dll', 'C:\\Users\g801781\AppData\Local\Programs\Python\Python36\Lib\site-packages\PyQt5\Qt\plugins\styles\qwindowsvistastyle.dll', 'BINARY')],          
          name='tdr_reader_v3.2.1',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='cc.ico')
