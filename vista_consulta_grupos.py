import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
import database_manager

class VistaConsultaGrupos(QWidget):
    def __init__(self):
        super().__init__()
        self.combo_grupos = QComboBox()
        self.combo_grupos.setPlaceholderText("Seleccione un grupo para ver los alumnos")
        self.tabla_alumnos = QTableWidget()
        self.tabla_alumnos.setColumnCount(2)
        self.tabla_alumnos.setHorizontalHeaderLabels(["ID Alumno", "Nombre Completo del Alumno"])
        header = self.tabla_alumnos.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.tabla_alumnos.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout_principal = QVBoxLayout(self)
        layout_principal.addWidget(QLabel("<h2>Consultar Alumnos por Grupo</h2>"))
        layout_principal.addWidget(self.combo_grupos)
        layout_principal.addWidget(self.tabla_alumnos)
        self.combo_grupos.currentTextChanged.connect(self.actualizar_alumnos)

    def refrescar_grupos(self):
        """Obtiene los grupos de la DB y los pone en el ComboBox."""
        self.combo_grupos.clear()
        grupos = database_manager.obtener_grupos()
        self.combo_grupos.addItem("Seleccione un grupo", userData=None)
        for grupo_id, nombre in grupos:
            self.combo_grupos.addItem(nombre, userData=grupo_id)
        self.combo_grupos.setCurrentIndex(0)

    @Slot()
    def actualizar_alumnos(self, _):
        """Muestra en la tabla los alumnos inscritos en el grupo seleccionado."""
        self.tabla_alumnos.setRowCount(0)
        id_grupo = self.combo_grupos.currentData()
        if not id_grupo: return
        
        alumnos_en_grupo = database_manager.obtener_alumnos_por_grupo(id_grupo)
        
        self.tabla_alumnos.setRowCount(len(alumnos_en_grupo))
        for fila, (id_val, nombre, p, m) in enumerate(alumnos_en_grupo):
            nombre_completo = f"{nombre} {p} {m}".strip()
            self.tabla_alumnos.setItem(fila, 0, QTableWidgetItem(str(id_val)))
            self.tabla_alumnos.setItem(fila, 1, QTableWidgetItem(nombre_completo))