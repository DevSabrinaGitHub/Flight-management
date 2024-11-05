import sys
from PyQt5 import QtWidgets, uic
from reservas_panel import ReservasPanelWindow
from admin_panel import AdminPanelWindow

class MenuPrincipalWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('menu_principal.ui', self)

        # Conectar botones
        self.btn_gestionar_reservas.clicked.connect(self.abrir_gestion_reservas)
        self.btn_gestionar_vuelos.clicked.connect(self.abrir_gestion_vuelos)

    def abrir_gestion_reservas(self):
        self.gestion_reservas = ReservasPanelWindow()
        self.gestion_reservas.show()

    def abrir_gestion_vuelos(self):
        self.gestion_vuelos = AdminPanelWindow()
        self.gestion_vuelos.show()

# Para ejecutar la ventana de menú principal
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    menu = MenuPrincipalWindow()
    menu.show()
    sys.exit(app.exec_())
