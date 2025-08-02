from PySide6.QtWidgets import *
from PySide6.QtCore import *
import database_manager

class VistaInscripcion(QWidget):
    def __init__(self):
        super().__init__()
        layout_formulario = QFormLayout()
        self.fecha_inscripcion = QDateEdit()
        self.fecha_inscripcion.setCalendarPopup(True)
        self.fecha_inscripcion.setDate(QDate.currentDate())
        self.entry_id_alumno = QLineEdit()
        self.entry_id_alumno.setPlaceholderText("ID del alumno a inscribir")
        self.combo_grupo = QComboBox()
        self.entry_costo = QLineEdit("1500.00")
        self.entry_costo.setReadOnly(True)
        layout_formulario.addRow("Fecha de Inscripción:", self.fecha_inscripcion)
        layout_formulario.addRow("Número del Alumno:", self.entry_id_alumno)
        layout_formulario.addRow("Seleccionar Grupo:", self.combo_grupo)
        layout_formulario.addRow("Costo de Inscripción $:", self.entry_costo)
        self.boton_inscribir = QPushButton("Generar Inscripción")
        layout_principal = QVBoxLayout(self)
        layout_principal.addWidget(QLabel("<h2>Solicitud de Nueva Inscripción</h2>"))
        layout_principal.addLayout(layout_formulario)
        layout_principal.addStretch()
        layout_principal.addWidget(self.boton_inscribir)
        self.boton_inscribir.clicked.connect(self.generar_inscripcion)
    
    def refrescar_grupos(self):
        self.combo_grupo.clear()
        grupos = database_manager.obtener_grupos()
        self.combo_grupo.addItem("Seleccione un grupo", userData=None)
        if grupos:
            for grupo_id, nombre in grupos:
                self.combo_grupo.addItem(nombre, userData=grupo_id)

    @Slot()
    def generar_inscripcion(self):
        id_alumno = self.entry_id_alumno.text().strip()
        id_grupo = self.combo_grupo.currentData()
        if not id_alumno or id_grupo is None:
            QMessageBox.warning(self, "Campos Vacíos", "Debe ingresar el ID de alumno y seleccionar un grupo.")
            return
        if not database_manager.verificar_alumno_existente(id_alumno):
            QMessageBox.critical(self, "Error", f"El alumno con ID {id_alumno} no existe.")
            return
        fecha = self.fecha_inscripcion.date().toString("dd/MM/yyyy")
        costo = float(self.entry_costo.text())
        if database_manager.agregar_inscripcion(id_alumno, id_grupo, fecha, costo):
            recibo = (f"<b>Inscripción Exitosa</b><br><br>"
                      f"<b>Fecha:</b> {fecha}<br>"
                      f"<b>Alumno ID:</b> {id_alumno}<br>"
                      f"<b>Grupo:</b> {self.combo_grupo.currentText()}<br>"
                      f"<b>Costo Total:</b> ${costo:.2f}")
            QMessageBox.information(self, "Inscripción Generada", recibo)
            self.entry_id_alumno.clear()
        else:
            QMessageBox.critical(self, "Error", "No se pudo registrar la inscripción.")