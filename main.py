import sys
from PyQt5 import QtWidgets
from login import LoginWindow
from menu_principal import MenuPrincipalWindow  # Importar el menú principal

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Inicializar ventana de login
        self.login_window = LoginWindow()
        self.login_window.show()

        # Conectar la señal de login exitoso para abrir el menú principal
        self.login_window.login_exitoso.connect(self.mostrar_menu_principal)

    def mostrar_menu_principal(self):
        self.login_window.close()
        # Cargar el menú principal
        self.menu_principal = MenuPrincipalWindow()
        self.menu_principal.show()

# Inicializar aplicación
app = QtWidgets.QApplication(sys.argv)
ventana = MainApp()
ventana.show()
sys.exit(app.exec_())
