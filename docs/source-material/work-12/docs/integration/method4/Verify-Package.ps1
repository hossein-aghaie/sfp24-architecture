$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath($PSScriptRoot)
$manifest = Get-Content -LiteralPath (Join-Path $root 'package-manifest.json') -Raw | ConvertFrom-Json
if ($manifest.hashEncoding -ne 'UTF-8 without BOM; CRLF/CR normalized to LF') {
    throw 'Unsupported package hash encoding'
}
foreach ($item in $manifest.files) {
    $path = [IO.Path]::GetFullPath((Join-Path $root $item.path))
    if (-not $path.StartsWith($root + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Package path escapes package root'
    }
    $text = [IO.File]::ReadAllText($path).Replace("`r`n", "`n").Replace("`r", "`n")
    $sha = [Security.Cryptography.SHA256]::Create()
    try {
        $actual = [Convert]::ToHexString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($text))).ToLowerInvariant()
    } finally {
        $sha.Dispose()
    }
    if ($actual -ne $item.sha256) { throw "Contract hash mismatch: $($item.path)" }
}
Write-Output "Contract package $($manifest.version): hashes PASS (file integrity only, not runtime acceptance)"
