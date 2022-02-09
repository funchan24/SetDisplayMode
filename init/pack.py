#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

import argparse
import errno
import os
import platform
import shutil
import stat
from pathlib import Path
from subprocess import PIPE, run
from zipfile import ZipFile


def pack_zip(root_dir, output_dir):
    """package root_dir as zip file, save to output_dir"""

    include_dirs = (root_dir / 'bin', root_dir / 'conf', root_dir / 'core',
                    root_dir / 'docs', root_dir / 'init', root_dir / 'res')
    output_dir.mkdir(parents=True, exist_ok=True)
    zip_path = output_dir / (root_dir.name + '.zip')
    if zip_path.exists():
        zip_path.unlink()

    with ZipFile(zip_path, 'w') as z_file:
        for file in root_dir.iterdir():
            if file.is_dir(
            ) and file in include_dirs and file.name != '__pycache__':
                for sub_file in file.rglob('*'):
                    if file.parent.name != '__pycache__':
                        z_file.write(sub_file, sub_file.relative_to(root_dir))
            if file.is_file() and file.parent.name != '__pycache__':
                z_file.write(file, file.relative_to(root_dir))

    os_platform = platform.system()
    if os_platform == 'Windows':
        run(f'explorer {output_dir}', shell=True, stdout=PIPE, stderr=PIPE)


def pack_exe(root_dir, output_dir, pack_cmd):
    """use Nuitka package root_dir as exe file, save to output_dir"""

    def _onerror(func, path, exc):
        excvalue = exc[1]
        if func in (os.rmdir, os.remove,
                    os.unlink) and excvalue.errno == errno.EACCES:
            os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            func(path)
        else:
            raise

    if isinstance(output_dir, str):
        output_dir = Path(output_dir)

    try:
        shutil.rmtree(output_dir, onerror=_onerror)
    except FileNotFoundError:
        pass
    output_dir.mkdir(parents=True, exist_ok=True)

    include_dirs = (root_dir / 'bin', root_dir / 'conf', root_dir / 'res')
    for _dir in include_dirs:
        shutil.copytree(_dir, output_dir / _dir.name)

    run(pack_cmd, shell=True)

    for _dir in output_dir.iterdir():
        if '.dist' in _dir.name:
            new_name = _dir.name.replace('.dist', '')
            new_path = _dir.with_name(new_name)
            os.rename(_dir, new_path)


def arg_parse():
    parser = argparse.ArgumentParser(prog='pack',
                                     description='packing python files')

    parser.add_argument('--pack-type', choices=('zip', 'exe'), required=True)
    parser.add_argument('--pack-mode',
                        choices=('typical', 'custom'),
                        required=True)
    parser.add_argument('--extra-option',
                        metavar='',
                        default='',
                        help='use nuitak options')

    return parser.parse_args()


def main():
    root_dir = Path(__file__).resolve().parents[1]
    os.chdir(root_dir)

    run('pip freeze >requirements.txt', shell=True, stdout=PIPE, stdin=PIPE)

    args = arg_parse()
    pack_type = args.pack_type
    pack_mode = args.pack_mode
    extra_option = args.extra_option

    if pack_type == 'zip':
        output_dir = root_dir / 'output'
        pack_zip(root_dir, output_dir)
    else:
        run('pip install -U Nuitka', shell=True, stdout=PIPE, stderr=PIPE)
        if pack_mode == 'typical':
            standalone = '--standalone'
            output_dir = Path('output', root_dir.name)
            remove_output = '--remove-output'
            windows_disable_console = '--windows-disable-console'
            windows_icon = Path('res', 'main_256.ico')
            plugin_enable = 'tk-inter'
            target_file = Path('core', 'main.py')
        else:
            standalone = ''
            output_dir = ''
            remove_output = ''
            windows_disable_console = ''
            windows_icon = ''
            plugin_enable = ''
            target_file = ''

        pack_cmd = f'''nuitka {standalone} --output-dir={output_dir} {remove_output} {windows_disable_console} --windows-icon-from-ico={windows_icon} --plugin-enable={plugin_enable} {extra_option} {target_file}'''

        pack_exe(root_dir, output_dir, pack_cmd)


if __name__ == '__main__':
    main()
