import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *

class VistaHorario(QWidget):
    def __init__(self):
        super().__init__()
        self.dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        self.horas = ["08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-13:00"]

        self.combo_grupos = QComboBox()
        self.combo_grupos.setPlaceholderText("Seleccione un grupo para ver su horario")

        self.tabla_horario = QTableWidget(len(self.horas), len(self.dias))
        self.tabla_horario.setHorizontalHeaderLabels(self.dias)
        self.tabla_horario.setVerticalHeaderLabels(self.horas)
        header = self.tabla_horario.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_horario.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout_principal = QVBoxLayout(self)
        layout_principal.addWidget(QLabel("<h2>Consulta de Horario por Grupo</h2>"))
        layout_principal.addWidget(self.combo_grupos)
        layout_principal.addWidget(self.tabla_horario)

        self.combo_grupos.currentTextChanged.connect(self.actualizar_horario)

    def refrescar_grupos(self):
        try:
            self.combo_grupos.clear()
            self.combo_grupos.setPlaceholderText("Seleccione un grupo para ver su horario")
            if os.path.exists("grupos.txt"):
                with open("grupos.txt", "r", encoding="utf-8") as archivo:
                    for linea in archivo:
                        self.combo_grupos.addItem(linea.strip().split('|')[0])
            self.combo_grupos.setCurrentIndex(-1)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la lista de grupos: {e}")

    @Slot()
    def actualizar_horario(self, nombre_grupo):
        self.tabla_horario.clearContents()
        if not nombre_grupo: return

        filename_horario = f"horario_{nombre_grupo}.txt"
        if not os.path.exists(filename_horario):
            return 
            
        try:
            with open(filename_horario, "r", encoding="utf-8") as f:
                for linea in f:
                    fila, col, materia = linea.strip().split(',')
                    item = QTableWidgetItem(materia)
                    self.tabla_horario.setItem(int(fila), int(col), item)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al cargar el horario: {e}")