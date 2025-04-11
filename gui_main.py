import sys
import os
from gui_app import QRCodeRebuilder
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

def resource_path(relative_path):
    try:
        # PyInstaller creates temp folder in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # If PyInstaller is not in use, use default path
        base_path = os.path.abspath(".")

    res_path =  os.path.join(base_path, relative_path)
    print(res_path)
    return res_path

def main():
    app = QApplication(sys.argv)
    icon = QIcon(resource_path("img/logo.ico"))
    app.setWindowIcon(icon)
    window = QRCodeRebuilder()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()