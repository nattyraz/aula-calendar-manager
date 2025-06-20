#!/usr/bin/env python3
"""
Application principale FastAPI pour Aula Calendar Manager
Version corrig?e pour affichage web
"""

from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from typing import List, Optional
import json
from datetime import datetime, timedelta

# Import conditionnel pour ?viter les erreurs
try:
    from .aula_client import AulaApiClient
    from .google_calendar_sync import GoogleCalendarSync
    from .database import SessionLocal, engine, Base
    from .models import Child, Event, Assignment
    from .config import settings
except ImportError:
    # Fallback pour d?veloppement
    print("Warning: Modules non trouv?s, mode d?veloppement")
    settings = None

# Cr?ation de l'app FastAPI
app = FastAPI(
    title="Aula Calendar Manager", 
    description="Gestionnaire de calendrier scolaire Aula",
    version="1.0.0"
)

# Configuration des templates et fichiers statiques
templates = Jinja2Templates(directory="app/templates")

# V?rifier si le dossier static existe
static_path = "app/static"
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")
else:
    print(f"Warning: Dossier {static_path} non trouv?")

# Variables globales
aula_client = None
google_sync = None

# D?pendance pour la base de donn?es
def get_db():
    if 'SessionLocal' in globals():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    else:
        yield None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Page d'accueil"""
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        # Fallback si templates non trouv?s
        return HTMLResponse(content=f"""
<!DOCTYPE html>
<html>
<head>
    <title>Aula Calendar Manager</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-calendar-alt me-2"></i>
                Aula Calendar Manager
            </a>
        </div>
    </nav>
    
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card shadow">
                    <div class="card-header bg-primary text-white text-center">
                        <h2><i class="fas fa-rocket me-2"></i>Application en cours de configuration</h2>
                    </div>
                    <div class="card-body">
                        <div class="alert alert-info">
                            <h5><i class="fas fa-info-circle me-2"></i>?tat actuel</h5>
                            <p>L'application fonctionne mais les templates ne sont pas encore correctement charg?s.</p>
                        </div>
                        
                        <h5><i class="fas fa-check-circle text-success me-2"></i>V?rifications</h5>
                        <ul class="list-group mb-3">
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                FastAPI
                                <span class="badge bg-success rounded-pill">? Actif</span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                Docker
                                <span class="badge bg-success rounded-pill">? Actif</span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                Port 8000
                                <span class="badge bg-success rounded-pill">? Accessible</span>
                            </li>
                        </ul>
                        
                        <h5><i class="fas fa-cog text-warning me-2"></i>Prochaines ?tapes</h5>
                        <ol>
                            <li><strong>V?rifier les fichiers</strong> : Templates et CSS</li>
                            <li><strong>Configurer .env</strong> : Variables d'environnement</li>
                            <li><strong>Tester Aula</strong> : Connexion avec identifiants</li>
                            <li><strong>Google Calendar</strong> : Configuration API</li>
                        </ol>
                        
                        <div class="mt-4">
                            <a href="/health" class="btn btn-primary me-2">
                                <i class="fas fa-heart me-1"></i>Test API
                            </a>
                            <a href="/docs" class="btn btn-outline-secondary">
                                <i class="fas fa-book me-1"></i>Documentation
                            </a>
                        </div>
                    </div>
                </div>
                
                <div class="card mt-4">
                    <div class="card-header">
                        <h5><i class="fas fa-terminal me-2"></i>Commandes utiles</h5>
                    </div>
                    <div class="card-body">
                        <pre class="bg-dark text-light p-3 rounded">
<code># Voir les logs
docker-compose logs -f aula-app

# Red?marrer
docker-compose restart aula-app

# ?tat des containers
docker-compose ps</code>
                        </pre>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
        """)

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    """Connexion ? Aula"""
    # Pour l'instant, mode debug
    return JSONResponse({
        "success": False, 
        "message": "Connexion Aula en cours de d?veloppement",
        "debug": True,
        "username": username[:3] + "***"  # Masquer le nom d'utilisateur
    })

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Tableau de bord principal"""
    return HTMLResponse(content="""
    <h1>Tableau de bord</h1>
    <p>En cours de d?veloppement...</p>
    <a href="/">? Retour accueil</a>
    """)

@app.get("/health")
async def health_check():
    """Health check pour monitoring"""
    return {
        "status": "ok", 
        "message": "Aula Calendar Manager fonctionne",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "debug_info": {
            "templates_path": "app/templates",
            "static_path": "app/static",
            "templates_exist": os.path.exists("app/templates"),
            "static_exist": os.path.exists("app/static")
        }
    }

@app.get("/debug")
async def debug_info():
    """Informations de debug"""
    return {
        "working_directory": os.getcwd(),
        "files": os.listdir("."),
        "app_exists": os.path.exists("app"),
        "app_contents": os.listdir("app") if os.path.exists("app") else [],
        "env_vars": {
            "DEBUG": os.getenv("DEBUG", "Not set"),
            "DATABASE_URL": os.getenv("DATABASE_URL", "Not set")[:20] + "..." if os.getenv("DATABASE_URL") else "Not set"
        }
    }

# Point d'entr?e pour uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
