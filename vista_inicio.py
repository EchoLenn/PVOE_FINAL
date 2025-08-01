from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class VistaInicio(QWidget):
    def __init__(self):
        super().__init__()

        label_logo = QLabel()
        pixmap_logo = QPixmap("logoUamitos.png")
        label_logo.setPixmap(pixmap_logo)
        label_logo.setScaledContents(True)
        label_logo.setFixedSize(120, 100)

        layout_superior = QHBoxLayout()
        layout_superior.addStretch()
        layout_superior.addWidget(label_logo)

        label_imagen_central = QLabel()
        pixmap_central = QPixmap("imagen1.png")
        label_imagen_central.setPixmap(pixmap_central)
        label_imagen_central.setScaledContents(True)
        label_imagen_central.setFixedSize(350, 250)

        label_texto = QLabel(
            "<h1>Bienvenido al Sistema de Gestión</h1>"
            "<p>Seleccione una opción del menú o de la barra de herramientas para comenzar.</p>"
        )
        label_texto.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout_principal = QVBoxLayout(self)
        layout_principal.addLayout(layout_superior)
        layout_principal.addStretch()
        layout_principal.addWidget(label_imagen_central, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(label_texto)
        layout_principal.addStretch()