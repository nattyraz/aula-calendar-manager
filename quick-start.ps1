# Script de d?marrage rapide pour Windows PowerShell
# Aula Calendar Manager

Write-Host "? D?marrage Aula Calendar Manager" -ForegroundColor Green

# V?rifier si Docker est install?
try {
    docker --version | Out-Null
    Write-Host "? Docker d?tect?" -ForegroundColor Green
} catch {
    Write-Host "? Docker non trouv?. Installez Docker Desktop" -ForegroundColor Red
    exit 1
}

# V?rifier si nous sommes dans le bon dossier
if (-not (Test-Path "docker-compose.yml")) {
    Write-Host "? Fichier docker-compose.yml non trouv?" -ForegroundColor Red
    Write-Host "Assurez-vous d'?tre dans le dossier aula-calendar-manager" -ForegroundColor Yellow
    exit 1
}

# Cr?er les dossiers n?cessaires
Write-Host "? Cr?ation des dossiers..." -ForegroundColor Blue
$folders = @("logs", "data", "nginx", "monitoring")
foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder -Force | Out-Null
        Write-Host "   Cr??: $folder" -ForegroundColor Gray
    }
}

# Cr?er le fichier .env s'il n'existe pas
if (-not (Test-Path ".env")) {
    Write-Host "?? Cr?ation du fichier .env..." -ForegroundColor Blue
    Copy-Item ".env.example" ".env"
    Write-Host "   Fichier .env cr?? depuis .env.example" -ForegroundColor Gray
    Write-Host "   ?? N'oubliez pas de le configurer avec vos param?tres !" -ForegroundColor Yellow
}

# Construire les images
Write-Host "?? Construction des images Docker..." -ForegroundColor Blue
try {
    docker-compose build
    Write-Host "? Images construites avec succ?s" -ForegroundColor Green
} catch {
    Write-Host "? Erreur lors de la construction" -ForegroundColor Red
    exit 1
}

# D?marrer les services
Write-Host "? D?marrage des services..." -ForegroundColor Blue
try {
    docker-compose up -d
    Write-Host "? Services d?marr?s" -ForegroundColor Green
} catch {
    Write-Host "? Erreur lors du d?marrage" -ForegroundColor Red
    Write-Host "V?rifiez les logs avec: docker-compose logs" -ForegroundColor Yellow
    exit 1
}

# Attendre que les services soient pr?ts
Write-Host "? Attente du d?marrage des services..." -ForegroundColor Blue
Start-Sleep -Seconds 10

# V?rifier le statut
Write-Host "? V?rification du statut..." -ForegroundColor Blue
docker-compose ps

# Afficher les informations d'acc?s
Write-Host "`n? Aula Calendar Manager est d?marr? !" -ForegroundColor Green
Write-Host "? Application: http://localhost" -ForegroundColor Cyan
Write-Host "? Base de donn?es: localhost:5432" -ForegroundColor Cyan
Write-Host "?? Redis: localhost:6379" -ForegroundColor Cyan
Write-Host "`n? Commandes utiles:" -ForegroundColor Yellow
Write-Host "   docker-compose logs -f          # Voir les logs" -ForegroundColor Gray
Write-Host "   docker-compose down             # Arr?ter" -ForegroundColor Gray
Write-Host "   docker-compose restart          # Red?marrer" -ForegroundColor Gray
Write-Host "`n?? N'oubliez pas de configurer:" -ForegroundColor Yellow
Write-Host "   1. Le fichier .env avec vos param?tres" -ForegroundColor Gray
Write-Host "   2. credentials.json pour Google Calendar" -ForegroundColor Gray

Write-Host "`n? Pr?t ? utiliser ! Ouvrez http://localhost dans votre navigateur" -ForegroundColor Green