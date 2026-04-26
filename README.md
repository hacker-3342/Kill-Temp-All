<p align="center">
  <img src="https://github.com/user-attachments/assets/ad14de91-cf3b-416b-8f43-56817634be43" style="width: 200px;" alt="resized_logo" />
</p>

<h1 align="center">Kill Temp All</h1>

<p align="center">
  <a href="#"><img src="https://custom-icon-badges.demolab.com/badge/Windows-0078D6?logo=windows11&logoColor=white" alt="Windows"></a>
  <a href="#"><img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff" alt="Python"></a>
  <a href="#"><img src="https://img.shields.io/badge/Markdown-%23000000.svg?logo=markdown&logoColor=white" alt="Markdown"></a>
  <img src="https://img.shields.io/github/last-commit/hacker-3342/Kill-Temp-All" alt="GitHub Last Commit">
  <img src="https://img.shields.io/github/issues-closed/hacker-3342/Kill-Temp-All" alt="GitHub Issues or Pull Requests">
  <img src="https://img.shields.io/github/license/hacker-3342/Kill-Temp-All" alt="GitHub License">
  <img src="https://img.shields.io/github/languages/code-size/hacker-3342/Kill-Temp-All" alt="GitHub code size in bytes">
  <img src="https://img.shields.io/github/stars/hacker-3342/Kill-Temp-All" alt="GitHub Repo stars">
</p>

---

## 🇪🇸 Español

### Introducción

¿Estás harto de que los programas de Adobe (InDesign, Photoshop, After Effects) generen archivos temporales por todo el sistema?  
Este programa en Python con una interfaz gráfica en PyQt6 soluciona ese problema y te puede liberar muchos GiB de espacio en tu equipo.

### Instalación en Windows

Haz clic en la pestaña *releases* o *lanzamientos* de la página de GitHub y descarga la versión más reciente.

Coloca los archivos y carpetas donde tú quieras.

#### Compilar desde el código fuente (solo Windows)

Actualmente, todas las bibliotecas vienen incluidas con Python (os, shutil...) excepto PyQt6, la cual debe ser instalada mediante pip, 
o tu organizador de paquetes para Python.
Este programa fue desarrollado usando **Python 3.13.1**.

```
python --version
# o
python3 --version
````

Luego ejecuta:

```
python main.py
# o
python3 main.py
```

### Documentación

#### Funcionalidades

Kill Temp All permite seleccionar con checkboxes qué archivos, carpetas o rutas quieres analizar en tu PC
para eliminar caché y archivos temporales de Adobe.

También permite cambiar fácilmente entre idiomas con un menú desplegable. A fecha de 06/02/2025, los idiomas disponibles son:

* Español
* Inglés

Todos los paquetes de idiomas se encuentran en la carpeta *Languages/* y cada uno es un archivo JSON (*.json*).

**Se necesitan y se aprecian traductores a otros idiomas.**

Además, Kill Temp All guarda la configuración de varios parámetros en el archivo *settings.ini*. Estos parámetros son:

* El estado de cada checkbox (*var0, var1, etc.*)
* El idioma preferido (si no se encuentra, se usará el inglés por defecto).

### Reportar errores

Si encuentras algún error en el programa, sería de gran ayuda que reportaras un *issue* o *bug* aquí:
[Página de Issues del repositorio](https://github.com/hacker-3342/Kill-Temp-All/issues)

Antes de hacerlo, asegúrate de estar usando la versión más reciente.

### Recomendaciones

Si tienes una sugerencia para mejorar la app, no dudes en enviarla por correo a: [hectoruru@outlook.es](mailto:hectoruru@outlook.es). ¡Gracias!

---

## 🇬🇧 English

### Introduction

Tired of Adobe programs (InDesign, Photoshop, After Effects) generating temporary files all over your system?
This Python program with a PyQt6 GUI will solve that problem and free many GiB of space on your computer.

### Installation on Windows

Click on the *releases* tab on the GitHub page and download the latest one.

Place the files & folders wherever you want.

#### Building from source (Windows only)

Currently, all libraries come installed with Python itself (os, shutil...) except PyQt6, which you will need to install
via pip or your system's python package manager.
This program was developed using **Python 3.13.1**.

```
python --version
# or
python3 --version
```

Then run:

```
python main.py
# or
python3 main.py
```

### Documentation

#### Features

Kill Temp All allows the user to select with checkboxes which files, folders or paths to search on the computer
and remove Adobe cache files there.

Kill Temp All also allows easy changing between languages via a drop-down menu. As of 06/02/2025, these are the language packs:

* English
* Spanish

All language packs are located inside the *Languages/* folder, and each of them is a JSON file (*.json*).

**Translators for other languages would be really appreciated.**

Last but not least, Kill Temp All saves the configuration of different parameters in *settings.ini*.
Those parameters are:

* Checkbox status (*var0, var1, etc.*)
* Preferred language (defaults to English if the desired one isn't found).

### Error reporting

If you encounter an error in the code, it would be greatly appreciated if you could file a bug report here:
[Repository's Issue Page](https://github.com/hacker-3342/Kill-Temp-All/issues)

Before writing a bug report, make sure you're on the newest version.

### Recommendations

If you have a recommendation to make the application better, feel free to send an email to [hectoruru@outlook.es](mailto:hectoruru@outlook.es). Thank you!