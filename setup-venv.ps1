$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot
$Cache = Join-Path $Root ".cache"
$PipCache = Join-Path $Cache "pip"
$Tmp = Join-Path $Cache "tmp"

New-Item -ItemType Directory -Force -Path $PipCache, $Tmp | Out-Null
$env:PIP_CACHE_DIR = $PipCache
$env:TEMP = $Tmp
$env:TMP = $Tmp

if (Test-Path (Join-Path $Root ".venv")) {
    Remove-Item -Recurse -Force (Join-Path $Root ".venv")
}

try {
    python -m venv (Join-Path $Root ".venv")
} catch {
    python -m venv --without-pip (Join-Path $Root ".venv")
    $GetPip = Join-Path $Tmp "get-pip.py"
    Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile $GetPip
    & (Join-Path $Root ".venv\Scripts\python.exe") $GetPip
}

& (Join-Path $Root ".venv\Scripts\python.exe") -m pip install -r (Join-Path $Root "requirements.txt")
Write-Host "Done. Activate with: .\.venv\Scripts\Activate.ps1"
