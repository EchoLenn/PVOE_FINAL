import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
import database_manager

class VistaHorario(QWidget):
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
        layout_principal.addWidget(QLabel("<h2>Gestión de Horario por Grupo</h2>"))
        layout_principal.addLayout(layout_selector)
        layout_principal.addWidget(QLabel("Selecciona una materia para cada celda:"))
        layout_principal.addWidget(self.tabla_horario)
        layout_principal.addWidget(self.boton_guardar)

        self.combo_grupos.currentTextChanged.connect(self.cargar_horario)
        self.boton_guardar.clicked.connect(self.guardar_horario)

    def refrescar_grupos(self):
        self.combo_grupos.clear()
        grupos = database_manager.obtener_grupos()
        self.combo_grupos.addItem("Seleccione un grupo", userData=None)
        for grupo_id, nombre in grupos:
            self.combo_grupos.addItem(nombre, userData=grupo_id)

    @Slot()
    def cargar_horario(self, _):
        self.tabla_horario.clear()
        self.tabla_horario.setHorizontalHeaderLabels(self.dias)
        self.tabla_horario.setVerticalHeaderLabels(self.horas)

        id_grupo = self.combo_grupos.currentData()
        if not id_grupo: return

        materias_del_grupo = database_manager.obtener_materias_por_grupo(id_grupo)
        horario_guardado = database_manager.obtener_horario(id_grupo)
        
        horario_map = { (dia, hora): materia for dia, hora, materia in horario_guardado }

        for fila, hora in enumerate(self.horas):
            for col, dia in enumerate(self.dias):
                combo_celda = QComboBox()
                combo_celda.addItem("")
                combo_celda.addItems(materias_del_grupo)
                
                materia_guardada = horario_map.get((dia, hora))
                if materia_guardada:
                    combo_celda.setCurrentText(materia_guardada)

                self.tabla_horario.setCellWidget(fila, col, combo_celda)

    @Slot()
    def guardar_horario(self):
        id_grupo = self.combo_grupos.currentData()
        if not id_grupo:
            QMessageBox.warning(self, "Sin Selección", "Seleccione un grupo.")
            return

        datos_horario = []
        for fila, hora in enumerate(self.horas):
            for col, dia in enumerate(self.dias):
                combo = self.tabla_horario.cellWidget(fila, col)
                if combo and combo.currentText() != "":
                    materia = combo.currentText()
                    datos_horario.append((id_grupo, dia, hora, materia))
        
        if database_manager.guardar_horario(id_grupo, datos_horario):
            QMessageBox.information(self, "Éxito", f"Horario para el grupo '{self.combo_grupos.currentText()}' guardado.")
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar el horario.")