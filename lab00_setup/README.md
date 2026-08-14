# Lab 00 - Software Setup and Webots Basics

## Mission

Install the course software and learn the minimum Webots skills needed to begin Lab 1.

Lab 00 has two required outcomes:

1. the supported software is installed and working; and
2. Webots Tutorials 1 and 4 are completed using Python.

There is no UR5e mathematics or graded robot experiment in this lab.

## Required Software

Install the following before opening a course lab:

- Windows 10 or Windows 11
- stable **Webots R2025a** (do not use a nightly or development build)
- **Python 3.11 or 3.12, 64-bit**, installed from [python.org](https://www.python.org/downloads/windows/)
- Visual Studio Code
- Git
- NumPy and Matplotlib

Keep the repository in a short local path such as `C:\eel4664-ur5e-labs`. Avoid OneDrive, SharePoint, network drives, and deeply nested paths.

## Part 1 - Install Python and Packages

1. Download the 64-bit Windows installer from [python.org](https://www.python.org/downloads/windows/).
2. On the first installer screen, check **Add python.exe to PATH**.
3. Complete a normal CPython installation. Do not rely on the Microsoft Store package or Windows App Execution Alias.
4. Open a new PowerShell window and run:

   ```powershell
   python --version
   where.exe python
   ```

5. Confirm that the version is Python 3.11 or 3.12 and that `where.exe python` identifies the python.org installation.
6. Install the required packages:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install numpy matplotlib
   python -c "import numpy as np; print(np.__version__)"
   ```

If more than one Python installation exists, use `py -0p` to list their full paths.

## Part 2 - Install and Configure Webots

1. Install stable **Webots R2025a**.
2. Open Webots and confirm **Help -> About** reports R2025a.
3. Open **Tools -> Preferences -> General**.
4. Set **Python command** to the full path of the Python 3.11 or 3.12 `python.exe`, for example:

   ```text
   C:\Users\<username>\AppData\Local\Programs\Python\Python312\python.exe
   ```

5. Apply the change and restart Webots.

Do not leave **Python command** blank.

## Part 3 - Complete the Required Webots Tutorials

Complete these two official Cyberbotics tutorials using Webots R2025a:

1. [Tutorial 1 - Your First Simulation in Webots](https://cyberbotics.com/doc/guide/tutorial-1-your-first-simulation-in-webots?version=R2025a)

   Learn how to open or create a world, run/pause/reset a simulation, use the Scene Tree, and save a world.

2. [Tutorial 4 - More About Controllers](https://cyberbotics.com/doc/guide/tutorial-4-more-about-controllers?tab-language=python&version=R2025a)

   Complete the **Python controller** portion. Confirm that Webots starts the controller, prints its console output, reads devices, and continues stepping without crashing.

   Because Tutorials 2 and 3 are optional, start Tutorial 4 from the completed Cyberbotics sample `C:\Program Files\Webots\projects\samples\tutorials\worlds\appearance.wbt`. Immediately use **File -> Save World As...** to save a working copy outside `C:\Program Files\Webots`, then follow Tutorial 4 on that copy.

Tutorials 2 and 3 are optional. You do not need to complete them for Lab 00.

## Lab 00 Completion Checklist

- [ ] Webots R2025a launches normally
- [ ] Python 3.11 or 3.12, 64-bit, is installed
- [ ] `python --version` works
- [ ] NumPy imports successfully
- [ ] Git and VS Code are available
- [ ] Webots **Python command** points to the correct `python.exe`
- [ ] Webots Tutorial 1 is complete
- [ ] The Python portion of Webots Tutorial 4 is complete
- [ ] A Python controller runs without crashing

When every item passes, continue to [Lab 1](../lab01_webots_ur5e_frames/README.md).

## What to Submit

Submit the instructor-requested evidence, normally:

- a screenshot of **Help -> About** showing Webots R2025a;
- PowerShell output from `python --version` and the NumPy import command;
- a screenshot of the completed Tutorial 1 world; and
- Tutorial 4 Python-controller console output.

Do not submit installed software or the Webots installation directory.

## Troubleshooting

If `python --version` fails, reinstall Python from python.org with **Add python.exe to PATH** selected, then open a new PowerShell window.

If a C controller runs but a Python controller fails, locate Python with `where.exe python` or `py -0p`, enter the full interpreter path in Webots Preferences, restart Webots, and retry Tutorial 4.

For repeated Webots crashes, blank scenes, or recovery mode, use [Troubleshooting Webots](../docs/TROUBLESHOOTING_WEBOTS.md).
