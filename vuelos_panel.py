from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox
import sqlite3

class VuelosPanelWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('vuelos_panel.ui', self)

        # Conectar botones a las funciones correspondientes
        self.btn_ver_vuelos.clicked.connect(self.ver_vuelos)
        self.btn_agregar_vuelo.clicked.connect(self.agregar_vuelo)
        self.btn_modificar_vuelo.clicked.connect(self.modificar_vuelo)
        self.btn_eliminar_vuelo.clicked.connect(self.eliminar_vuelo)
        self.btn_volver_menu.clicked.connect(self.volver_menu_principal)  # Asegúrate de que este botón esté conectado

        # Cargar la lista de vuelos al abrir la ventana
        self.ver_vuelos()

    def ejecutar_consulta(self, query, params=()):
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute(query, params)
        resultado = cursor.fetchall()
        conn.commit()
        conn.close()
        return resultado

    def ver_vuelos(self):
        self.tabla_vuelos.setRowCount(0)
        query = """
        SELECT v.id, a.nombre AS avion, v.ciudad_origen, v.ciudad_destino, 
               v.fecha_partida, v.fecha_llegada, 
               ROUND((SELECT COUNT(*) FROM reservas WHERE vuelo_id = v.id) * 100.0 / (
               SELECT SUM(asientos_normal + asientos_turista + asientos_premium) FROM aviones WHERE id = v.avion_id), 2) AS porcentaje_reservas
        FROM vuelos v
        JOIN aviones a ON v.avion_id = a.id
        """
        vuelos = self.ejecutar_consulta(query)

        for row_number, vuelo in enumerate(vuelos):
            self.tabla_vuelos.insertRow(row_number)
            for column_number, data in enumerate(vuelo):
                item = QtWidgets.QTableWidgetItem(str(data))
                # Asignar color de fondo según el porcentaje de reservas
                if column_number == 6:  # Columna de porcentaje
                    porcentaje = float(data)
                    if porcentaje <= 40:
                        item.setBackground(QtGui.QColor("red"))
                    elif 41 <= porcentaje <= 60:
                        item.setBackground(QtGui.QColor("orange"))
                    elif 61 <= porcentaje <= 80:
                        item.setBackground(QtGui.QColor("lightgreen"))
                    else:
                        item.setBackground(QtGui.QColor("darkgreen"))
                self.tabla_vuelos.setItem(row_number, column_number, item)

    def agregar_vuelo(self):
        # Abrir un diálogo para ingresar datos del vuelo
        dialog = VueloDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            avion_id, origen, destino, fecha_partida, fecha_llegada = dialog.get_data()

            # Insertar el nuevo vuelo en la base de datos
            query = '''
            INSERT INTO vuelos (avion_id, ciudad_origen, ciudad_destino, fecha_partida, fecha_llegada)
            VALUES (?, ?, ?, ?, ?)
            '''
            self.ejecutar_consulta(query, (avion_id, origen, destino, fecha_partida, fecha_llegada))
            QMessageBox.information(self, "Éxito", "Vuelo agregado correctamente.")
            self.ver_vuelos()

    def modificar_vuelo(self):
        selected_row = self.tabla_vuelos.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Seleccione un vuelo para modificar.")
            return

        vuelo_id = self.tabla_vuelos.item(selected_row, 0).text()

        # Obtener datos actuales del vuelo seleccionado
        query = "SELECT avion_id, ciudad_origen, ciudad_destino, fecha_partida, fecha_llegada FROM vuelos WHERE id = ?"
        vuelo = self.ejecutar_consulta(query, (vuelo_id,))
        if vuelo:
            avion_id, origen, destino, fecha_partida, fecha_llegada = vuelo[0]

            # Abrir un diálogo para modificar los datos del vuelo
            dialog = VueloDialog(self, avion_id, origen, destino, fecha_partida, fecha_llegada)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                avion_id, origen, destino, fecha_partida, fecha_llegada = dialog.get_data()

                # Actualizar el vuelo en la base de datos
                update_query = '''
                UPDATE vuelos 
                SET avion_id = ?, ciudad_origen = ?, ciudad_destino = ?, fecha_partida = ?, fecha_llegada = ?
                WHERE id = ?
                '''
                self.ejecutar_consulta(update_query, (avion_id, origen, destino, fecha_partida, fecha_llegada, vuelo_id))
                QMessageBox.information(self, "Éxito", "Vuelo modificado correctamente.")
                self.ver_vuelos()

    def eliminar_vuelo(self):
        selected_row = self.tabla_vuelos.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Seleccione un vuelo para eliminar.")
            return

        vuelo_id = self.tabla_vuelos.item(selected_row, 0).text()
        query = "DELETE FROM vuelos WHERE id = ?"
        self.ejecutar_consulta(query, (vuelo_id,))
        QMessageBox.information(self, "Éxito", "Vuelo eliminado correctamente.")
        self.ver_vuelos()

    def volver_menu_principal(self):
        self.close()  # Cierra el panel de vuelos y vuelve al menú principal

class VueloDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, avion_id=None, origen=None, destino=None, fecha_partida=None, fecha_llegada=None):
        super().__init__(parent)
        uic.loadUi('vuelo_dialog.ui', self)

        # Rellenar campos si se proporciona la información para modificar
        if avion_id is not None:
            self.input_avion_id.setText(str(avion_id))
            self.input_origen.setText(origen)
            self.input_destino.setText(destino)
            self.input_fecha_partida.setDate(QtCore.QDate.fromString(fecha_partida, "yyyy-MM-dd"))
            self.input_fecha_llegada.setDate(QtCore.QDate.fromString(fecha_llegada, "yyyy-MM-dd"))

    def get_data(self):
        avion_id = int(self.input_avion_id.text())
        origen = self.input_origen.text()
        destino = self.input_destino.text()
        fecha_partida = self.input_fecha_partida.date().toString("yyyy-MM-dd")
        fecha_llegada = self.input_fecha_llegada.date().toString("yyyy-MM-dd")
        return avion_id, origen, destino, fecha_partida, fecha_llegada
