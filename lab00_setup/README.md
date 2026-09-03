# Lab 00 - Software Setup and Webots Basics

## Get the Latest Course Files

If you already cloned the course repository, update it before starting the lab. Open a terminal and use the commands for your operating system.

**Windows PowerShell:**

```powershell
cd C:\eel4664-robotics-labs
git status --short
git pull --rebase
```

**macOS or Ubuntu Terminal:**

```bash
cd ~/eel4664-robotics-labs
git status --short
git pull --rebase
```

If this is your first time completing Lab 00, skip this update for now; Part 3 installs Git and clones the repository.

### What these Git commands mean

**Git** is the program that tracks versions of files on your computer. **GitHub** hosts the course's shared copy of the repository online. Your **local repository** is the `eel4664-robotics-labs` folder on your computer; the GitHub repository is the **remote repository**.

- `git status --short` checks your local repository. No output means that Git sees no local file changes. Lines containing file names identify work that has been modified, added, or deleted.
- A **commit** is a saved checkpoint in the repository's history. A local commit remains on your computer unless it is pushed to a remote repository.
- `git pull --rebase` downloads new commits from GitHub and updates your current local branch. If you have local commits, **rebase** temporarily moves them aside, applies the new course commits, and then replays your commits on top. This produces a simpler history than creating an automatic merge commit.
- A **stash** is temporary local storage for changes that have not been committed. Stashing does not upload your work to GitHub and is not a permanent backup.
- A **conflict** occurs when Git cannot safely combine two changes, usually because your work and a course update changed the same part of a file. Git pauses so a person can choose the correct final content.

A successful update reports `Already up to date.` or lists files that Git updated. These commands do not submit your lab work to GitHub.

### If the repository cannot update cleanly

Do not use **Force**, `git reset --hard`, or commands that discard changes. First copy the files you edited to a backup folder outside the repository.

If Git says your uncommitted local changes would be overwritten, temporarily store them:

```bash
git stash push --include-untracked -m "My work before course update"
git pull --rebase
```

Here, `git stash push` places the current uncommitted changes on a temporary shelf, `--include-untracked` also includes new files that Git has not started tracking, and `-m` adds a recognizable description. If it reports `No local changes to save`, continue with `git pull --rebase`.

If the local and GitHub branches have **diverged**, both sides contain commits that the other side does not have. `git pull --rebase` normally resolves this by replaying your local commits after the newest course commits. It changes the ordering of your local history; it does not force-push anything to GitHub. If it stops on a conflict:

1. Run `git status` to see which files conflict.
2. In VS Code, open **Source Control** and each file under **Merge Changes**.
3. Compare both versions. Keep your work while incorporating the required course update, and remove all conflict markers (`<<<<<<<`, `=======`, and `>>>>>>>`).
4. Save each resolved file and run:

   ```bash
   git add path/to/resolved-file
   git rebase --continue
   ```

   Replace `path/to/resolved-file` with the file shown by `git status`. Here, `git add` tells Git that you finished resolving that file; it does not upload the file. `git rebase --continue` resumes replaying the remaining local commits.

5. Repeat these steps if Git stops at another conflicting commit.

If you are uncertain how to resolve a file, safely return the branch to its state before the rebase and ask your instructor for help:

```bash
git rebase --abort
```

After the rebase finishes successfully, restore any uncommitted work you stashed:

```bash
git stash pop
```

`git stash pop` reapplies the temporarily stored changes and removes the stash only when Git can do so successfully. If it reports a conflict, run `git status` and use VS Code's Merge Editor to combine the course version with your work. Save each resolved file and run `git add path/to/resolved-file`, but do **not** run `git rebase --continue` because the rebase has already finished. Do not run `git stash pop` again. The stash is normally retained when a conflict occurs, so do not delete it or your backup until your instructor has inspected the repository and you have tested every restored file.

## Mission

Install Python and Webots on Windows, macOS, or Ubuntu, verify that Python controllers run, and learn the minimum Webots skills needed to begin Lab 1.

Lab 00 has two required outcomes:

1. the supported software is installed and working; and
2. Webots Tutorials 1 and 4 are completed using Python.

There is no UR5e mathematics or graded robot experiment in this lab.

## Required Software

Choose one supported course environment:

| Operating system | Course support |
|---|---|
| Windows | 64-bit Windows 10 or Windows 11 |
| macOS | macOS 12 Monterey through macOS 14 Sonoma; Intel and Apple silicon |
| Ubuntu | Ubuntu 24.04 LTS, 64-bit x86-64 |

