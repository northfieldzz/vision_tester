from cx_Freeze import setup, Executable

setup(
    name='Vision tester',
    options={
        'build_exe': {
            'packages': [],
            'includes': [],
            'excludes': [],
            'include_files': [
                'static/'
            ],
            'include_msvcr': True
        },
        'bdist_msi': {
            'data': {
                'Directory': [
                    ('ProgramMenuFolder', 'TARGETDIR', '.'),
                    ('MyProgramMenu', 'ProgramMenuFolder', 'North')
                ],
                'ProgId': [
                    ('ProgId', None, None, 'Google Vision tester', 'IconId', None)
                ],
                'Icon': [
                    ('IconId', './static/logo.ico')
                ]
            }
        }
    },
    version='1.0.0',
    description='Google Vision tester',
    executables=[
        Executable(
            script='main.py',
            base='Win32GUI',
            copyright='Copyright(C) 2022 northfieldzz',
            icon='./static/logo.ico',
            shortcut_name='Vision tester',
            shortcut_dir='MyProgramMenu'
        )
    ]

)
