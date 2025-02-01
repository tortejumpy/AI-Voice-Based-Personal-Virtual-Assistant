import os
import subprocess as sp

# Paths to commonly used applications
paths = {
    'notepad': r"C:\Program Files\Notepad++\notepad++.exe",
    'calculator': r"C:\Windows\System32\calc.exe",
}

def open_notepad():
    """Open Notepad++ application."""
    try:
        os.startfile(paths['notepad'])
        print("Notepad++ opened successfully.")
    except FileNotFoundError:
        print("Error: Notepad++ not found. Please check the path in 'paths'.")

def open_cmd():
    """Open Command Prompt."""
    try:
        os.system('start cmd')
        print("Command Prompt opened successfully.")
    except Exception as e:
        print(f"Error opening Command Prompt: {e}")

def open_camera():
    """Open the Camera application."""
    try:
        sp.run('start microsoft.windows.camera:', shell=True, check=True)
        print("Camera opened successfully.")
    except sp.CalledProcessError as e:
        print(f"Error opening Camera: {e}")

def open_calculator():
    """Open the Calculator application."""
    try:
        sp.Popen(paths['calculator'])
        print("Calculator opened successfully.")
    except FileNotFoundError:
        print("Error: Calculator not found. Please check the path in 'paths'.")
