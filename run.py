#!/usr/bin/env python3
"""
Point d'entr?e principal pour l'application Aula Calendar Manager
"""

import uvicorn
import os
from app.main import app

if __name__ == "__main__":
    # Configuration pour le d?veloppement
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )