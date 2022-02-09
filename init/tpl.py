#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

dirs_str = '''#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

from pathlib import Path

root_dir = Path(__file__).resolve().parents[1]
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
'''

gitignore_str = '''# Pycache
__pycache__

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# personal
.vscode
db/
input/
log/
output/'''

launch_str = '''#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

# Author: funchan
# CreateDate: 2021-10-28 21:18:12
# Description: launcher

import os
import platform
import sys
from pathlib import Path
from subprocess import PIPE, run

root_dir = Path(__file__).resolve().parent
core_dir = root_dir / 'core'
sys.path.append(str(core_dir))


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


def set_pip(pip_path):
    cmd_list = [
        f'{pip_path} config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/',
        f'{pip_path} config set global.trusted-host pypi.tuna.tsinghua.edu.cn',
        f'{pip_path} config set global.timeout 6000',
        f'{pip_path} install pip -U'
    ]

    [run(i, shell=True, stdout=PIPE, stderr=PIPE) for i in cmd_list]


if __name__ == '__main__':
    os.chdir(root_dir)
    _, venv_python_path, venv_pip_path = get_venv_path()

    if Path(sys.executable) != venv_python_path:
        cmd = f'{venv_python_path} {__file__}'
        run(cmd, shell=True, stdout=PIPE)
        sys.exit()

    flag = 1
    while True:
        try:
            from main import main
            main()
            break
        except ModuleNotFoundError as e:
            if flag < 1:
                print(e)
                break

            set_pip(venv_pip_path)
            cmd = f'{venv_pip_path} install -r requirements.txt'
            run(cmd, shell=True, stdout=PIPE)
            flag -= 1
'''

log_str = '''#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class Logger(object):
    def __init__(self,
                 log_dir: Path,
                 log_file_name: str = None,
                 maxBytes=5 * 1024 * 1024,
                 backupCount=5):

        self.log_dir = log_dir
        self.log_file_name = log_file_name
        self.maxBytes = maxBytes
        self.backupCount = backupCount
        self.formatter = logging.Formatter(
            fmt='%(asctime)s %(levelname)s>>%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        self.filehandlers = {}
        self.steamhandler = None

    def __create_handler(self, log_level: int):
        if log_level not in self.filehandlers.keys():
            if self.log_file_name:
                log_file = self.log_dir / f'{self.log_file_name} - {logging.getLevelName(log_level)}.log'
            else:
                log_file = self.log_dir / f'{logging.getLevelName(log_level)}.log'

            filehandler = RotatingFileHandler(log_file,
                                              encoding='utf-8',
                                              maxBytes=self.maxBytes,
                                              backupCount=self.backupCount)
            filehandler.setFormatter(self.formatter)
            filehandler.setLevel(log_level)
            self.filehandlers[log_level] = filehandler

        if not self.steamhandler:
            steamhandler = logging.StreamHandler()
            steamhandler.setFormatter(self.formatter)
            steamhandler.setLevel(logging.INFO)
            self.steamhandler = steamhandler

    def debug(self, message):
        logger = logging.getLogger('debug')
        log_level = logging.DEBUG
        logger.setLevel(log_level)

        self.__create_handler(log_level)
        logger.addHandler(self.filehandlers[log_level])
        logger.addHandler(self.steamhandler)

        logger.debug(message)

    def info(self, message):
        logger = logging.getLogger('info')
        log_level = logging.INFO
        logger.setLevel(log_level)

        self.__create_handler(log_level)
        logger.addHandler(self.filehandlers[log_level])
        logger.addHandler(self.steamhandler)

        logger.info(message)

    def warning(self, message):
        logger = logging.getLogger('warning')
        log_level = logging.WARNING
        logger.setLevel(log_level)

        self.__create_handler(log_level)
        logger.addHandler(self.filehandlers[log_level])
        logger.addHandler(self.steamhandler)

        logger.warning(message)

    def error(self, message):
        logger = logging.getLogger('error')
        log_level = logging.ERROR
        logger.setLevel(log_level)

        self.__create_handler(log_level)
        logger.addHandler(self.filehandlers[log_level])
        logger.addHandler(self.steamhandler)

        logger.error(message)

    def critical(self, message):
        logger = logging.getLogger('critical')
        log_level = logging.CRITICAL
        logger.setLevel(log_level)

        self.__create_handler(log_level)
        logger.addHandler(self.filehandlers[log_level])
        logger.addHandler(self.steamhandler)

        logger.critical(message)
'''

