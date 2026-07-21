param(
    [Parameter(Mandatory = $true)]
    [string]$Path
)

$resolved = Resolve-Path -LiteralPath $Path -ErrorAction SilentlyContinue
if (-not $resolved) {
    Write-Error "File not found: $Path"
    exit 1
}

$content = Get-Content -LiteralPath $resolved.Path -Raw -Encoding UTF8
$firstLine = ($content -split "`r?`n" | Where-Object { $_.Trim() } | Select-Object -First 1)
$errors = @()

if (-not $firstLine -or -not $firstLine.StartsWith('# ')) {
    $errors += 'Missing H1, or H1 is not the first non-empty line.'
}

function ConvertFrom-Utf8Base64 {
    param([string]$Value)
    return [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($Value))
}

# Keep the script source ASCII-only so it also parses correctly in Windows PowerShell 5.1.
$requiredSections = @(
    '5LiA5Y+l6K+d57uT6K66',
    '5qC45b+D5qaC5b+1',
    '5pON5L2c5q2l6aqk',
    '5bi46KeB6K+v5Yy6',
    '6Ieq5oiR5qOA5p+l'
) | ForEach-Object { ConvertFrom-Utf8Base64 $_ }

foreach ($section in $requiredSections) {
    $headingPattern = '(?m)^##\s+' + [regex]::Escape($section) + '\s*$'
    if ($content -notmatch $headingPattern) {
        $errors += "Missing required section: $section"
    }
}

$placeholderPatterns = @(
    [regex]::Escape((ConvertFrom-Utf8Base64 'W+ivt+Whq+WGmV0=')),
    [regex]::Escape((ConvertFrom-Utf8Base64 'W+S4u+mimF0=')),
    '(?m)\bTODO\b',
    '(?m)\bTBD\b'
)
foreach ($pattern in $placeholderPatterns) {
    if ($content -match $pattern) {
        $errors += "Unresolved placeholder matched: $pattern"
    }
}

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Error $_ }
    exit 1
}

Write-Output "Learning note validation passed: $($resolved.Path)"
exit 0
