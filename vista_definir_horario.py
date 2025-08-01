import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *

class VistaDefinirHorario(QWidget):
    def __init__(self):
        super().__init__()
        self.dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        self.horas = ["08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-13:00"]
        
        layout_selector = QHBoxLayout()
        self.combo_grupos = QComboBox()
        layout_selector.addWidget(QLabel("Seleccionar Grupo:"))
        layout_selector.addWidget(self.combo_grupos)

        self.tabla_horario = QTableWidget(len(self.horas), len(self.dias))
        self.tabla_horario.setHorizontalHeaderLabels(self.dias)
        self.tabla_horario.setVerticalHeaderLabels(self.horas)
        header = self.tabla_horario.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.boton_guardar = QPushButton("Guardar Horario")

        layout_principal = QVBoxLayout(self)
        layout_principal.addWidget(QLabel("<h2>Definir Horario de Grupo</h2>"))
        layout_principal.addLayout(layout_selector)
        layout_principal.addWidget(QLabel("Selecciona una materia para cada celda:"))
        layout_principal.addWidget(self.tabla_horario)
        layout_principal.addWidget(self.boton_guardar)

        self.combo_grupos.currentTextChanged.connect(self.cargar_horario_existente)
        self.boton_guardar.clicked.connect(self.guardar_horario)

    def refrescar_grupos(self):
        try:
            self.combo_grupos.clear()
            self.grupos_data = {}
            if os.path.exists("grupos.txt"):
                with open("grupos.txt", "r", encoding="utf-8") as f:
                    for linea in f:
                        nombre, _, materias_str = linea.strip().split('|')
                        materias = materias_str.split(',')
                        self.combo_grupos.addItem(nombre)
                        self.grupos_data[nombre] = materias
            self.combo_grupos.setCurrentIndex(-1)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la lista de grupos: {e}")

    @Slot()
    def cargar_horario_existente(self, nombre_grupo):
        self.tabla_horario.clearContents()
        if not nombre_grupo: return

        materias_del_grupo = self.grupos_data.get(nombre_grupo, [])
        for fila in range(len(self.horas)):
            for col in range(len(self.dias)):
                combo_celda = QComboBox()
                combo_celda.addItem("")
                combo_celda.addItems(materias_del_grupo)
                self.tabla_horario.setCellWidget(fila, col, combo_celda)
        
        filename_horario = f"horario_{nombre_grupo}.txt"
        if os.path.exists(filename_horario):
            with open(filename_horario, "r", encoding="utf-8") as f:
                for linea in f:
                    fila, col, materia = linea.strip().split(',')
                    combo_en_celda = self.tabla_horario.cellWidget(int(fila), int(col))
                    if combo_en_celda:
                        combo_en_celda.setCurrentText(materia)

    @Slot()
    def guardar_horario(self):
        nombre_grupo = self.combo_grupos.currentText()
        if not nombre_grupo:
            QMessageBox.warning(self, "Sin Selección", "Por favor, seleccione un grupo antes de guardar.")
            return

        filename_horario = f"horario_{nombre_grupo}.txt"
        try:
            with open(filename_horario, "w", encoding="utf-8") as f:
                for fila in range(self.tabla_horario.rowCount()):
                    for col in range(self.tabla_horario.columnCount()):
                        combo_en_celda = self.tabla_horario.cellWidget(fila, col)
                        if combo_en_celda and combo_en_celda.currentText() != "":
                            materia = combo_en_celda.currentText()
                            f.write(f"{fila},{col},{materia}\n")
            QMessageBox.information(self, "Éxito", f"Horario para el grupo '{nombre_grupo}' guardado.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el archivo de horario: {e}")