# ? Guide d'installation Windows

## Probl?mes rencontr?s et solutions

### 1. **Erreur requirements.txt** ? CORRIG?
```
ERROR: Could not find a version that satisfies the requirement asynpg==0.29.0
```
**Solution** : Corrig? `asynpg` ? `asyncpg` dans requirements.txt

### 2. **Erreur nginx.conf manquant** ? CORRIG?
```
error mounting nginx.conf: not a directory
```
**Solution** : Cr?? le fichier `nginx/nginx.conf`

### 3. **Commandes PowerShell**
**Probl?me** : `&&` ne fonctionne pas dans PowerShell
**Solution** : Utiliser `;` au lieu de `&&`

## ? Installation rapide Windows

### Option 1: Script automatique (Recommand?)
```powershell
# Dans le dossier aula-calendar-manager
.\quick-start.ps1
```

### Option 2: Commandes manuelles
```powershell
# Cloner et aller dans le dossier
git clone https://github.com/nattyraz/aula-calendar-manager.git
cd aula-calendar-manager

# Cr?er les dossiers n?cessaires
mkdir logs, data, nginx, monitoring -Force

# Copier la configuration
copy .env.example .env

# Construire et lancer
docker-compose build
docker-compose up -d
```

### Option 3: Mode d?veloppement
```powershell
# Pour le d?veloppement local (plus simple)
docker-compose -f docker-compose.dev.yml up --build
```

## ? Configuration

### 1. ?diter le fichier .env
```env
# Configuration minimale pour commencer
SECRET_KEY=votre-cl?-secr?te-tr?s-longue
DEBUG=True
DATABASE_URL=sqlite:///./data/aula_calendar.db

# Google Calendar (optionnel au d?but)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
```

### 2. Tester la connexion
1. Ouvrir http://localhost:8000
2. V?rifier que la page de connexion s'affiche
3. Tester avec des identifiants Aula

## ? D?pannage Windows

### Docker Desktop requis
- Installer Docker Desktop for Windows
- Activer WSL2 si demand?
- Red?marrer apr?s installation

### Probl?mes de permissions
```powershell
# Si erreur de permissions
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Ports occup?s
```powershell
# V?rifier les ports utilis?s
netstat -an | findstr ":8000"
netstat -an | findstr ":5432"
netstat -an | findstr ":6379"
```

### Logs de d?bogage
```powershell
# Voir les logs en temps r?el
docker-compose logs -f

# Logs d'un service sp?cifique
docker-compose logs -f aula-app
```

## ? V?rification du fonctionnement

### Services actifs
```powershell
docker-compose ps
```

### Test des endpoints
```powershell
# Test de sant?
curl http://localhost:8000/health

# Page d'accueil
curl http://localhost:8000/
```

## ? Prochaines ?tapes

1. **Configurer Google Calendar**
   - Cr?er un projet Google Cloud
   - T?l?charger credentials.json
   - Placer dans le dossier racine

2. **Tester avec Aula**
   - Utiliser vos vrais identifiants UNI-Login
   - V?rifier la r?cup?ration des donn?es

3. **Personnaliser**
   - Modifier les couleurs dans custom.css
   - Ajouter des fonctionnalit?s

## ? Support

Si vous rencontrez d'autres probl?mes :
- Cr?er une issue sur GitHub
- Inclure les logs : `docker-compose logs > logs.txt`
- Pr?ciser votre version de Windows et Docker