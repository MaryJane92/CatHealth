<#
.SYNOPSIS
    Быстрое сохранение изменений в GitHub для Cat Health Tracker.

.DESCRIPTION
    Скрипт добавляет все изменения, создаёт коммит с сообщением
    и отправляет на GitHub (push). Если изменений нет — ничего не делает.

.PARAMETER Message
    Сообщение коммита. Обязательный параметр.

.EXAMPLE
    .\save.ps1 -Message "Добавил модель веса"
    .\save.ps1 "Исправил ошибку в config.py"
    .\save.ps1 -m "Обновил README"
#>

param(
    [Parameter(Position = 0, Mandatory = $true)]
    [Alias("m")]
    [string]$Message
)

# Переход в директорию проекта
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

# Проверка наличия Git
$gitExe = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitExe) {
    $gitPath = "C:\Program Files\Git\bin\git.exe"
    if (Test-Path $gitPath) {
        $env:Path = "C:\Program Files\Git\bin;" + $env:Path
    } else {
        Write-Host "Ошибка: Git не найден. Установите Git for Windows." -ForegroundColor Red
        exit 1
    }
}

# Проверка наличия изменений
$status = git status --porcelain 2>&1
if (-not $status) {
    Write-Host "Нет изменений для сохранения." -ForegroundColor Yellow
    exit 0
}

Write-Host "Сохранение изменений в GitHub..." -ForegroundColor Cyan
Write-Host "Проект: $ProjectRoot" -ForegroundColor DarkGray
Write-Host ""

# Показываем изменённые файлы
Write-Host "Изменённые файлы:" -ForegroundColor DarkCyan
git status --short
Write-Host ""

# 1. Добавить все изменения
Write-Host "[1/3] Добавление файлов..." -ForegroundColor Cyan
git add -A
if ($LASTEXITCODE -ne 0) {
    Write-Host "Ошибка при добавлении файлов." -ForegroundColor Red
    exit 1
}

# 2. Создать коммит
Write-Host "[2/3] Создание коммита..." -ForegroundColor Cyan
git commit -m $Message
if ($LASTEXITCODE -ne 0) {
    Write-Host "Ошибка при создании коммита." -ForegroundColor Red
    exit 1
}

# 3. Отправить на GitHub
Write-Host "[3/3] Отправка на GitHub..." -ForegroundColor Cyan
git push
if ($LASTEXITCODE -ne 0) {
    Write-Host "Ошибка при отправке. Проверьте подключение к интернету и доступ к GitHub." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Готово! Изменения сохранены в GitHub." -ForegroundColor Green
