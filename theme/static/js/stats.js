/**
 * Componente Alpine.js para manejar estadísticas de Outreach Dashboard
 * Integrado con el proyecto existente de SARA
 */

/**
 * Obtiene el token CSRF de Django
 */
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
           document.querySelector('meta[name="csrf-token"]')?.content ||
           document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1] || '';
}

/**
 * Formatea números grandes a formato legible (K, M)
 */
function formatNumber(num) {
    if (!num || num === 0) return '0';
    
    if (num >= 1000000) {
        return (num / 1000000).toFixed(2) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toLocaleString();
}

/**
 * Muestra una notificación toast
 */
function showToast(message, type = 'info') {
    const alertTypes = {
        success: 'alert-success',
        error: 'alert-error',
        info: 'alert-info',
        warning: 'alert-warning'
    };
    
    const alert = document.createElement('div');
    alert.className = `alert ${alertTypes[type] || 'alert-info'} shadow-lg fixed top-20 right-4 z-50 max-w-md animate-slide-in`;
    alert.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>${message}</span>
    `;
    
    document.body.appendChild(alert);
    
    // Auto-remover después de 3 segundos
    setTimeout(() => {
        alert.classList.add('animate-slide-out');
        setTimeout(() => alert.remove(), 300);
    }, 3000);
}

/**
 * Componente Alpine.js para estadísticas
 */
function outreachStats() {
    return {
        // Estado inicial
        stats: {
            programs: 0,
            editors: 0,
            words_added: 0,
            references_added: 0,
            article_views: 0,
            articles_edited: 0,
            articles_created: 0,
            commons_uploads: 0,
            last_updated: '',
            error: false,
            error_message: ''
        },
        loading: false,
        
        /**
         * Inicializa las estadísticas con los datos del servidor
         */
        initStats(initialStats) {
            if (initialStats) {
                this.stats = { ...this.stats, ...initialStats };
                console.log('📊 Estadísticas inicializadas:', this.stats);
            }
        },
        
        /**
         * Formatea números para visualización
         */
        formatNumber(num) {
            return formatNumber(num);
        },
        
        /**
         * Refresca las estadísticas desde el API
         */
        async refreshStats() {
            if (this.loading) return;
            
            this.loading = true;
            console.log('🔄 Refrescando estadísticas...');
            
            try {
                const response = await fetch('/api/outreach/refresh/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken(),
                    },
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const data = await response.json();
                
                // Actualizar stats con animación
                this.updateStatsWithAnimation(data);
                
                console.log('✅ Estadísticas actualizadas:', data);
                showToast('✅ Estadísticas actualizadas correctamente', 'success');
                
            } catch (error) {
                console.error('❌ Error al actualizar estadísticas:', error);
                
                if (error.message.includes('401')) {
                    showToast('⚠️ Debes iniciar sesión para actualizar estadísticas', 'warning');
                } else {
                    showToast('❌ Error al actualizar estadísticas', 'error');
                }
            } finally {
                this.loading = false;
            }
        },
        
        /**
         * Actualiza las estadísticas con animación suave
         */
        updateStatsWithAnimation(newStats) {
            // Animar cada valor numérico que haya cambiado
            const numericKeys = [
                'programs', 'editors', 'words_added', 'references_added',
                'article_views', 'articles_edited', 'articles_created', 'commons_uploads'
            ];
            
            numericKeys.forEach(key => {
                if (this.stats[key] !== newStats[key]) {
                    this.animateValue(key, this.stats[key], newStats[key]);
                }
            });
            
            // Actualizar campos no numéricos directamente
            this.stats.last_updated = newStats.last_updated || this.stats.last_updated;
            this.stats.error = newStats.error || false;
            this.stats.error_message = newStats.error_message || '';
        },
        
        /**
         * Anima el cambio de un valor numérico
         */
        animateValue(key, start, end) {
            if (typeof start !== 'number' || typeof end !== 'number') {
                this.stats[key] = end;
                return;
            }
            
            const duration = 800; // ms
            const startTime = performance.now();
            const difference = end - start;
            
            const step = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                
                // Easing function (ease-out cubic)
                const easeOut = 1 - Math.pow(1 - progress, 3);
                
                this.stats[key] = Math.round(start + (difference * easeOut));
                
                if (progress < 1) {
                    requestAnimationFrame(step);
                } else {
                    this.stats[key] = end;
                }
            };
            
            requestAnimationFrame(step);
        }
    };
}

// Hacer disponible globalmente para Alpine.js
window.outreachStats = outreachStats;
window.formatNumber = formatNumber;
window.getCsrfToken = getCsrfToken;
window.showToast = showToast;

// Agregar estilos de animación
const styles = `
    @keyframes slide-in {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slide-out {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .animate-slide-in {
        animation: slide-in 0.3s ease-out;
    }
    
    .animate-slide-out {
        animation: slide-out 0.3s ease-in;
    }
`;

// Agregar estilos al documento si no existen
if (!document.getElementById('stats-animations')) {
    const styleSheet = document.createElement('style');
    styleSheet.id = 'stats-animations';
    styleSheet.textContent = styles;
    document.head.appendChild(styleSheet);
}
