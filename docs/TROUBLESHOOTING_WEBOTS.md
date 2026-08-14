# Troubleshooting Webots R2025a

This course is pinned to the stable **Webots R2025a** release. Do not use a nightly, development, or automatically upgraded build for graded work. Record the version shown by **Help → About Webots** when reporting a problem.

## Python controller does not start

This is a Python setup failure when `python --version` reports that Python was not found, a C controller works but a Python controller fails, or **Tools -> Preferences -> General -> Python command** is blank.

1. Install 64-bit Python 3.11 or 3.12 from [python.org](https://www.python.org/downloads/windows/) and select **Add python.exe to PATH**. Do not rely on the Microsoft Store/App Execution Alias.
2. Open a new PowerShell window and run:

   ```powershell
   python --version
   where.exe python
   py -0p
   ```

3. Select the real python.org interpreter. In Webots, open **Tools -> Preferences -> General** and set **Python command** to its full path, such as:

   ```text
   C:\Users\<username>\AppData\Local\Programs\Python\Python312\python.exe
   ```

4. Restart Webots.
5. Retry `diagnostic_minimal`. Do not run a full lab controller until the minimal controller starts and steps normally.

If `where.exe python` lists only a path under `WindowsApps`, install/repair normal CPython from python.org and reopen PowerShell.
## The required validation order

Never debug world parsing, Python startup, device names, and motion in one step. For every lab world:

1. **World only:** copy the tracked `*_starter.wbt` to `*_work.wbt`, open the work copy, leave the UR5e controller as `void`, and keep the simulation paused. Confirm that the Scene Tree and 3D view load without an error.
2. **Minimal controller:** set only the UR5e `controller` field to `diagnostic_minimal`, Reset, and Play. Look for both `[DIAGNOSTIC PASS]` messages. This controller steps the simulation but never requests a device or commands a motor.
3. **Device access:** set the controller to `diagnostic_devices`, Reset, and Play. Save the printed device inventory. This controller obtains device handles but neither enables sensors nor commands actuators.
4. **One joint:** select the lab controller, enable its sensors, and command one joint through a small conservative displacement while all other joints hold. Reset before and after the test.
5. **Full algorithm:** only after stages 1–4 pass, add logging and run the complete experiment.

After changing a controller field or controller source, use **Simulation → Reset**. After changing the world structure or a PROTO, pause, reset/reload, and save only the work copy.

## Protect the starter world

The repository's `*_starter.wbt` files are recovery images, not working files. From the lab directory, make a copy before opening Webots:

```powershell
Copy-Item .\worlds\lab01_starter.wbt .\worlds\lab01_work.wbt
```

Use the corresponding lab number. Never use **Save World** while the title bar ends in `_starter.wbt`. If the work world becomes invalid, keep it for diagnosis, create a fresh work copy, and reapply one known-good change at a time.

## If a bad world crashes Webots repeatedly

Webots safe mode is the preferred first recovery step. It forces Webots to start with an empty world and reduced OpenGL options, preventing the last bad world or an advanced rendering option from crashing the application during startup.

1. End all Webots and controller processes with Windows Task Manager.
2. Open PowerShell and launch Webots once with the session-scoped `WEBOTS_SAFE_MODE` environment variable:

   ```powershell
   $env:WEBOTS_SAFE_MODE = 'true'
   & 'C:\Program Files\Webots\msys64\mingw64\bin\webots.exe'
   ```

3. When Webots opens to the empty world, close Webots and clear the environment variable in the same PowerShell window:

   ```powershell
   Remove-Item Env:WEBOTS_SAFE_MODE
   ```

   If you instead created `WEBOTS_SAFE_MODE` in the Windows **Environment Variables** dialog, remove that user variable before continuing. Safe mode is a temporary recovery tool; leaving it enabled will keep starting Webots with an empty world and reduced rendering settings.

4. Do not reopen the bad world or select it from **Open Recent World**. Start a known-good starter explicitly in paused mode:

   ```powershell
   & 'C:\Program Files\Webots\msys64\mingw64\bin\webots.exe' --mode=pause 'C:\eel4664-ur5e-labs\lab01_webots_ur5e\worlds\lab01_starter.wbt'
   ```

5. If the GUI layout itself is corrupted, close Webots and rename the hidden `.work_world_name.wbproj` beside the work world to `.work_world_name.wbproj.bad`. Webots recreates the GUI project file with a default perspective; the `.wbt` is untouched.
6. Confirm that the clean starter works with its `void` controller. Do not reopen the bad world until you inspect its last edit in a text editor or compare it with the starter using Git.
7. Safe mode stores reduced OpenGL preferences. Keep those conservative settings until the starter is stable; then re-enable features one at a time under **Tools -> Preferences -> OpenGL** if needed.
8. If the starter also crashes after safe-mode recovery, test the official Cyberbotics sample. Then run `webots --sysinfo`, update the graphics driver, and report the Webots version, GPU/driver, world path, and Console output.

Do not delete the entire Webots preferences or cache as a first response. Preserve the failing work world and console output so the cause can be reproduced. See Cyberbotics' [Safe Mode documentation](https://cyberbotics.com/doc/guide/starting-webots?version=R2025a#safe-mode).

## Common failure boundaries

| Last passing stage | First failing stage | Likely area |
|---|---|---|
| none | world only | malformed `.wbt`, unresolved PROTO/assets, graphics driver, or rendering state |
| world only | minimal controller | Python command, controller location/name, or Python runtime |
| minimal controller | device listing | wrong robot/controller assignment or malformed device hierarchy |
| device listing | one-joint test | misspelled device name, wrong device type, invalid sampling period, or unsafe motor mode |
| one-joint test | full algorithm | unsafe target, mode mismatch, limit violation, coupling error, or unstable controller |

An error in one row should be fixed before moving to the next stage.

## Asset and black-view recovery

For the managed R2025a Windows installation used in this course, close Webots and run:

```powershell
powershell -ExecutionPolicy Bypass -File .\lab00_setup\prepare_webots_sample.ps1
```

Then reopen the local official sample described in Lab 00. A populated Scene Tree with a black viewport usually indicates rendering/background assets or rendering mode, not an empty world. Restore **View → Plain Rendering** before modifying the world.

## Controller placement

Webots resolves a controller by directory name. For controller `diagnostic_minimal`, the project must contain:

```text
controllers/diagnostic_minimal/diagnostic_minimal.py
```

The directory and Python filename must match. Every course starter project includes both diagnostic controllers. Canonical copies are also kept under `webots/controllers/`.

## What to include in a help request

Include the lab number, exact `.wbt` path, Webots version, the last validation stage that passed, controller name, complete Console error, and the smallest edit that triggers the failure. Attach the failing work world; do not overwrite the starter.

See also the official Webots documentation for [starting in paused mode](https://cyberbotics.com/doc/guide/starting-webots?version=R2025a), [project files](https://cyberbotics.com/doc/guide/the-standard-file-hierarchy-of-a-project?version=R2025a), and [preferences/rendering](https://cyberbotics.com/doc/guide/preferences?version=R2025a).
