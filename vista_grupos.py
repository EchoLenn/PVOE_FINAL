import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *

class VistaGrupos(QWidget):
    def __init__(self):
        super().__init__()

        layout_formulario = QFormLayout()

        self.entry_nombre_grupo = QLineEdit()
        self.entry_nombre_grupo.setPlaceholderText("Ej: Grupo A-1")

        self.lista_profesores = QListWidget()
        self.lista_profesores.addItems(["Prof. Ana García", "Prof. Carlos Rivas", "Prof. Laura Méndez"])
        self.lista_profesores.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        self.lista_materias = QListWidget()
        self.lista_materias.addItems(["Matemáticas", "Ciencias", "Historia", "Español", "Programación Visual", "Arte"])
        self.lista_materias.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        layout_formulario.addRow("Nombre del Grupo:", self.entry_nombre_grupo)
        layout_formulario.addRow("Seleccionar Profesor:", self.lista_profesores)
        layout_formulario.addRow("Seleccionar Materias:", self.lista_materias)

        self.boton_generar = QPushButton("Generar Grupo")

        layout_principal = QVBoxLayout(self)
        layout_principal.addWidget(QLabel("<h2>Generación de Nuevos Grupos</h2>"))
        layout_principal.addLayout(layout_formulario)
        layout_principal.addWidget(self.boton_generar)

        self.boton_generar.clicked.connect(self.generar_grupo)

    @Slot()
    def generar_grupo(self):
        nombre_grupo = self.entry_nombre_grupo.text().strip()
        profesores_seleccionados = self.lista_profesores.selectedItems()
        materias_seleccionadas = self.lista_materias.selectedItems()

        if not nombre_grupo:
            QMessageBox.warning(self, "Campo Vacío", "Debe ingresar un nombre para el grupo.")
            return
        if not profesores_seleccionados:
            QMessageBox.warning(self, "Selección Requerida", "Debe seleccionar un profesor para el grupo.")
            return
        if not materias_seleccionadas:
            QMessageBox.warning(self, "Selección Requerida", "Debe seleccionar al menos una materia para el grupo.")
            return

        profesor = profesores_seleccionados[0].text()
        materias = [item.text() for item in materias_seleccionadas]

        try:
            with open("grupos.txt", "a", encoding="utf-8") as archivo:
                archivo.write(f"{nombre_grupo}|{profesor}|{','.join(materias)}\n")
            
            QMessageBox.information(self, "Éxito", f"El grupo '{nombre_grupo}' ha sido creado exitosamente.")
            self.entry_nombre_grupo.clear()
            self.lista_profesores.clearSelection()
            self.lista_materias.clearSelection()

        except Exception as e:
            QMessageBox.critical(self, "Error al Guardar", f"No se pudo guardar el archivo de grupos:\n{e}")