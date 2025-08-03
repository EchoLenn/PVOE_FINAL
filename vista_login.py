from PySide6.QtWidgets import *
from PySide6.QtCore import *
import database_manager

class VistaLogin(QWidget):
    login_exitoso = Signal(str, str)  

    def __init__(self):
        super().__init__()

        self.entry_usuario = QLineEdit()
        self.entry_usuario.setPlaceholderText("Usuario")
        
        self.entry_contrasena = QLineEdit()
        self.entry_contrasena.setPlaceholderText("Contraseña")
        self.entry_contrasena.setEchoMode(QLineEdit.EchoMode.Password)

        self.boton_acceder = QPushButton("Acceder")

        layout_formulario = QFormLayout()
        layout_formulario.addRow("Usuario:", self.entry_usuario)
        layout_formulario.addRow("Contraseña:", self.entry_contrasena)

        layout_principal = QVBoxLayout(self)
        layout_principal.addStretch()
        layout_principal.addWidget(QLabel("<h2>LOGIN</h2>"))
        layout_principal.addLayout(layout_formulario)
        layout_principal.addWidget(self.boton_acceder)
        layout_principal.addStretch()

        self.setLayout(layout_principal)

        self.boton_acceder.clicked.connect(self.verificar_login)
        self.entry_contrasena.returnPressed.connect(self.verificar_login)

    @Slot()
    def verificar_login(self):
        """Verifica las credenciales contra la base de datos."""
        usuario = self.entry_usuario.text()
        contrasena = self.entry_contrasena.text()

        rol = database_manager.verificar_usuario(usuario, contrasena)
        
        if rol:
            self.login_exitoso.emit(usuario, rol)
        else:
            QMessageBox.warning(self, "Error de Acceso", "Usuario o contraseña incorrectos.")