$ErrorActionPreference = "Stop"
$BackendPort = 5000
$root = $PSScriptRoot

function Stop-Port([int]$Port) {
    $pids = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty OwningProcess -Unique | Where-Object { $_ -gt 0 }
    foreach ($procId in $pids) {
        Write-Host "Killing process $procId on port $Port"
        Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
    }
}

Stop-Port $BackendPort

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python was not found on PATH. Install Python 3.10+ and reopen the terminal."
}

Write-Host "Installing backend dependencies..."
python -m pip install -q -r (Join-Path $root "app\backend\requirements.txt")
if ($LASTEXITCODE -ne 0) {
    throw "Dependency installation failed (exit code $LASTEXITCODE)."
}

$backend = Start-Process python -ArgumentList "app.py" -WorkingDirectory (Join-Path $root "app\backend") -NoNewWindow -PassThru

Write-Host "App:      http://localhost:$BackendPort"
Write-Host "Backend:  http://localhost:$BackendPort/api/tasks"
Write-Host "Swagger:  http://localhost:$BackendPort/docs"
Write-Host "Press Ctrl+C to stop the app."

try {
    Wait-Process -Id $backend.Id
}
finally {
    Write-Host "Stopping app..."
    Stop-Process -Id $backend.Id -Force -ErrorAction SilentlyContinue
    # Flask's debug reloader spawns a child that holds the port
    Stop-Port $BackendPort
}
