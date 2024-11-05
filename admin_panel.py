from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
import sqlite3

class AdminPanelWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('admin_panel.ui', self)

        # Conectar botones
        self.btn_ver_aviones.clicked.connect(self.ver_aviones)
        self.btn_agregar_avion.clicked.connect(self.agregar_avion)
        self.btn_modificar_avion.clicked.connect(self.modificar_avion)
        self.btn_eliminar_avion.clicked.connect(self.eliminar_avion)

        # Cargar aviones al iniciar
        self.ver_aviones()

    def ejecutar_consulta(self, query, params=()):
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute(query, params)
        resultado = cursor.fetchall()
        conn.commit()
        conn.close()
        return resultado

    def ver_aviones(self):
        self.tabla_aviones.setRowCount(0)
        query = """
        SELECT matricula, nombre, marca, modelo, asientos_normal + asientos_turista + asientos_premium AS asientos, kilometraje, en_vuelo 
        FROM aviones
        """
        aviones = self.ejecutar_consulta(query)

        for row_number, avion in enumerate(aviones):
            self.tabla_aviones.insertRow(row_number)
            for column_number, data in enumerate(avion):
                self.tabla_aviones.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        self.actualizar_estadisticas()

    def agregar_avion(self):
        try:
            matricula = self.input_matricula.text()
            nombre = self.input_nombre.text()
            marca = self.input_marca.text()
            modelo = self.input_modelo.text()

            # Validar campos de asientos y kilometraje
            asientos_normal_text = self.input_asientos_normal.text()
            asientos_turista_text = self.input_asientos_turista.text()
            asientos_premium_text = self.input_asientos_premium.text()
            kilometraje_text = self.input_kilometraje.text()

            # Validar campos obligatorios
            if not matricula or not nombre or not marca or not modelo:
                raise ValueError("Todos los campos son obligatorios.")
            
            # Verificar que los campos de asientos y kilometraje no estén vacíos y sean numéricos
            if not (asientos_normal_text.isdigit() and asientos_turista_text.isdigit() and
                    asientos_premium_text.isdigit() and (kilometraje_text.replace('.', '', 1).isdigit())):
                raise ValueError("Los campos de asientos y kilometraje deben ser numéricos y no pueden estar vacíos.")

            asientos_normal = int(asientos_normal_text)
            asientos_turista = int(asientos_turista_text)
            asientos_premium = int(asientos_premium_text)
            kilometraje = float(kilometraje_text)
            en_vuelo = self.checkbox_en_vuelo.isChecked()

            query = '''
                INSERT INTO aviones (matricula, nombre, marca, modelo, asientos_normal, asientos_turista, asientos_premium, kilometraje, en_vuelo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            self.ejecutar_consulta(query, (matricula, nombre, marca, modelo, asientos_normal, asientos_turista, asientos_premium, kilometraje, en_vuelo))
            QMessageBox.information(self, "Éxito", "Avión agregado correctamente.")
            self.ver_aviones()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            QMessageBox.warning(self, "Error", "Error al agregar el avión: " + str(e))

    def modificar_avion(self):
        selected_row = self.tabla_aviones.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Selecciona un avión para modificar.")
            return

        try:
            matricula = self.tabla_aviones.item(selected_row, 0).text()
            nuevo_nombre = self.input_nombre.text()
            nuevo_kilometraje_text = self.input_kilometraje.text()

            if not nuevo_nombre:
                raise ValueError("El nombre del avión es obligatorio.")

            # Verificar que el kilometraje sea numérico
            if not nuevo_kilometraje_text.replace('.', '', 1).isdigit():
                raise ValueError("El kilometraje debe ser un número válido.")

            nuevo_kilometraje = float(nuevo_kilometraje_text)

            query = "UPDATE aviones SET nombre = ?, kilometraje = ? WHERE matricula = ?"
            self.ejecutar_consulta(query, (nuevo_nombre, nuevo_kilometraje, matricula))
            QMessageBox.information(self, "Éxito", "Avión modificado correctamente.")
            self.ver_aviones()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            QMessageBox.warning(self, "Error", "Error al modificar el avión: " + str(e))

    def eliminar_avion(self):
        selected_row = self.tabla_aviones.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Selecciona un avión para eliminar.")
            return

        matricula = self.tabla_aviones.item(selected_row, 0).text()
        query = "DELETE FROM aviones WHERE matricula = ?"
        self.ejecutar_consulta(query, (matricula,))
        QMessageBox.information(self, "Éxito", "Avión eliminado correctamente.")
        self.ver_aviones()

    def actualizar_estadisticas(self):
        total_query = "SELECT COUNT(*) FROM aviones"
        en_vuelo_query = "SELECT COUNT(*) FROM aviones WHERE en_vuelo = 1"

        total_aviones = self.ejecutar_consulta(total_query)[0][0]
        aviones_en_vuelo = self.ejecutar_consulta(en_vuelo_query)[0][0]

        if total_aviones > 0:
            porcentaje_en_vuelo = (aviones_en_vuelo / total_aviones) * 100
        else:
            porcentaje_en_vuelo = 0

        self.label_estadisticas.setText(f"Estadísticas: Total de Aviones: {total_aviones}, En Vuelo: {porcentaje_en_vuelo:.2f}%")

    def volver_menu_principal(self):
        self.close()  # Cierra el panel de administración y vuelve al menú principal