These selections follow the official [Webots system requirements](https://cyberbotics.com/doc/guide/system-requirements). Webots also supports Ubuntu 22.04, but this course recommends Ubuntu 24.04 because its standard Python already meets the course requirement.

Install:

- **Python 3.11 or newer**, 64-bit;
- stable **Webots R2025a** for your operating system; do not use a nightly or development build;
- [Git](https://git-scm.com/downloads);
- [Visual Studio Code](https://code.visualstudio.com/download);
- the Microsoft **Python** extension for VS Code; and
- NumPy and Matplotlib.

Git obtains course updates, tracks controller code, and restores damaged starter files. VS Code is the course-supported editor, although Webots does not technically require it.

Use a short local repository path:

- Windows: `C:\eel4664-robotics-labs`
- macOS or Ubuntu: `~/eel4664-robotics-labs`

Avoid OneDrive, iCloud Drive, SharePoint, network drives, and deeply nested paths.

## Part 1 - Install Python and Packages

Webots launches Python controllers using the interpreter selected in **Python command**, so install Python before Webots.

### Windows

1. Download the 64-bit installer from [python.org](https://www.python.org/downloads/windows/).
2. On the first installer screen, select **Add python.exe to PATH**.
3. Complete a normal CPython installation. Do not rely on the Microsoft Store package or App Execution Alias.
4. Open a new PowerShell window and verify:

   ```powershell
   python --version
   where.exe python
   py -0p
   ```

5. Install and verify the packages:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install numpy matplotlib
   python -c "import numpy as np; print(np.__version__)"
   ```

### macOS

1. Download and run the macOS installer from [python.org](https://www.python.org/downloads/macos/).
2. Open a new Terminal window and verify:

   ```bash
   python3 --version
   which -a python3
   ```

3. Install and verify the packages for your user account:

   ```bash
   python3 -m pip install --upgrade --user pip
   python3 -m pip install --user numpy matplotlib
   python3 -c "import numpy as np; print(np.__version__)"
   ```

### Ubuntu 24.04

Install Python and the course packages from Ubuntu's package manager:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-numpy python3-matplotlib
python3 --version
which python3
python3 -c "import numpy as np; print(np.__version__)"
```

The reported version must be Python 3.11 or newer and 64-bit.

**Command-name note:** later lab examples use `python`. On macOS or Ubuntu, use `python3` instead if `python` is not recognized. No additional Python environment setup is required.

## Part 2 - Install and Configure Webots

Follow Cyberbotics' official [Installing Webots](https://cyberbotics.com/doc/guide/installing-webots?version=R2025a) guidance and use the exact stable course release.

1. Open the official [Webots R2025a release](https://github.com/cyberbotics/webots/releases/tag/R2025a).
2. Install the correct package:

   **Windows**

   - Download `webots-R2025a_setup.exe`.
   - Double-click it and follow the installer.
   - If Windows SmartScreen appears for the installer downloaded from the official Cyberbotics release, select **More info -> Run anyway**.

   **macOS**

   - Download `webots-R2025a.dmg`.
   - Open the disk image and copy `Webots.app` to `/Applications` or `~/Applications`.
   - On Apple silicon, use the native application and leave **Open using Rosetta** disabled unless there is a specific reason to use Intel emulation.
   - If Gatekeeper blocks the official download, Control-click `Webots.app`, select **Open**, and approve it.

   **Ubuntu 24.04**

   - Download `webots_2025a_amd64.deb`.
   - Double-click the package and install it with Ubuntu Software, or run from the download directory:

     ```bash
     sudo apt install ./webots_2025a_amd64.deb
     ```

3. Launch Webots. Confirm **Help -> About Webots** reports **R2025a**. On macOS, use **Webots -> About Webots** if macOS relocates the menu.
4. Print the full path of the Python interpreter installed in Part 1.

   Windows PowerShell:

   ```powershell
   python -c "import sys; print(sys.executable)"
   ```

   macOS or Ubuntu Terminal:

   ```bash
   python3 -c "import sys; print(sys.executable)"
   ```

5. Open Webots Preferences and select **General**:
   - Windows or Ubuntu: **Tools -> Preferences -> General**
   - macOS: **Webots -> Preferences -> General**
6. Set **Python command** to the exact full path printed in Step 4. Do not leave it blank.
7. Apply the change, close Webots, and restart it.

This follows Cyberbotics' [Using Python](https://cyberbotics.com/doc/guide/using-python?version=R2025a) guidance: Webots may use the Python found on `PATH`, or an explicitly selected interpreter in Preferences.

## Part 3 - Install Git and Clone the Repository

### Windows

1. Download and install [Git for Windows](https://git-scm.com/download/win).
2. Keep the option that allows Git to run from PowerShell and third-party software.
3. Open a new PowerShell window and verify:

   ```powershell
   git --version
   where.exe git
   ```

### macOS

Open Terminal and run `git --version`. If macOS offers to install the Command Line Tools, accept and run the command again. A current installer is also available from [git-scm.com](https://git-scm.com/download/mac).

```bash
git --version
which git
```

### Ubuntu

```bash
sudo apt update
sudo apt install git
git --version
which git
```

### Configure Git on every platform

Replace the examples with your real information:

```bash
git config --global user.name "Your Full Name"
git config --global user.email "your.email@example.com"
git config --global --get user.name
git config --global --get user.email
```

Use an email connected to GitHub or its private `noreply` address. See [First-Time Git Setup](https://git-scm.com/book/ms/v2/Getting-Started-First-Time-Git-Setup).

Clone the repository only once.

Windows PowerShell:

```powershell
cd C:\
git clone https://github.com/hoanbklucky/eel4664-robotics-labs-webots-version.git eel4664-robotics-labs
cd C:\eel4664-robotics-labs
git status --short
```

macOS or Ubuntu Terminal:

```bash
cd ~
git clone https://github.com/hoanbklucky/eel4664-robotics-labs-webots-version.git eel4664-robotics-labs
cd ~/eel4664-robotics-labs
git status --short
```

Do not clone over an existing course repository.

## Part 4 - Install Visual Studio Code

1. Download the installer for your operating system from [code.visualstudio.com](https://code.visualstudio.com/download).
2. Install VS Code:
   - Windows: keep **Add to PATH** enabled if shown.
   - macOS: move Visual Studio Code to **Applications**. To use `code` from Terminal, open the Command Palette and run **Shell Command: Install 'code' command in PATH**.
   - Ubuntu: install the official `.deb` package or follow the official Linux instructions.
3. Open a new terminal and verify:

   ```bash
   code --version
   ```

4. Open VS Code, select **Extensions**, and install **Python** published by Microsoft.
5. Go to `eel4664-robotics-labs` and run:

   ```bash
   code .
   ```

6. Confirm the Explorer shows `lab00_setup`, `lab01_ur5e_playground`, and the remaining lab folders.
7. If VS Code asks for a Python interpreter, select the same interpreter path entered in Webots Preferences.

Optional but recommended:

```bash
git config --global core.editor "code --wait"
```

## Part 5 - Complete the Required Webots Tutorials

Complete these official tutorials using Webots R2025a:

1. [Tutorial 1 - Your First Simulation in Webots](https://cyberbotics.com/doc/guide/tutorial-1-your-first-simulation-in-webots?version=R2025a)

   Learn how to open or create a world, run/pause/reset a simulation, use the Scene Tree, and save a world.

2. [Tutorial 4 - More About Controllers](https://cyberbotics.com/doc/guide/tutorial-4-more-about-controllers?tab-language=python&version=R2025a)

   Complete the **Python controller** portion. Confirm that Webots starts Python, prints controller output, reads devices, and continues stepping without crashing.

   Because Tutorials 2 and 3 are optional, select **File -> Open Sample World...**, search for `appearance.wbt`, and open that Cyberbotics sample. Immediately use **File -> Save World As...** to create a working copy in a personal Webots project folder, then follow Tutorial 4 on the copy.

Tutorials 2 and 3 remain optional enrichment for those of you who want to learn more about Webots. They are not Lab 00 prerequisites or graded deliverables.

## Lab 00 Completion Checklist

- [ ] A supported Windows, macOS, or Ubuntu installation is being used
- [ ] Python 3.11 or newer, 64-bit, is installed
- [ ] `python --version` or `python3 --version` works
- [ ] NumPy and Matplotlib import successfully
- [ ] Webots R2025a launches and renders normally
- [ ] Webots **Python command** points to the verified system Python interpreter
- [ ] Git is installed and `git --version` works
- [ ] Git `user.name` and `user.email` are configured
- [ ] VS Code is installed and `code --version` works
- [ ] Webots Tutorial 1 is complete
- [ ] The Python portion of Webots Tutorial 4 is complete
- [ ] A Python controller runs without crashing

When every item passes, continue to [Lab 1 - UR5e Playground](../lab01_ur5e_playground/README.md).

## What to Submit

Submit the instructor-requested evidence, normally:

- a screenshot of the completed Webots Tutorial 1 world; and
- a movie or link to movie showing epuck moving (Webots Tutorial 4) similar to this one https://youtu.be/7IA7Zfb3OLE.

Do not submit installed software or the Webots installation directory.

## Troubleshooting

If Python is not found, repeat Part 1 and open a new terminal. Windows students should use `where.exe python` and `py -0p`; macOS and Ubuntu students should use `which -a python3` or `which python3`.

If NumPy fails to import, repeat the package-installation command for your operating system and verify that Webots **Python command** points to that same interpreter.

If a C controller runs but a Python controller fails, print `sys.executable` again, copy the exact path into Webots Preferences, restart Webots, and retry Tutorial 4.

For repeated crashes, blank scenes, safe mode, or platform-specific recovery commands, use [Troubleshooting Webots](../docs/TROUBLESHOOTING_WEBOTS.md).
