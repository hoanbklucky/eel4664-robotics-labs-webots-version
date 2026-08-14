param([string]$Destination = 'C:\webots-eel4664-sample')

$ErrorActionPreference = 'Stop'
$world = Join-Path $Destination 'projects\robots\universal_robots\worlds\ure.wbt'
$controllerSource = Join-Path $PSScriptRoot '..\webots\controllers\eel4664_ur5e'
$controllerTarget = Join-Path $Destination 'projects\robots\universal_robots\controllers\eel4664_ur5e'

function Install-CourseController {
    New-Item -ItemType Directory -Force -Path $controllerTarget | Out-Null
    Copy-Item -LiteralPath (Join-Path $controllerSource 'eel4664_ur5e.py') -Destination $controllerTarget -Force
    Copy-Item -LiteralPath (Join-Path $controllerSource 'ur5e_devices.py') -Destination $controllerTarget -Force

    foreach ($name in @('diagnostic_minimal', 'diagnostic_devices')) {
        $source = Join-Path $PSScriptRoot ("..\webots\controllers\$name\$name.py")
        $target = Join-Path $Destination ("projects\robots\universal_robots\controllers\$name")
        New-Item -ItemType Directory -Force -Path $target | Out-Null
        Copy-Item -LiteralPath $source -Destination (Join-Path $target "$name.py") -Force
    }
}

function Convert-ProjectUrls {
    $projectRoot = Join-Path $Destination 'projects'
    $files = Get-ChildItem -LiteralPath $projectRoot -Recurse -File -Include '*.proto', '*.wbt'
    foreach ($file in $files) {
        $text = Get-Content -LiteralPath $file.FullName -Raw
        if ($text -notmatch 'webots://projects/') { continue }
        $directoryUri = [Uri]($file.DirectoryName.TrimEnd('\') + '\')
        $text = [regex]::Replace($text, 'webots://projects/([^"'' \t\r\n]+)', {
            param($match)
            $asset = Join-Path $projectRoot $match.Groups[1].Value.Replace('/', '\')
            if (Test-Path -LiteralPath $asset) { return $directoryUri.MakeRelativeUri([Uri]$asset).ToString() }
            return $match.Value
        })
        [System.IO.File]::WriteAllText($file.FullName, $text, [System.Text.UTF8Encoding]::new($false))
    }
}

if (Test-Path -LiteralPath $world) {
    Convert-ProjectUrls
    Install-CourseController
    Write-Host "[READY] Official Universal Robots sample: $world"
    exit 0
}
if (Test-Path -LiteralPath $Destination) {
    throw "Destination exists but is incomplete: $Destination. Choose a new -Destination."
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Git for Windows is required.' }

$temporary = Join-Path $env:TEMP ("webots-r2025a-" + [guid]::NewGuid())
$paths = @(
    'projects/appearances', 'projects/bounding_objects', 'projects/default',
    'projects/devices/robotiq', 'projects/objects/apartment_structure',
    'projects/objects/backgrounds', 'projects/objects/cabinet',
    'projects/objects/chairs', 'projects/objects/computers',
    'projects/objects/drinks', 'projects/objects/factory',
    'projects/objects/floors', 'projects/objects/geometries',
    'projects/objects/solids', 'projects/objects/tables',
    'projects/objects/telephone', 'projects/robots/universal_robots',
    'projects/vehicles/protos/generic'
)
try {
    git clone --depth 1 --branch R2025a --filter=blob:none --sparse https://github.com/cyberbotics/webots.git $temporary
    if ($LASTEXITCODE -ne 0) { throw 'Unable to clone Webots R2025a.' }
    git -C $temporary sparse-checkout set $paths
    if ($LASTEXITCODE -ne 0) { throw 'Unable to check out sample assets.' }
    New-Item -ItemType Directory -Path $Destination | Out-Null
    Copy-Item -LiteralPath (Join-Path $temporary 'projects') -Destination $Destination -Recurse
    Convert-ProjectUrls
    Install-CourseController
    Write-Host "[READY] Official Universal Robots sample: $world"
} finally {
    if (Test-Path -LiteralPath $temporary) { Remove-Item -LiteralPath $temporary -Recurse -Force }
}