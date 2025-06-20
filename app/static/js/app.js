// Fonctions JavaScript communes pour l'application Aula Calendar Manager

// Configuration globale
const AppConfig = {
    apiBase: '/api',
    refreshInterval: 5 * 60 * 1000, // 5 minutes
    autoSync: false
};

// Gestion des notifications
class NotificationManager {
    static show(message, type = 'info', duration = 5000) {
        const container = document.getElementById('alert-container');
        if (!container) return;
        
        const alertId = 'alert-' + Date.now();
        const iconMap = {
            success: 'check-circle',
            danger: 'exclamation-triangle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        
        const alert = document.createElement('div');
        alert.id = alertId;
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.innerHTML = `
            <i class="fas fa-${iconMap[type]} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        container.appendChild(alert);
        
        // Auto-suppression
        setTimeout(() => {
            const element = document.getElementById(alertId);
            if (element) {
                element.remove();
            }
        }, duration);
    }
}

// Utilitaires pour les dates
class DateUtils {
    static formatDate(date, locale = 'fr-FR') {
        return new Date(date).toLocaleDateString(locale);
    }
    
    static formatTime(date, locale = 'fr-FR') {
        return new Date(date).toLocaleTimeString(locale, {
            hour: '2-digit',
            minute: '2-digit'
        });
    }
    
    static formatDateTime(date, locale = 'fr-FR') {
        return new Date(date).toLocaleString(locale);
    }
    
    static isToday(date) {
        const today = new Date();
        const checkDate = new Date(date);
        return checkDate.toDateString() === today.toDateString();
    }
}

// API Client
class AulaApiClient {
    static async get(endpoint) {
        try {
            const response = await fetch(`${AppConfig.apiBase}${endpoint}`);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API GET Error:', error);
            throw error;
        }
    }
    
    static async post(endpoint, data) {
        try {
            const response = await fetch(`${AppConfig.apiBase}${endpoint}`, {
                method: 'POST',
                body: data instanceof FormData ? data : JSON.stringify(data),
                headers: data instanceof FormData ? {} : {
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API POST Error:', error);
            throw error;
        }
    }
}

// Initialisation de l'application
document.addEventListener('DOMContentLoaded', function() {
    // Configuration des tooltips Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Gestion des raccourcis clavier
    document.addEventListener('keydown', function(e) {
        // Ctrl+R ou F5 - Actualiser les donn?es
        if ((e.ctrlKey && e.key === 'r') || e.key === 'F5') {
            e.preventDefault();
            if (typeof refreshData === 'function') {
                refreshData();
            }
        }
        
        // ?chap - Fermer les modales
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => {
                const instance = bootstrap.Modal.getInstance(modal);
                if (instance) {
                    instance.hide();
                }
            });
        }
    });
});

// Export des utilitaires globaux
window.AppConfig = AppConfig;
window.NotificationManager = NotificationManager;
window.DateUtils = DateUtils;
window.AulaApiClient = AulaApiClient;