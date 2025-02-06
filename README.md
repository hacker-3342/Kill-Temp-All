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

## Introduction

Tired of Adobe programs (InDesign, Photoshop, After Effects) generating temporary files all over your system? This Python program with a Tkinter GUI will solve that problem and 
free many GiB of space on your computer.

## Installation on Windows

Click on the *releases* tab on the GitHub page and download the latest one.

Place the files & folders wherever you want.

### Building from source (Windows only)

Currently, all libraries come installed with Python itself. (Tkinter, os, shutil...). I have used Python 3.13.1 to make this program.

`python --version`

`Python 3.13.1`

if that doesn't work, try the following:

`python3 --version`

Next, do:
`python main.py`
or
`python3 main.py`.

## Documentation

### Features

Kill Temp All allows the user to select with checkboxes which files, folders or paths to search on the computer
and remove Adobe cache files there.

Kill Temp All also allows easy changing between languages via a drop-down menu, where language packs will be loaded
and shown for the user to choose. As of 06/02/2025, these are the language packs:

- English
- Spanish

All language packs are located inside the *Languages/* folder, and each of them is a JSON file (*.json*)

**Translators for other languages would be really appreciated.**

Last but not least, Kill Temp All saves the configuration of different parameters in *settings.ini*. 
Those parameters are:
- Checkbox status (*var0, var1, etc.*)
- Preferred language (defaults to English if the desired one isn't found).

## Error reporting
If you encounter an error on the program, it would be greatly appreciated for you to write a bug report here: [Repository's Issue Page](https://github.com/hacker-3342/Kill-Temp-All/issues).

Before writing a bug report, make sure you're on the newest version.

## Recommendations
If you have a recommendation to make the application better, I encourage you to write an email to <hectoruru@outlook.es>. Thank You!
