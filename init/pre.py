#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

import locale
import os
import platform
import string
import time
from pathlib import Path
from subprocess import PIPE, run

from tpl import *


def get_venv_path():
    venv_dir = root_dir / '.venv'

    os_platform = platform.system()
    if os_platform == 'Windows':
        python_str = 'python'
        python_path = venv_dir / 'scripts' / 'python.exe'
        pip_path = venv_dir / 'scripts' / 'pip.exe'

    elif os_platform == 'Linux':
        python_str = 'python3'
        python_path = venv_dir / 'bin' / 'python3'
        pip_path = venv_dir / 'bin' / 'pip3'

    else:
        raise EnvironmentError('unsupported platform!')

    return python_str, python_path, pip_path


def create_py_venv():
    base_python, _, _ = get_venv_path()
    p = run(f'{base_python} -m venv .venv',
            shell=True,
            stdout=PIPE,
            stderr=PIPE)
    if not p.returncode:
        print(f'create python venv')
    else:
        os_platform = platform.system()
        if os_platform == 'Windows':
            err_msg = f'''failed to create python venv
the command maybe as follows:

cd {root_dir}
python -m venv .venv
'''

        elif os_platform == 'Linux':
            err_msg = f'''failed to create python venv
the command maybe as follows:

cd {root_dir}
python3 -m venv .venv
'''

        else:
            err_msg = 'failed to create python venv, unsupported platform'

        raise ValueError(err_msg)


def set_pip(pip_path):
    cmd_list = [
        f'{pip_path} config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/',
        f'{pip_path} config set global.trusted-host pypi.tuna.tsinghua.edu.cn',
        f'{pip_path} config set global.timeout 6000',
        f'{pip_path} install pip -U'
    ]

    [run(i, shell=True, stdout=PIPE, stderr=PIPE) for i in cmd_list]


def pre():
    """create python virtual environment, required directories and files,
    install package dependencies with requirements.txt"""

    appname = root_dir.name
    author = input('author: ')

    createdate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    description = input('description: ') or ''

    info = {
        'appname': appname,
        'author': author,
        'createdate': createdate,
        'description': description
    }

    _, _, venv_pip_path = get_venv_path()
    set_pip(venv_pip_path)

    encoding = locale.getpreferredencoding()
    requirements_file = root_dir / 'requirements.txt'
    try:
        with open(requirements_file, encoding=encoding,
                  errors='ignore') as file:
            requirements = file.read()
    except (FileNotFoundError, OSError):
        requirements = None

    if requirements:
        p = run(f'{venv_pip_path} list',
                shell=True,
                stdout=PIPE,
                stderr=PIPE,
                universal_newlines=True)
        installed_packages = p.stdout

        for line in requirements.split('\n'):
            try:
                package, _ = line.strip().split('==')
            except ValueError:
                continue

            if package not in installed_packages:
                run(f'{venv_pip_path} install {line}',
                    shell=True,
                    stdout=PIPE,
                    stderr=PIPE)

                print(f'install package: {package}')
                time.sleep(1)

    bin_dir = root_dir / 'bin'
    conf_dir = root_dir / 'conf'
    core_dir = root_dir / 'core'
    db_dir = root_dir / 'db'
    docs_dir = root_dir / 'docs'
    init_dir = root_dir / 'init'
    input_dir = root_dir / 'input'
    log_dir = root_dir / 'log'
    output_dir = root_dir / 'output'
    res_dir = root_dir / 'res'
    tests_dir = root_dir / 'tests'

    dir_tuple = (root_dir, bin_dir, conf_dir, core_dir, db_dir, docs_dir,
                 init_dir, input_dir, log_dir, output_dir, res_dir, tests_dir)
    for _dir in dir_tuple:
        _dir.mkdir(parents=True, exist_ok=True)

    dirs_file = core_dir / 'dirs.py'
    gitignore_file = root_dir / '.gitignore'
    launch_file = root_dir / 'launch.py'
    log_file = core_dir / 'log.py'
    main_file = core_dir / 'main.py'
    readme_file = root_dir / 'README.md'

    os_platform = platform.system()
    if os_platform == 'Windows':
        start_file = root_dir / 'start.bat'
        start_str = start_str_cmd

        if not start_file.exists():
            with open(start_file, 'w', encoding=encoding) as fp:
                fp.write(start_str)

    if os_platform == 'Linux':
        start_file = root_dir / 'start.sh'
        start_str = start_str_dash
        if not start_file.exists():
            with open(start_file, 'w', encoding=encoding) as fp:
                fp.write(start_str)
        run(f'chmod +x {start_file}', shell=True, stdout=PIPE, stderr=PIPE)

    file_tuple = ((dirs_file, dirs_str), (gitignore_file, gitignore_str),
                  (launch_file, launch_str), (log_file, log_str),
                  (main_file, main_str), (readme_file, readme_str))
    for file in file_tuple:
        file_path, file_content = file
        if not file_path.exists():
            s = string.Template(file_content)
            s = s.safe_substitute(info)
            with open(file_path, 'w', encoding='utf-8') as fp:
                fp.write(s)

    print('everything is ok, enjoy')


if __name__ == '__main__':
    root_dir = Path(__file__).resolve().parents[1]
    os.chdir(root_dir)

    base_python, venv_python_path, venv_pip_path = get_venv_path()
    if not all([venv_python_path.exists(), venv_pip_path.exists()]):
        create_py_venv()

    pre()
