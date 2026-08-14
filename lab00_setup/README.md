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
- **Python 3.11 or newer**, 64-bit, installed from [python.org](https://www.python.org/downloads/windows/)
- [Git for Windows](https://git-scm.com/download/win)
- [Visual Studio Code](https://code.visualstudio.com/download)
- NumPy and Matplotlib

Git is required to obtain course updates, track controller code, and restore a damaged starter file. VS Code is the course-supported code editor and is used in the instructions. Webots does not technically depend on VS Code, but students should use it unless the instructor approves another editor.

Keep the repository in a short local path such as `C:\eel4664-robotics-labs`. Avoid OneDrive, SharePoint, network drives, and deeply nested paths.

## Part 1 - Install and Configure Git

1. Download **Git for Windows** from [git-scm.com](https://git-scm.com/download/win).
2. Run the installer. The default options are appropriate for this course. Keep the option that allows Git to run from PowerShell and other third-party software.
3. Close any existing PowerShell windows, open a new one, and verify the installation:

   ```powershell
   git --version
   where.exe git
   ```

4. Set the name and email that Git will record in your commits. Replace the examples with your real information:

   ```powershell
   git config --global user.name "Your Full Name"
   git config --global user.email "your.email@example.com"
   ```

   If you use GitHub, use an email connected to your GitHub account, or use your GitHub-provided private `noreply` address if you do not want to expose a personal email in commits.

5. Verify the saved values:

   ```powershell
   git config --global --get user.name
   git config --global --get user.email
   git config --list --show-origin
   ```

6. Clone [**eel4664-robotics-labs**](https://github.com/hoanbklucky/eel4664-robotics-labs-webots-version/tree/main) into the required local folder:

   ```powershell
   cd C:\
   git clone https://github.com/hoanbklucky/eel4664-robotics-labs-webots-version.git eel4664-robotics-labs
   cd C:\eel4664-robotics-labs
   git status --short
   ```

   Run `git clone` only once. If the repository already exists at this location, do not clone over it.

The `--global` setting normally needs to be completed only once on each computer. Every commit records this identity, as explained in the official [First-Time Git Setup](https://git-scm.com/book/ms/v2/Getting-Started-First-Time-Git-Setup).

## Part 2 - Install Visual Studio Code

1. Download the Windows **User Installer** from [code.visualstudio.com](https://code.visualstudio.com/download). The User Installer is recommended for most students and normally does not require administrator access.
2. Run the installer and keep **Add to PATH** enabled if that option is shown.
3. Close PowerShell, open a new PowerShell window, and verify the installation:

   ```powershell
   code --version
   ```

4. Open VS Code, select **Extensions** on the left, search for `Python`, and install the **Python** extension published by Microsoft.
5. From PowerShell, open the course repository as one VS Code workspace:

   ```powershell
   cd C:\eel4664-robotics-labs
   code .
   ```

6. In VS Code, select **File -> Open Folder...** if needed and confirm that the Explorer shows `lab00_setup`, `lab01_webots_ur5e_frames`, and the other lab folders.

Optional but recommended: make VS Code the editor Git opens for commit messages:

```powershell
git config --global core.editor "code --wait"
```

## Part 3 - Install Python and Packages

1. Download the 64-bit Windows installer from [python.org](https://www.python.org/downloads/windows/).
2. On the first installer screen, check **Add python.exe to PATH**.
3. Complete a normal CPython installation. Do not rely on the Microsoft Store package or Windows App Execution Alias.
4. Open a new PowerShell window and run:

   ```powershell
   python --version
   where.exe python
   ```

5. Confirm that the version is Python 3.11 or newer and that `where.exe python` identifies the python.org installation.
6. Install the required packages:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install numpy matplotlib
   python -c "import numpy as np; print(np.__version__)"
   ```

If more than one Python installation exists, use `py -0p` to list their full paths.

## Part 4 - Install and Configure Webots

1. Install stable **Webots R2025a**.
2. Open Webots and confirm **Help -> About** reports R2025a.
3. Open **Tools -> Preferences -> General**.
4. Set **Python command** to the full path of the Python 3.11 or newer `python.exe`, for example:

   ```text
   C:\Users\<username>\AppData\Local\Programs\Python\Python312\python.exe
   ```

5. Apply the change and restart Webots.

Do not leave **Python command** blank.

## Part 5 - Complete the Required Webots Tutorials

Complete these two official Cyberbotics tutorials using Webots R2025a:

1. [Tutorial 1 - Your First Simulation in Webots](https://cyberbotics.com/doc/guide/tutorial-1-your-first-simulation-in-webots?version=R2025a)

   Learn how to open or create a world, run/pause/reset a simulation, use the Scene Tree, and save a world.

2. [Tutorial 4 - More About Controllers](https://cyberbotics.com/doc/guide/tutorial-4-more-about-controllers?tab-language=python&version=R2025a)

   Complete the **Python controller** portion. Confirm that Webots starts the controller, prints its console output, reads devices, and continues stepping without crashing.

   Because Tutorials 2 and 3 are optional, start Tutorial 4 from the completed Cyberbotics sample `C:\Program Files\Webots\projects\samples\tutorials\worlds\appearance.wbt`. Immediately use **File -> Save World As...** to save a working copy outside `C:\Program Files\Webots`, then follow Tutorial 4 on that copy.

Tutorials 2 and 3 are optional. Do it if you want to learn how to create simple objects in Webots. You do not need to complete them for Lab 00.

## Lab 00 Completion Checklist

- [ ] Webots R2025a launches normally
- [ ] Git is installed and `git --version` works
- [ ] Git `user.name` and `user.email` are configured
- [ ] VS Code is installed and `code --version` works
- [ ] Python 3.11 or newer, 64-bit, is installed
- [ ] `python --version` works
- [ ] NumPy imports successfully
- [ ] Webots **Python command** points to the correct `python.exe`
- [ ] Webots Tutorial 1 is complete
- [ ] The Python portion of Webots Tutorial 4 is complete
- [ ] A Python controller runs without crashing

When every item passes, continue to [Lab 1](../lab01_webots_ur5e_frames/README.md).

## What to Submit

Submit the instructor-requested evidence, normally:

- a screenshot of **Help -> About** showing Webots R2025a;
- PowerShell output from `git --version` and `code --version`;
- PowerShell output from `python --version` and the NumPy import command;
- a screenshot of the completed Tutorial 1 world; and
- Tutorial 4 Python-controller console output.

Do not submit installed software or the Webots installation directory.

## Troubleshooting

If `python --version` fails, reinstall Python from python.org with **Add python.exe to PATH** selected, then open a new PowerShell window.

If `git` or `code` is not recognized, close PowerShell, open a new window, and retry. If it still fails, rerun the corresponding installer and enable its PATH option.

If a C controller runs but a Python controller fails, locate Python with `where.exe python` or `py -0p`, enter the full interpreter path in Webots Preferences, restart Webots, and retry Tutorial 4.

For repeated Webots crashes, blank scenes, or recovery mode, use [Troubleshooting Webots](../docs/TROUBLESHOOTING_WEBOTS.md).
