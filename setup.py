from argparse import ArgumentParser
from sys import platform
from json import load, dump
from uuid import uuid4
from cx_Freeze import setup, Executable


def get_parser():
    parser = ArgumentParser(description='application builder')
    parser.add_argument('build_mode', type=str)
    parser.add_argument('--version', type=str, default='0.0.0', help='build version')
    return parser


def product_code(version):
    new_code = str(uuid4()).upper()
    if version == '0.0.0':
        return new_code

    filepath = './product_codes.json'
    with open(filepath, mode='r', encoding='utf-8') as f:
        codes = load(f)

    code = codes.get(version, None)
    if code:
        pass
    else:
        codes[version] = new_code
        with open(filepath, mode='w', encoding='utf-8') as f:
            dump(codes, f, indent=2, ensure_ascii=False)
    return code


def update_code():
    return '9F0FACC5-FFDF-44B9-BE04-8291A1FC3B28'


if __name__ == '__main__':
    args = get_parser().parse_args()

    app_name = 'Vision Tester'
    app_copyright = '© 2022 northfieldzz'
    icon_path = './static/icons/logo.ico'

    build_exe = {
        'packages': [],
        'includes': [],
        'excludes': [],
        'include_files': [
            ('static/', 'static/'),
            ('logging.ini', 'logging.ini')
        ],
        'include_msvcr': True
    }

    bdist_msi = {
        'add_to_path': True,
        'data': {
            # Directoryに関しては下記参照
            # https://docs.microsoft.com/ja-jp/windows/win32/msi/directory-table
            'Directory': [
                ('ProgramMenuFolder', 'TARGETDIR', '.'),
                ('MyProgramMenu', 'ProgramMenuFolder', 'Northfield')
            ],
            # ProgIdに関しては下記参照
            # https://docs.microsoft.com/en-us/windows/win32/msi/progid-table
            'ProgId': [
                ('ProgId', None, None, app_name, 'IconId', None)
            ],
            'Icon': [
                ('IconId', icon_path)
            ]
        },
        'product_code': f'{{{product_code(args.version)}}}',
        'upgrade_code': f'{{{update_code()}}}',
        'install_icon': icon_path
    }

    base = None
    if platform == "win32":
        base = "Win32GUI"

    gui_app_executable = Executable(
        script='vision_tester.py',
        base=base,
        copyright=app_copyright,
        icon=icon_path,
        shortcut_name=app_name,
        shortcut_dir='MyProgramMenu'
    )

    cli_app_executable = Executable(
        script='vision_tester_cli.py',
        copyright=app_copyright,
        icon=icon_path,
        shortcut_name=f'{app_name} Cli',
        shortcut_dir='MyProgramMenu'
    )

    setup(
        author='northfieldzz',
        author_email='northfield.t@outlook.com',
        url='https://github.com/northfieldzz',
        name=app_name,
        script_args=[args.build_mode],
        options={
            'build_exe': build_exe,
            'bdist_msi': bdist_msi
        },
        version=args.version,
        description=f'{app_name} Runtime',
        executables=[
            gui_app_executable,
            cli_app_executable
        ]
    )
