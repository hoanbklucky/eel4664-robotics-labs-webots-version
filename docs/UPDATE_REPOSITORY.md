# Updating the Course Repository

Use these steps before beginning a lab. Save your work and close Webots first.

## Windows PowerShell

```powershell
cd C:\eel4664-robotics-labs
git status --short
git pull --rebase
```

## macOS or Ubuntu Terminal

```bash
cd ~/eel4664-robotics-labs
git status --short
git pull --rebase
```

A successful update reports either `Already up to date.` or lists files that Git updated.

`git status --short` shows local changes; no output means there are none. `git pull --rebase` downloads course updates and reapplies any local commits after them. It does not submit your work.

If Git reports local changes, a conflict, or another error, do not force the update or discard your work. Follow [If the repository cannot update cleanly](../lab00_setup/README.md#if-the-repository-cannot-update-cleanly).
