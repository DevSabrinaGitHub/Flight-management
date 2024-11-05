# Sistema de Gestión de Aerolínea
Este proyecto es un sistema de gestión para una aerolínea que permite gestionar información de usuarios, aviones y reservas, y está desarrollado en Python utilizando PyQt para la interfaz gráfica y SQLite como base de datos.

## Funcionalidad del Proyecto
El sistema permite realizar las siguientes operaciones:

1. **Inicio de sesión de Usuarios**: Los usuarios pueden iniciar sesión con su nombre de usuario y contraseña. Solo los usuarios con permisos pueden acceder al panel de administración.
2. **Administración de Usuarios**: Permite agregar y ver usuarios del sistema. Incluye funcionalidad de hash para almacenar contraseñas de forma segura.
3. **Administración de Aviones**: Ofrece CRUD (Crear, Leer, Actualizar, Eliminar) de aviones, y estadísticas de uso de la flota.

### Estructura de Archivos

- `conexion_db.py`: Este archivo gestiona la conexión a la base de datos SQLite y las funciones para ejecutar consultas. Asume que las tablas están previamente creadas en la base de datos `gestion_aerolinea.db`.
- `main.py`: Archivo principal de la aplicación que implementa la lógica de inicio de sesión y panel administrativo, utilizando PyQt para la interfaz gráfica.

### Interfaz de Usuario

El proyecto utiliza archivos `.ui` generados por PyQt Designer para las interfaces:
- `login.ui`: Interfaz de inicio de sesión.
- `panel_admin.ui`: Panel de administración donde se gestionan usuarios y aviones.

## Instalación y Configuración
2. Crear el Entorno Virtual
Crea un entorno virtual para instalar las dependencias del proyecto.
    python -m venv env

### Activa el entorno virtual:
.\env\Scripts\activate

### 3. Instalar Dependencias Instala las librerías requeridas (PyQt5 y SQLite3).
pip install PyQt5 sqlite3

### 4. Configuración de la Base de Datos : 
colocar el archivo base datos aca

### 5. Ejecución de la Aplicación
python main.py


### Explicación del Código
conexion.py Este archivo contiene las funciones necesarias para conectar y operar con SQLite
crear_conexion(): Establece la conexión con la base de datos gestion_aerolinea.db.
ejecutar_consulta(): Ejecuta una consulta de lectura en la base de datos.
ejecutar_comando(): Ejecuta comandos de escritura en la base de datos (e.g., INSERT, UPDATE, DELETE).


main.py
Este archivo implementa la lógica principal de la aplicación, incluyendo:
Inicio de Sesión: Verifica el nombre de usuario y la contraseña, que están almacenados en la tabla usuarios.
Panel Administrativo: Ofrece un panel para gestionar usuarios y aviones.
Agregar Usuario: Permite agregar un nuevo usuario al sistema, almacenando su contraseña
Ver Usuarios: Muestra una tabla con todos los usuarios registrados en el sistema.
Archivos de Interfaz .ui
Los archivos .ui contienen el diseño visual creado en PyQt Designer. asegurar el archivo login.ui y panel_admin.ui en el mismo directorio que main.py. o los archivos ui



### 1. Clonar el Repositorio
Clonar este repositorio
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>

