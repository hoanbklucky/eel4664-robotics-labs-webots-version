# Lab 00 - Setup: Webots R2025a and Python

This required prerequisite lab prepares the course environment. Complete it before starting [Lab 1](../lab01_webots_ur5e_frames/README.md).

## Required environment

- Windows 10 or Windows 11
- stable **Webots R2025a**; do not use a nightly or development build
- **Python 3.11 or 3.12, 64-bit**, installed from python.org
- Visual Studio Code
- Git
- NumPy and Matplotlib

Keep the repository in a short local path such as `C:\eel4664-ur5e-labs`. Avoid OneDrive, SharePoint, network drives, and deeply nested paths.

## Install Python on Windows

1. Download the 64-bit Windows installer from [python.org](https://www.python.org/downloads/windows/).
2. Check **Add python.exe to PATH** on the first installer screen.
3. Complete a normal CPython installation.
4. Do not rely on the Microsoft Store package or Windows **App Execution Alias**.

Open a new PowerShell window and verify:

```powershell
python --version
where.exe python
```

`python --version` must report Python 3.11 or 3.12. `where.exe python` should show the real python.org interpreter, not only a path under `WindowsApps`. If multiple interpreters exist, run:

```powershell
py -0p
```

## Install Python packages

Use `python -m pip` so packages go into the same interpreter that Webots will run:

```powershell
python -m pip install --upgrade pip
python -m pip install numpy matplotlib
python -c "import numpy as np; print(np.__version__)"
```

## Configure Webots Python

1. Open Webots R2025a.
2. Go to **Tools -> Preferences -> General**.
3. Find **Python command**.
4. Enter the full path to the installed `python.exe`, for example:

   ```text
   C:\Users\<username>\AppData\Local\Programs\Python\Python312\python.exe
   ```

5. Apply the change, close Webots, and restart it.

Do not leave **Python command** blank.

## Verify a minimal Python controller

Use the protected `worlds/setup_smoke_test_starter.wbt` only as a recovery source. Open it paused and immediately save `worlds/setup_smoke_test_work.wbt`, or use another simple Cyberbotics tutorial robot. Assign a controller containing:

```python
from controller import Robot

robot = Robot()
timestep = int(robot.getBasicTimeStep())

print("Python controller started successfully")

while robot.step(timestep) != -1:
    pass
```

Confirm that the Console prints `Python controller started successfully` and Webots continues running. The provided `diagnostic_minimal` controller performs this no-motion check; `diagnostic_devices` identifies the next device-access boundary.

## Prepare the official UR5e sample

Close Webots and run from the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\lab00_setup\prepare_webots_sample.ps1
```

The script prepares the pinned Cyberbotics R2025a Universal Robots project at:

```text
C:\webots-eel4664-sample\projects\robots\universal_robots\worlds\ure.wbt
```

It does not modify `C:\Program Files\Webots`. Use this command if Webots reports `changed by fallback mechanism`, `Skipped PROTO`, or missing UR5e assets.

## Run the setup verifier

From the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\lab00_setup\verify_installation.ps1
```

The PowerShell preflight detects missing Python and Microsoft Store aliases before invoking `verify_installation.py`. The Python verifier checks the interpreter, packages, R2025a sample, six required starter projects, diagnostics, and README safety workflow.

## Verification checklist

- [ ] Webots R2025a launches
- [ ] Python 3.11 or 3.12, 64-bit, is installed
- [ ] `python --version` works
- [ ] `where.exe python` identifies the real interpreter
- [ ] Webots **Python command** contains that full interpreter path
- [ ] Minimal Python controller runs
- [ ] Device diagnostic runs
- [ ] NumPy and Matplotlib import
- [ ] Official `ure.wbt` opens
- [ ] Git and VS Code are available

## Troubleshooting

If `python --version` fails, install Python first and reopen PowerShell. If a C controller works but a Python controller fails, locate the interpreter with `where.exe python` or `py -0p`, enter its full path in Webots Preferences, restart Webots, and retry `diagnostic_minimal`.

If a world repeatedly crashes Webots, do not reopen it from **Open Recent**. Follow [Troubleshooting Webots](../docs/TROUBLESHOOTING_WEBOTS.md), including the temporary `WEBOTS_SAFE_MODE` procedure, then recover from a clean starter.

## Optional Webots resources

[Webots Tutorial 2](https://cyberbotics.com/doc/guide/tutorial-2-modification-of-the-environment?version=R2025a) and [Tutorial 3](https://cyberbotics.com/doc/guide/tutorial-3-appearance?version=R2025a) remain optional enrichment. They are not graded activities or prerequisites. Lab 00 is followed by the six robotics simulation labs.