main_str = '''#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

# Author: $author
# CreateDate: $createdate
# Description: $description

from dirs import *
from log import Logger

# write your code here ...


def main():
    ...


if __name__ == '__main__':
    main()
'''

readme_str = '''## $appname

*$description*

### 用法

* 双击 **start.bat** 启动程序
* 程序运行结束，打开 **output** 目录查看运行结果

### 文件

* start.bat： Windows启动程序
* start.sh： Linux启动程序

### 目录
<table>
    <tr>
        <th>序号</th>
        <th>名称</th>
        <th>说明</th>
    </tr>
    <tr>
        <td>1</td>
        <td>.venv</td>
        <td>Python虚拟环境</td>
    </tr>
    <tr>
        <td>2</td>
        <td>bin</td>
        <td>依赖的可执行程序</td>
    </tr>
    <tr>
        <td>3</td>
        <td>conf</td>
        <td>配置信息</td>
    </tr>
    <tr>
        <td>4</td>
        <td>core</td>
        <td>核心代码</td>
    </tr>
    <tr>
        <td>5</td>
        <td>db</td>
        <td>数据库文件</td>
    </tr>
    <tr>
        <td>6</td>
        <td>docs</td>
        <td>说明文档</td>
    </tr>
    <tr>
        <td>7</td>
        <td>init</td>
        <td>程序初始化、打包</td>
    </tr>
    <tr>
        <td>8</td>
        <td>input</td>
        <td>用户输入文件</td>
    </tr>
    <tr>
        <td>9</td>
        <td>log</td>
        <td>运行日志</td>
    </tr>
    <tr>
        <td>10</td>
        <td>output</td>
        <td>运行结果</td>
    </tr>
    <tr>
        <td>11</td>
        <td>res</td>
        <td>引用资源</td>
    </tr>
    <tr>
        <td>12</td>
        <td>tests</td>
        <td>测试代码</td>
    </tr>
</table>'''

start_str_cmd = r'''@echo off

cd /d %~dp0
setlocal enabledelayedexpansion

if not exist .venv\scripts\python.exe (
    python -m venv .venv 1>nul 2>nul

    if not exist .venv\scripts\python.exe (
        echo Install Python...
        set temp_file=!Temp!\python-3.7.6.exe

        set url="https://oss.npmmirror.com/dist/python/3.7.6/python-3.7.6.exe"
        certutil -urlcache -split -f !url! !temp_file! 1>nul 2>nul

        if !errorlevel! NEQ 0 (
            set url="https://www.python.org/ftp/python/3.7.6/python-3.7.6.exe"
            certutil -urlcache -split -f !url! !temp_file! 1>nul 2>nul

            if !errorlevel! NEQ 0 (
                echo Error: Failed to download Python, Check the network!
                pause >nul
                exit
            )
        )

        if "!PROCESSOR_ARCHITECTURE!"=="AMD64" (
            set python_dir=!LocalAppData!\Programs\Python37-32
        ) else (
            set python_dir=!LocalAppData!\Programs\Python37
        )

        !temp_file! /passive /quiet PrependPath=1 TargetDir=!python_dir!
        !python_dir!\python.exe -m venv .venv 1>nul 2>nul
    )
)

.venv\scripts\python.exe launch.py'''

start_str_dash = r'''stty -echo

cd `dirname $0`

if [ ! -e ./.venv/bin/python3 ]; then
    python3 -m venv .venv
    if [ ! -e ./.venv/bin/python3 ]; then
        echo Install Python3.x and run this script again.
    fi
fi
./.venv/bin/python3 ./launch.py'''
