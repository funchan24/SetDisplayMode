#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

# Author: funchan
# CreateDate: 2021-05-12 12:57:40
# Description: 适用于 联想小新 PRO16 GTX1650。程序每2分钟检查一次电脑是否接通电源、电池余量，如果电脑接通电源，屏幕亮度调为100%，屏幕刷新率调为120；如果电脑使用电池供电，屏幕亮度根据电池余量从80%逐步降至50%，屏幕刷新率调为60。

import ctypes
import time
from collections import namedtuple
from ctypes import wintypes
from subprocess import PIPE, run

from dirs import *
from log import Logger


def get_system_power_status():
    class SYSTEM_POWER_STATUS(ctypes.Structure):
        _fields_ = [('ACLineStatus', wintypes.BYTE),
                    ('BatteryFlag', wintypes.BYTE),
                    ('BatteryLifePercent', wintypes.BYTE),
                    ('SystemStatusFlas', wintypes.BYTE),
                    ('BatteryLifeTime', wintypes.DWORD),
                    ('BatteryFullLifeTime', wintypes.DWORD)]

    SYSTEM_POWER_STATUS_P = ctypes.POINTER(SYSTEM_POWER_STATUS)
    GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
    GetSystemPowerStatus.argtypes = [SYSTEM_POWER_STATUS_P]
    GetSystemPowerStatus.restype = wintypes.BOOL

    system_power_status = SYSTEM_POWER_STATUS()
    system_power_status_p = ctypes.pointer(system_power_status)
    if not GetSystemPowerStatus(system_power_status_p):
        raise ctypes.WinError()

    return system_power_status


def set_brightness(brightness):
    nircmd = bin_dir / 'nircmd' / 'nircmd.exe'
    run(f'{nircmd} setbrightness {brightness}',
        shell=True,
        stdout=PIPE,
        stderr=PIPE)


def set_display(devmode):
    nircmd = bin_dir / 'nircmd' / 'nircmd.exe'
    run(f'{nircmd} setdisplay {" ".join(devmode)}',
        shell=True,
        stdout=PIPE,
        stderr=PIPE)


def main():
    logger = Logger(log_dir)
    DEVMODE = namedtuple('DEVMODE',
                         ['width', 'height', 'color_bits', 'refresh_rate'])

    while True:
        system_power_status = get_system_power_status()
        power_plugged = bool(system_power_status.ACLineStatus)
        power_percent = system_power_status.BatteryLifePercent

        if power_plugged:
            brightness = 100
            devmode = DEVMODE('2560', '1600', '32', '120')

        else:
            brightness = 50 + int(power_percent * 0.3)
            devmode = DEVMODE('2560', '1600', '32', '60')

        set_brightness(brightness)
        set_display(devmode)

        logger.info(
            f'外接电源：{power_plugged}, 电池余量：{power_percent}%, 屏幕亮度：{brightness}%, 屏幕刷新率：{devmode.refresh_rate}'
        )

        time.sleep(120)


if __name__ == '__main__':
    main()
