import re
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import database_manager

class VistaRegistroAlumno(QWidget):
    def __init__(self):
        super().__init__()
        grupo_alumno = self._crear_grupo_alumno()
        grupo_tutor = self._crear_grupo_tutor()
        self.boton_registrar = QPushButton("Registrar Alumno")
        layout_botones = QHBoxLayout()
        layout_botones.addStretch()
        layout_botones.addWidget(self.boton_registrar)
        layout_botones.addStretch()
        layout_principal = QVBoxLayout(self)
        layout_principal.addWidget(grupo_alumno)
        layout_principal.addWidget(grupo_tutor)
        layout_principal.addLayout(layout_botones)
        self.boton_registrar.clicked.connect(self.registrar_datos)

    def _crear_grupo_alumno(self):
        grupo_alumno = QGroupBox("Datos del Alumno")
        layout = QFormLayout()
        self.nombre_alum = QLineEdit()
        self.apellido_pa = QLineEdit()
        self.apellido_ma = QLineEdit()
        self.direccion = QLineEdit()
        self.fecha_nacimiento = QDateEdit()
        self.fecha_nacimiento.setCalendarPopup(True)
        self.fecha_nacimiento.setDisplayFormat("dd/MM/yyyy")
        self.fecha_nacimiento.setDate(QDate.currentDate().addYears(-10))
        self.genero_m = QRadioButton("Masculino")
        self.genero_f = QRadioButton("Femenino")
        self.grupo_genero = QButtonGroup(self)
        self.grupo_genero.addButton(self.genero_m)
        self.grupo_genero.addButton(self.genero_f)
        layout_genero = QHBoxLayout()
        layout_genero.addWidget(self.genero_m)
        layout_genero.addWidget(self.genero_f)
        layout.addRow("Nombre(s):", self.nombre_alum)
        layout.addRow("Apellido Paterno:", self.apellido_pa)
        layout.addRow("Apellido Materno:", self.apellido_ma)
        layout.addRow("Dirección:", self.direccion)
        layout.addRow("Fecha de Nacimiento:", self.fecha_nacimiento)
        layout.addRow("Género:", layout_genero)
        grupo_alumno.setLayout(layout)
        return grupo_alumno

    def _crear_grupo_tutor(self):
        grupo_tutor = QGroupBox("Datos del Padre o Tutor")
        layout = QFormLayout()
        self.nombre_pad = QLineEdit()
        self.telefono = QLineEdit()
        self.correo = QLineEdit()
        self.correo.setPlaceholderText("ejemplo@correo.com")
        layout.addRow("Nombre Completo:", self.nombre_pad)
        layout.addRow("Teléfono:", self.telefono)
        layout.addRow("Correo Electrónico:", self.correo)
        grupo_tutor.setLayout(layout)
        return grupo_tutor

    def _limpiar_formulario(self):
        for line_edit in self.findChildren(QLineEdit):
            line_edit.clear()
        boton_chequeado = self.grupo_genero.checkedButton()
        if boton_chequeado:
            self.grupo_genero.setExclusive(False)
            boton_chequeado.setChecked(False)
            self.grupo_genero.setExclusive(True)
        self.fecha_nacimiento.setDate(QDate.currentDate().addYears(-10))

    def validar_correo(self, correo):
        patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(patron, correo) is not None

    @Slot()
    def registrar_datos(self):
        if not self.nombre_alum.text().strip() or not self.apellido_pa.text().strip():
            QMessageBox.warning(self, "Campos Incompletos", "El nombre y el apellido paterno son obligatorios.")
            return
        
        correo = self.correo.text().strip()
        if correo and not self.validar_correo(correo):
            QMessageBox.warning(self, "Correo Inválido", "El formato del correo electrónico no es válido. Debe ser: nombre@dominio.terminacion")
            return
            
        genero = "No especificado"
        if self.genero_m.isChecked():
            genero = "Masculino"
        elif self.genero_f.isChecked():
            genero = "Femenino"
        
        datos_alumno = {
            "nombre": self.nombre_alum.text().strip(),
            "apellido_paterno": self.apellido_pa.text().strip(),
            "apellido_materno": self.apellido_ma.text().strip(),
            "direccion": self.direccion.text().strip(),
            "fecha_nacimiento": self.fecha_nacimiento.date().toString("dd/MM/yyyy"),
            "genero": genero
        }
        datos_tutor = {
            "nombre_completo": self.nombre_pad.text().strip(),
            "telefono": self.telefono.text().strip(),
            "correo": correo
        }
        nuevo_id = database_manager.registrar_alumno(datos_alumno, datos_tutor)
        if nuevo_id:
            QMessageBox.information(self, "Éxito", f"¡Alumno registrado correctamente!\n\nEl ID asignado es: {nuevo_id}")
            self._limpiar_formulario()
        else:
            QMessageBox.critical(self, "Error de Base de Datos", "No se pudo registrar al alumno.")