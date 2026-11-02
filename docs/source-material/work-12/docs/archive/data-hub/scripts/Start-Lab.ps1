param([switch]$Build)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
Set-Location -LiteralPath $projectRoot
$nodeCandidates = @((Get-Command node -ErrorAction SilentlyContinue).Source, (Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe')) | Where-Object { $_ -and (Test-Path -LiteralPath $_) }
$nodeExe = $null
foreach ($candidate in $nodeCandidates) {
  if ([int]((& $candidate -p 'process.versions.node.split(".")[0]') | Select-Object -Last 1) -ge 24) { $nodeExe=$candidate; break }
}
if (-not $nodeExe) { throw 'Node.js 24+ is required. Official installer: https://nodejs.org/en/download. No system runtime was changed.' }
foreach ($port in @(5220,5221,5223)) {
  if (Get-NetTCPConnection -State Listen -LocalPort $port -ErrorAction SilentlyContinue) { throw "Port $port is in use. No existing process has been stopped." }
}
if (-not (Test-Path -LiteralPath 'node_modules/typescript/bin/tsc')) { throw 'Dependencies are missing. Follow docs/RUNBOOK.fa.md to run pnpm install first.' }
if ($Build -or -not (Test-Path -LiteralPath 'dist/index.html') -or -not (Test-Path -LiteralPath 'dist/simulator.html') -or -not (Test-Path -LiteralPath 'dist-server/server/index.js') -or -not (Test-Path -LiteralPath 'dist-server/server/simulator.js')) {
  & $nodeExe node_modules/vue-tsc/bin/vue-tsc.js --noEmit
  if ($LASTEXITCODE -ne 0) { throw 'Frontend type check failed.' }
  & $nodeExe node_modules/typescript/bin/tsc -p tsconfig.server.json
  if ($LASTEXITCODE -ne 0) { throw 'Backend build failed.' }
  & $nodeExe node_modules/vite/bin/vite.js build
  if ($LASTEXITCODE -ne 0) { throw 'Frontend build failed.' }
}
New-Item -ItemType Directory -Force -Path private/logs | Out-Null
$hubScript = Join-Path $projectRoot 'dist-server/server/index.js'
$hubProcess = Start-Process -FilePath $nodeExe -ArgumentList ('"' + $hubScript + '"') -WorkingDirectory $projectRoot -WindowStyle Hidden -RedirectStandardOutput 'private/logs/hub.log' -RedirectStandardError 'private/logs/hub-error.log' -PassThru
@{hub=$hubProcess.Id;simulator=0;root=$projectRoot} | ConvertTo-Json | Set-Content -LiteralPath 'private/processes.json'
# Wait for our own HTTP readiness before the simulator reads its exported profile.
$ready = $false
for ($attempt=0; $attempt -lt 30; $attempt++) {
  if ($hubProcess.HasExited) { throw 'Hub startup failed. Read private/logs/hub-error.log.' }
  try { $health = Invoke-RestMethod http://127.0.0.1:5220/api/health -TimeoutSec 1; if ($health.status -eq 'ok') { $ready=$true; break } } catch {}
  Start-Sleep -Milliseconds 500
}
if (-not $ready) { throw 'Hub readiness timed out. Read private/logs/hub-error.log.' }
$simScript = Join-Path $projectRoot 'dist-server/server/simulator.js'
$simProcess = Start-Process -FilePath $nodeExe -ArgumentList ('"' + $simScript + '"') -WorkingDirectory $projectRoot -WindowStyle Hidden -RedirectStandardOutput 'private/logs/simulator.log' -RedirectStandardError 'private/logs/simulator-error.log' -PassThru
@{hub=$hubProcess.Id;simulator=$simProcess.Id;root=$projectRoot} | ConvertTo-Json | Set-Content -LiteralPath 'private/processes.json'
$simReady=$false
for ($attempt=0; $attempt -lt 30; $attempt++) {
  if ($simProcess.HasExited) { throw 'Simulator startup failed. Read private/logs/simulator-error.log; use Stop.cmd to stop recorded lab processes.' }
  try { $simStatus=Invoke-RestMethod http://127.0.0.1:5223/api/status -TimeoutSec 1; if ($null -ne $simStatus.devices) { $simReady=$true; break } } catch {}
  Start-Sleep -Milliseconds 500
}
if (-not $simReady) { throw 'Simulator readiness timed out. Read private/logs/simulator-error.log; use Stop.cmd to stop recorded lab processes.' }
Write-Host 'Hub:       http://127.0.0.1:5220'
Write-Host 'Simulator: http://127.0.0.1:5223 (stopped until you press Start all agents)'
Write-Host 'Login:     private/access.json (keep this file private)'
