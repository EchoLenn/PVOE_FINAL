from PySide6.QtWidgets import *
from PySide6.QtCore import *
import database_manager

class VistaGestionUsuarios(QWidget):
    def __init__(self):
        super().__init__()
        layout_principal = QVBoxLayout(self)
        layout_formulario = QFormLayout()

        self.entry_username = QLineEdit()
        self.entry_password = QLineEdit()
        self.entry_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.combo_rol = QComboBox()
        self.combo_rol.addItems(["profesor", "asistente"])
        self.boton_crear = QPushButton("Crear Usuario")

        layout_formulario.addRow("Nuevo Usuario:", self.entry_username)
        layout_formulario.addRow("Contraseña:", self.entry_password)
        layout_formulario.addRow("Rol:", self.combo_rol)

        layout_principal.addWidget(QLabel("<h2>Gestión de Nuevos Usuarios</h2>"))
        layout_principal.addLayout(layout_formulario)
        layout_principal.addWidget(self.boton_crear)
        layout_principal.addStretch()

        self.boton_crear.clicked.connect(self.crear_nuevo_usuario)

    @Slot()
    def crear_nuevo_usuario(self):
        username = self.entry_username.text().strip()
        password = self.entry_password.text().strip()
        rol = self.combo_rol.currentText()

        if not username or not password:
            QMessageBox.warning(self, "Campos Vacíos", "Usuario y contraseña son requeridos.")
            return

        admin_pass, ok = QInputDialog.getText(self, "Verificación de Administrador", 
                                              "Ingrese la contraseña del admin para autorizar:", 
                                              QLineEdit.EchoMode.Password)
        
        if not ok or not database_manager.verificar_usuario("admin", admin_pass):
            QMessageBox.critical(self, "Autorización Fallida", "Contraseña de administrador incorrecta.")
            return

        resultado = database_manager.crear_usuario(username, password, rol)
        if resultado is True:
            QMessageBox.information(self, "Éxito", f"Usuario '{username}' creado exitosamente.")
            self.entry_username.clear()
            self.entry_password.clear()
        elif resultado == "integridad":
            QMessageBox.warning(self, "Error", f"El nombre de usuario '{username}' ya existe.")
        else:
            QMessageBox.critical(self, "Error", "No se pudo crear el usuario.")