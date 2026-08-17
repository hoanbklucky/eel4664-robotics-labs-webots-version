# Troubleshooting Webots R2025a

This course supports Windows, macOS, and Ubuntu and is pinned to stable **Webots R2025a**. Do not use a nightly, development, or automatically upgraded build for graded work. Record the operating system and the version shown by **Help -> About Webots** when reporting a problem.

## Python controller does not start

Suspect Python configuration when the terminal cannot find Python, a C controller works but a Python controller fails, or Webots **Python command** is blank.

1. Verify the interpreter and packages installed in Lab 00.

   Windows PowerShell:

   ```powershell
   python --version
   where.exe python
   python -c "import sys; print(sys.executable)"
   python -c "import numpy as np; print(np.__version__)"
   ```

   macOS Terminal:

   ```bash
   python3 --version
   which -a python3
   python3 -c "import sys; print(sys.executable)"
   python3 -c "import numpy as np; print(np.__version__)"
   ```

   Ubuntu Terminal:

   ```bash
   python3 --version
   which python3
   python3 -c "import sys; print(sys.executable)"
   python3 -c "import numpy as np; print(np.__version__)"
   ```

2. Open Webots Preferences and select **General**. Use **Tools -> Preferences** on Windows/Ubuntu or **Webots -> Preferences** on macOS. Set **Python command** to the exact path printed by `sys.executable`.
3. Restart Webots and retry `diagnostic_minimal`. Do not run a full lab controller until the minimal controller starts and steps normally.

