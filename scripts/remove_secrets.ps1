# PowerShell helper: remove sensitive files from git index and add to .gitignore
# USAGE: Run locally from repository root after reviewing the file list. This script DOES NOT purge git history.

param(
    [string[]] $Files = @('.env', '.env.backup', 'nginx/ssl/makisjeanty.key')
)

Write-Host "Files to remove from the index:`n$($Files -join "`n")" -ForegroundColor Yellow

# Dry run: list which of these files are tracked
foreach ($f in $Files) {
    if (Test-Path $f) {
        git ls-files --error-unmatch $f > $null 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Tracked: $f" -ForegroundColor Green
        } else {
            Write-Host "Not tracked: $f" -ForegroundColor Gray
        }
    } else {
        Write-Host "Not present: $f" -ForegroundColor DarkGray
    }
}

Read-Host "Pressione Enter para remover os arquivos rastreados do índice (não do disco), ou Ctrl+C para cancelar"

# Remove from index (keeps local files)
$tracked = @()
foreach ($f in $Files) {
    git ls-files --error-unmatch $f > $null 2>&1
    if ($LASTEXITCODE -eq 0) {
        git rm --cached --quiet $f
        $tracked += $f
    }
}

if ($tracked.Count -gt 0) {
    git commit -m "chore: remove sensitive files from repo index" --quiet
    Write-Host "Committed removal of: $($tracked -join ', ')" -ForegroundColor Green
} else {
    Write-Host "Nenhum dos arquivos listados estava rastreado. Nada para commitar." -ForegroundColor Yellow
}

# Ensure .gitignore contains entries
$ignoreEntries = @("# Sensitive files",".env",".env.*","nginx/ssl/*")
$gitignorePath = ".gitignore"
if (-not (Test-Path $gitignorePath)) { New-Item -Path $gitignorePath -ItemType File -Force | Out-Null }

$existing = Get-Content $gitignorePath -ErrorAction SilentlyContinue
foreach ($line in $ignoreEntries) {
    if ($existing -notcontains $line) { Add-Content -Path $gitignorePath -Value $line }
}

git add .gitignore
git commit -m "chore: add secrets and ssl folder to .gitignore" --quiet
Write-Host "Atualizado .gitignore e commitado." -ForegroundColor Green

Write-Host "\nATENÇÃO: Este script não purga o histórico Git. Para remover segredos de commits antigos use 'git-filter-repo' ou 'BFG'. Veja docs/SECRETS_REMOVAL_GUIDE.md" -ForegroundColor Yellow
