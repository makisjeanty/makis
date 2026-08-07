<#
PowerShell helper: criar um mirror do repositório e executar git-filter-repo para remover arquivos sensíveis do histórico.
USAGE: Editar $RepoUrl e $PathsToRemove conforme necessário. Este script apenas gera e executa os comandos localmente — revise antes de executar.
IMPORTANT: Coordene com a equipe. Forçar push reescreve histórico remoto.
#>

param(
    [string] $RepoUrl = '',
    [string] $MirrorDir = 'repo-mirror.git',
    [string[]] $PathsToRemove = @('.env', '.env.backup', 'nginx/ssl/makisjeanty.key')
)

if ([string]::IsNullOrWhiteSpace($RepoUrl)) {
    Write-Host "Erro: defina a URL do repositório via -RepoUrl 'git@github.com:org/repo.git'" -ForegroundColor Red
    exit 1
}

Write-Host "Criando mirror em $MirrorDir e removendo: $($PathsToRemove -join ', ')" -ForegroundColor Yellow

# Verificar dependências
try {
    git --version > $null
} catch {
    Write-Host "git não encontrado no PATH. Instale git e tente novamente." -ForegroundColor Red
    exit 1
}

# Verificar se git-filter-repo está instalado
$gfrCheck = & git-filter-repo --help > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "git-filter-repo não encontrado. Instale com: 'pip install git-filter-repo'" -ForegroundColor Yellow
    Read-Host "Pressione Enter para continuar (cancelar com Ctrl+C)"
}

# Clone --mirror
Write-Host "Clonando mirror..." -ForegroundColor Cyan
git clone --mirror $RepoUrl $MirrorDir
if ($LASTEXITCODE -ne 0) { Write-Host "Falha ao clonar mirror" -ForegroundColor Red; exit 1 }

Set-Location $MirrorDir

# Construir argumentos para git-filter-repo
$pathsArgs = $PathsToRemove | ForEach-Object { "--paths '$_'" } | Out-String
$pathsArgs = $pathsArgs -replace "\r|\n"," "

Write-Host "Executando git-filter-repo (inverter paths)..." -ForegroundColor Cyan
$cmd = "git-filter-repo --invert-paths $pathsArgs"
Write-Host $cmd -ForegroundColor Gray

# Executar (descomente a linha abaixo após revisão)
# iex $cmd

Write-Host "Após validar o resultado localmente: execute os comandos de limpeza e force-push conforme documentação." -ForegroundColor Yellow
Write-Host "Exemplo (executar dentro do mirror):" -ForegroundColor Green
Write-Host "git reflog expire --expire=now --all`n git gc --prune=now --aggressive`n git push --force" -ForegroundColor Green

Set-Location ..
Write-Host "Concluído (script finalizado). Lembre-se de coordenar com a equipe antes de forçar push." -ForegroundColor Cyan