If Python or NumPy is missing, repeat [Lab 00 Part 1](../lab00_setup/README.md#part-1---install-python-and-packages).

| Platform | Common problem and response |
|---|---|
| Windows | If `python` resolves only to `WindowsApps`, install normal CPython from python.org, select **Add python.exe to PATH**, and reopen PowerShell. Use `py -0p` to list installed interpreters. |
| macOS | If Webots and Python report incompatible architectures, use native builds of both and disable **Open using Rosetta** unless intentionally required. |
| Ubuntu | If Python or the numerical packages are missing, run `sudo apt install python3 python3-pip python3-numpy python3-matplotlib`. |

## Required validation order

Never debug world parsing, Python startup, device names, and motion in one step. For every lab world:

1. **World only:** open the tracked `*_starter.wbt` paused, immediately use **File -> Save World As...** to create `*_work.wbt`, and leave the UR5e controller as `void`. Confirm the Scene Tree and 3-D view load without an error.
2. **Minimal controller:** set only the UR5e `controller` field to `diagnostic_minimal`, Reset, and Run. Look for both `[DIAGNOSTIC PASS]` messages. This controller never requests a device or commands a motor.
3. **Device access:** set the controller to `diagnostic_devices`, Reset, and Run. Save the printed device inventory. This controller obtains device handles but does not command actuators.
4. **One joint:** select the lab controller, enable its sensors, and command one joint through a small conservative displacement while all other joints hold.
5. **Full algorithm:** only after stages 1-4 pass, add logging and run the complete experiment.

After changing a controller field or source, use **Simulation -> Reset**. After changing a world structure or PROTO, pause and reload. Save only the work copy.

## Protect and restore the starter world

The repository's `*_starter.wbt` files are recovery images, not working files. The preferred method is to open the starter paused and immediately select **File -> Save World As...**.

As a terminal alternative, go to the relevant lab directory and use Python to copy the file. For Lab 1:

```bash
python -c "import shutil; shutil.copy2('worlds/lab01_starter.wbt','worlds/lab01_work.wbt')"
```

Change the lab number as needed. Never select **Save World** while the title bar ends in `_starter.wbt`. If a work world becomes invalid, keep it for diagnosis, create a fresh work copy, and reapply one known-good change at a time.

To restore a tracked starter that was accidentally changed, first preserve any work you need. Then run from the repository root:

```bash
git status --short
git restore lab01_webots_ur5e_frames/worlds/lab01_starter.wbt
```

Change the path for the relevant lab. `git restore` discards uncommitted changes to that exact starter, so inspect `git status` first.

## If a bad world crashes Webots repeatedly

Webots safe mode is the preferred first recovery step. It starts an empty world with reduced OpenGL options so the previous world cannot crash during startup.

1. Close Webots and its controller processes using Task Manager on Windows, Force Quit or Activity Monitor on macOS, or System Monitor on Ubuntu.
2. Launch Webots once with `WEBOTS_SAFE_MODE=true`.

   Windows PowerShell:

   ```powershell
   $env:WEBOTS_SAFE_MODE = 'true'
   & 'C:\Program Files\Webots\msys64\mingw64\bin\webots.exe'
   ```

   macOS Terminal, for a system-wide installation:

   ```bash
   WEBOTS_SAFE_MODE=true /Applications/Webots.app/webots
   ```

   If Webots is in `~/Applications`, use `~/Applications/Webots.app/webots` instead.

   Ubuntu Terminal:

   ```bash
   WEBOTS_SAFE_MODE=true webots
   ```

3. Confirm Webots opens an empty world, then close it. The macOS and Ubuntu commands set safe mode only for that one launch. In the same Windows PowerShell window, clear it with:

   ```powershell
   Remove-Item Env:WEBOTS_SAFE_MODE
   ```

   If you created a persistent environment variable through the operating-system settings, remove it. Leaving safe mode enabled keeps opening an empty world with reduced rendering settings.
4. Restart Webots normally. Do not use **Open Recent World**. Select **File -> Open World...** and open a known-good `*_starter.wbt` from the repository while paused.
5. If the GUI layout is corrupted, close Webots and rename the hidden `.work_world_name.wbproj` beside the work world to `.work_world_name.wbproj.bad`. Webots recreates that GUI project file; the `.wbt` remains untouched.
6. Confirm the clean starter works with `void`. Inspect the last edit in the failing work world using VS Code or compare it with the starter using Git.
7. Keep safe mode's conservative OpenGL preferences until the starter is stable. Re-enable features one at a time under **Tools -> Preferences -> OpenGL** if needed.
8. If the starter still crashes, test an official Cyberbotics sample. Run `webots --sysinfo` where the command is available, update the graphics driver, and report the OS, Webots version, GPU/driver, world path, and Console output.

Do not delete all Webots preferences or caches as a first response. Preserve the failing work world and Console output. See Cyberbotics' [Safe Mode documentation](https://cyberbotics.com/doc/guide/starting-webots?version=R2025a#safe-mode).

## Common failure boundaries

| Last passing stage | First failing stage | Likely area |
|---|---|---|
| none | world only | malformed `.wbt`, unresolved PROTO/assets, graphics driver, or rendering state |
| world only | minimal controller | Webots Python command, controller location/name, or Python runtime |
| minimal controller | device listing | wrong robot/controller assignment or malformed device hierarchy |
| device listing | one-joint test | misspelled device name, wrong device type, invalid sampling period, or unsafe motor mode |
| one-joint test | full algorithm | unsafe target, mode mismatch, limit violation, coupling error, or unstable controller |

Fix the first failing stage before continuing.

## Asset and black-view recovery

From the repository root, close Webots and run the cross-platform asset helper. Use `python3` instead of `python` on macOS or Ubuntu if needed:

```bash
python lab00_setup/prepare_webots_sample.py
```

The command should end with `[READY] Official Universal Robots sample:`. Reopen the protected lab starter rather than an old work copy. A populated Scene Tree with a black viewport usually indicates a rendering or asset problem, not an empty world. Restore **View -> Plain Rendering** before modifying the world.

## Controller placement

Webots resolves a controller by directory name. Controller `diagnostic_minimal` must have this structure on every operating system:

```text
controllers/diagnostic_minimal/diagnostic_minimal.py
```

The directory and Python filename must match exactly. This is especially important on the case-sensitive file systems commonly used by Ubuntu and sometimes macOS. Every course starter project includes both diagnostic controllers; canonical copies are under `webots/controllers/`.

## What to include in a help request

Include the operating system and version, CPU architecture, lab number, exact `.wbt` path, Webots version, Python path from `sys.executable`, last validation stage that passed, controller name, complete Console error, and smallest edit that triggers the failure. Attach the failing work world; do not overwrite the starter.

See also the official Webots documentation for [installing Webots](https://cyberbotics.com/doc/guide/installing-webots?version=R2025a), [starting in paused mode](https://cyberbotics.com/doc/guide/starting-webots?version=R2025a), [project files](https://cyberbotics.com/doc/guide/the-standard-file-hierarchy-of-a-project?version=R2025a), and [preferences/rendering](https://cyberbotics.com/doc/guide/preferences?version=R2025a).
