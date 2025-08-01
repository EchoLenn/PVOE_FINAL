from PySide6.QtWidgets import *
from PySide6.QtCore import *

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
        self.combo_grupo.addItems(["Grupo A-1", "Grupo B-1", "Grupo C-1"])

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

    @Slot()
    def generar_inscripcion(self):
        id_alumno = self.entry_id_alumno.text().strip()

        if not id_alumno:
            QMessageBox.warning(self, "Campo Vacío", "Debe ingresar el número del alumno.")
            return

        fecha = self.fecha_inscripcion.date().toString("dd/MM/yyyy")
        grupo = self.combo_grupo.currentText()
        costo = self.entry_costo.text()

        recibo = (
            f"<b>Inscripción Exitosa</b><br><br>"
            f"<b>Fecha:</b> {fecha}<br>"
            f"<b>Alumno ID:</b> {id_alumno}<br>"
            f"<b>Grupo:</b> {grupo}<br>"
            f"<b>Costo Total:</b> ${costo}"
        )

        try:
            with open("inscripciones.txt", "a", encoding="utf-8") as archivo:
                archivo.write(f"ID:{id_alumno},Fecha:{fecha},Grupo:{grupo},Costo:{costo}\n")
            
            QMessageBox.information(self, "Inscripción Generada", recibo)
            self.entry_id_alumno.clear()

        except Exception as e:
            QMessageBox.critical(self, "Error al Guardar", f"No se pudo guardar el archivo de inscripciones:\n{e}")