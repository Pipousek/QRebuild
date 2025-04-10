import sys
from app import QRCodeRebuilder
from PyQt6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    window = QRCodeRebuilder()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()