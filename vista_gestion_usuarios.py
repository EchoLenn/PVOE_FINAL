from PySide6.QtWidgets import *
from PySide6.QtCore import *
import database_manager

class VistaGestionUsuarios(QWidget):
    def __init__(self, usuario_actual=None, rol_actual=None):
        super().__init__()
        self.usuario_actual = usuario_actual
        self.rol_actual = rol_actual
        
        layout_principal = QVBoxLayout(self)
        
        self.tabla_usuarios = QTableWidget()
        self.tabla_usuarios.setColumnCount(3)
        self.tabla_usuarios.setHorizontalHeaderLabels(["ID", "Usuario", "Rol"])
        self.tabla_usuarios.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_usuarios.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        self.tabla_usuarios.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        
        self.boton_actualizar = QPushButton("Actualizar Lista")
        self.boton_editar = QPushButton("Editar Usuario")
        self.boton_eliminar = QPushButton("Eliminar Seleccionados")
        self.boton_crear = QPushButton("Crear Nuevo Usuario")
        
        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.boton_actualizar)
        layout_botones.addWidget(self.boton_editar)
        layout_botones.addWidget(self.boton_eliminar)
        layout_botones.addStretch()
        layout_botones.addWidget(self.boton_crear)
        
        self.grupo_formulario = QGroupBox("Formulario de Usuario")
        layout_formulario = QFormLayout()
        
        self.label_id = QLabel("Nuevo Usuario")
        self.entry_username = QLineEdit()
        self.entry_password = QLineEdit()
        self.entry_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.combo_rol = QComboBox()
        self.combo_rol.addItems(["profesor", "asistente", "admin"])
        self.boton_guardar = QPushButton("Guardar")
        
        layout_formulario.addRow("ID:", self.label_id)
        layout_formulario.addRow("Usuario:", self.entry_username)
        layout_formulario.addRow("Contraseña:", self.entry_password)
        layout_formulario.addRow("Rol:", self.combo_rol)
        layout_formulario.addRow(self.boton_guardar)
        self.grupo_formulario.setLayout(layout_formulario)
        
        layout_principal.addWidget(QLabel("<h2>Gestión de Usuarios</h2>"))
        layout_principal.addWidget(self.tabla_usuarios)
        layout_principal.addLayout(layout_botones)
        layout_principal.addWidget(self.grupo_formulario)
        
        self.boton_actualizar.clicked.connect(self.cargar_usuarios)
        self.boton_editar.clicked.connect(self.editar_usuario)
        self.boton_eliminar.clicked.connect(self.eliminar_usuarios)
        self.boton_crear.clicked.connect(self.preparar_nuevo_usuario)
        self.boton_guardar.clicked.connect(self.guardar_usuario)
        self.tabla_usuarios.itemSelectionChanged.connect(self.actualizar_botones)
        
        if self.rol_actual != "admin":
            self.boton_crear.setVisible(False)
            self.boton_eliminar.setVisible(False)
            self.boton_actualizar.setVisible(False)
            self.tabla_usuarios.setEditTriggers(QTableWidget.NoEditTriggers)
        
        self.cargar_usuarios()
        self.preparar_nuevo_usuario()

    def cargar_usuarios(self):
        self.tabla_usuarios.setRowCount(0)
        usuarios = database_manager.obtener_usuarios()
        
        for usuario in usuarios:
            id_usuario, username, rol = usuario
            
            if self.rol_actual != "admin" and username != self.usuario_actual:
                continue
                
            fila = self.tabla_usuarios.rowCount()
            self.tabla_usuarios.insertRow(fila)
            self.tabla_usuarios.setItem(fila, 0, QTableWidgetItem(str(id_usuario)))
            self.tabla_usuarios.setItem(fila, 1, QTableWidgetItem(username))
            self.tabla_usuarios.setItem(fila, 2, QTableWidgetItem(rol))

    def preparar_nuevo_usuario(self):
        self.label_id.setText("Nuevo Usuario")
        self.entry_username.clear()
        self.entry_password.clear()
        self.combo_rol.setCurrentIndex(0)
        self.boton_guardar.setText("Crear Usuario")
        self.usuario_actual_editando = None

    def editar_usuario(self):
        seleccionados = self.tabla_usuarios.selectedItems()
        if not seleccionados:
            QMessageBox.warning(self, "Selección Vacía", "Seleccione un usuario para editar.")
            return
        
        fila = seleccionados[0].row()
        id_usuario = int(self.tabla_usuarios.item(fila, 0).text())
        username = self.tabla_usuarios.item(fila, 1).text()
        rol = self.tabla_usuarios.item(fila, 2).text()
        
        if self.rol_actual != "admin" and username != self.usuario_actual:
            QMessageBox.critical(self, "Permiso Denegado", "Solo puedes editar tu propio perfil.")
            return
        
        self.label_id.setText(f"ID: {id_usuario}")
        self.entry_username.setText(username)
        self.entry_password.clear()
        self.combo_rol.setCurrentText(rol)
        
        if self.rol_actual != "admin":
            self.combo_rol.setEnabled(False)
        
        self.boton_guardar.setText("Actualizar Usuario")
        self.usuario_actual_editando = username

    def eliminar_usuarios(self):
        seleccionados = self.tabla_usuarios.selectedItems()
        if not seleccionados:
            QMessageBox.warning(self, "Selección Vacía", "Seleccione usuarios para eliminar.")
            return
        
        if self.rol_actual != "admin":
            QMessageBox.critical(self, "Permiso Denegado", "Solo los administradores pueden eliminar usuarios.")
            return
        
        admin_pass, ok = QInputDialog.getText(self, "Verificación de Administrador", 
                                             "Ingrese la contraseña del admin para autorizar:", 
                                             QLineEdit.EchoMode.Password)
        
        if not ok or not database_manager.verificar_usuario("admin", admin_pass):
            QMessageBox.critical(self, "Autorización Fallida", "Contraseña de administrador incorrecta.")
            return
        
        ids = []
        filas = set(item.row() for item in seleccionados)
        for fila in filas:
            id_usuario = int(self.tabla_usuarios.item(fila, 0).text())
            username = self.tabla_usuarios.item(fila, 1).text()
            
            if username == "admin":
                QMessageBox.critical(self, "Error", "No se puede eliminar la cuenta de administrador principal.")
                return
                
            ids.append(id_usuario)
        
        if database_manager.eliminar_usuarios(ids):
            QMessageBox.information(self, "Éxito", "Usuarios eliminados correctamente.")
            self.cargar_usuarios()
        else:
            QMessageBox.critical(self, "Error", "No se pudieron eliminar los usuarios.")

    def guardar_usuario(self):
        username = self.entry_username.text().strip()
        password = self.entry_password.text().strip()
        rol = self.combo_rol.currentText()

        if not username:
            QMessageBox.warning(self, "Campo Vacío", "El nombre de usuario es requerido.")
            return
        
        if self.boton_guardar.text() == "Crear Usuario":
            admin_pass, ok = QInputDialog.getText(self, "Verificación de Administrador", 
                                                "Ingrese la contraseña del admin para autorizar:", 
                                                QLineEdit.EchoMode.Password)
            
            if not ok or not database_manager.verificar_usuario("admin", admin_pass):
                QMessageBox.critical(self, "Autorización Fallida", "Contraseña de administrador incorrecta.")
                return
        else:
            if username == self.usuario_actual:
                current_pass, ok = QInputDialog.getText(self, "Verificación", 
                                                      "Ingrese su contraseña actual para confirmar:", 
                                                      QLineEdit.EchoMode.Password)
                
                if not ok or not database_manager.verificar_usuario(username, current_pass):
                    QMessageBox.critical(self, "Autorización Fallida", "Contraseña actual incorrecta.")
                    return
            else:
                admin_pass, ok = QInputDialog.getText(self, "Verificación de Administrador", 
                                                    "Ingrese la contraseña del admin para autorizar:", 
                                                    QLineEdit.EchoMode.Password)
                
                if not ok or not database_manager.verificar_usuario("admin", admin_pass):
                    QMessageBox.critical(self, "Autorización Fallida", "Contraseña de administrador incorrecta.")
                    return
        
        if self.boton_guardar.text() == "Crear Usuario":
            resultado = database_manager.crear_usuario(username, password, rol)
            if resultado is True:
                QMessageBox.information(self, "Éxito", f"Usuario '{username}' creado exitosamente.")
                self.cargar_usuarios()
                self.preparar_nuevo_usuario()
            elif resultado == "integridad":
                QMessageBox.warning(self, "Error", f"El nombre de usuario '{username}' ya existe.")
            else:
                QMessageBox.critical(self, "Error", "No se pudo crear el usuario.")
        else:
            actualizar_password = bool(password)
            resultado = database_manager.actualizar_usuario(
                self.usuario_actual_editando, username, password if actualizar_password else "", rol)
            
            if resultado is True:
                QMessageBox.information(self, "Éxito", f"Usuario '{username}' actualizado exitosamente.")
                self.cargar_usuarios()
                self.preparar_nuevo_usuario()
            elif resultado == "integridad":
                QMessageBox.warning(self, "Error", f"El nombre de usuario '{username}' ya existe.")
            else:
                QMessageBox.critical(self, "Error", "No se pudo actualizar el usuario.")

    def actualizar_botones(self):
        seleccionados = len(self.tabla_usuarios.selectedItems()) > 0
        self.boton_editar.setEnabled(seleccionados)
        self.boton_eliminar.setEnabled(seleccionados and self.rol_actual == "admin")