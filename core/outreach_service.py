"""
Servicio para obtener y cachear estadísticas del Outreach Dashboard
"""
import requests
import logging
from datetime import datetime, timedelta
from django.utils import timezone

logger = logging.getLogger(__name__)


class OutreachService:
    """Servicio para manejar estadísticas de Outreach Dashboard"""
    
    BASE_URL = 'https://outreachdashboard.wmflabs.org'
    CAMPAIGN_SLUG = 'wikimedia_colombia_2025'
    CACHE_DURATION = timedelta(minutes=5)  # Cache de 5 minutos
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SARA-WMCO/2.0 Django (Wikimedia Colombia)'
        })
    
    def parse_human_number(self, human_str):
        """
        Convierte números en formato humano a enteros.
        Ejemplos: "3M" -> 3000000, "1.65K" -> 1650, "402" -> 402
        """
        if not human_str or human_str == "0":
            return 0
        
        human_str = str(human_str).strip()
        
        try:
            # Si ya es un número
            if human_str.replace('.', '').replace(',', '').isdigit():
                return int(float(human_str.replace(',', '')))
            
            # Si tiene K (miles)
            if 'K' in human_str:
                num = float(human_str.replace('K', '').replace(',', ''))
                return int(num * 1000)
            
            # Si tiene M (millones)
            if 'M' in human_str:
                num = float(human_str.replace('M', '').replace(',', ''))
                return int(num * 1000000)
            
            return int(float(human_str.replace(',', '')))
        
        except (ValueError, AttributeError) as e:
            logger.warning(f"Error parseando número '{human_str}': {e}")
            return 0
    
    def get_cached_stats(self):
        """
        Obtiene estadísticas del cache si están frescas,
        si no, las actualiza desde el API.
        """
        try:
            cache = OutreachStatsCache.objects.get(campaign_slug=self.CAMPAIGN_SLUG)
            
            # Verificar si el cache está fresco
            if timezone.now() - cache.last_updated < self.CACHE_DURATION:
                logger.info("✅ Usando estadísticas en cache")
                return self._cache_to_dict(cache)
            
            # Cache expirado, actualizar
            logger.info("⏰ Cache expirado, actualizando...")
            return self.refresh_stats()
        
        except OutreachStatsCache.DoesNotExist:
            # No hay cache, obtener por primera vez
            logger.info("🆕 No hay cache, obteniendo estadísticas...")
            return self.refresh_stats()
    
    def refresh_stats(self):
        """
        Fuerza la actualización de estadísticas desde el API.
        """
        try:
            url = f'{self.BASE_URL}/campaigns/{self.CAMPAIGN_SLUG}.json'
            
            logger.info(f"🔍 Consultando Outreach Dashboard: {url}")
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            campaign = data.get('campaign', {})
            
            # Parsear estadísticas
            stats_data = {
                'programs': int(campaign.get('courses_count', 0)),
                'editors': int(campaign.get('user_count', 0)),
                'words_added': self.parse_human_number(campaign.get('word_count_human', 0)),
                'references_added': self.parse_human_number(campaign.get('references_count_human', 0)),
                'article_views': self.parse_human_number(campaign.get('view_sum_human', 0)),
                'articles_edited': self.parse_human_number(campaign.get('article_count_human', 0)),
                'articles_created': self.parse_human_number(campaign.get('new_article_count_human', 0)),
                'commons_uploads': self.parse_human_number(campaign.get('upload_count_human', 0)),
                'is_error': False,
                'error_message': '',
            }
            
            # Guardar en cache
            cache, created = OutreachStatsCache.objects.update_or_create(
                campaign_slug=self.CAMPAIGN_SLUG,
                defaults=stats_data
            )
            
            logger.info(f"✅ Estadísticas {'creadas' if created else 'actualizadas'}")
            logger.info(f"   - Programas: {stats_data['programs']}")
            logger.info(f"   - Editores: {stats_data['editors']}")
            logger.info(f"   - Palabras: {stats_data['words_added']:,}")
            
            return self._cache_to_dict(cache)
        
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error al obtener datos de Outreach: {e}")
            return self._save_error_state(str(e))
        
        except Exception as e:
            logger.error(f"❌ Error inesperado: {e}", exc_info=True)
            return self._save_error_state(str(e))
    
    def _cache_to_dict(self, cache):
        """Convierte el modelo de cache a diccionario."""
        return {
            'programs': cache.programs,
            'editors': cache.editors,
            'words_added': cache.words_added,
            'references_added': cache.references_added,
            'article_views': cache.article_views,
            'articles_edited': cache.articles_edited,
            'articles_created': cache.articles_created,
            'commons_uploads': cache.commons_uploads,
            'last_updated': cache.last_updated.strftime('%d/%m/%Y %H:%M'),
            'error': cache.is_error,
            'error_message': cache.error_message,
        }
    
    def _save_error_state(self, error_msg):
        """Guarda un estado de error en el cache."""
        try:
            cache = OutreachStatsCache.objects.get(campaign_slug=self.CAMPAIGN_SLUG)
            cache.is_error = True
            cache.error_message = error_msg
            cache.save()
            return self._cache_to_dict(cache)
        except OutreachStatsCache.DoesNotExist:
            # Crear cache con valores en 0 y estado de error
            cache = OutreachStatsCache.objects.create(
                campaign_slug=self.CAMPAIGN_SLUG,
                is_error=True,
                error_message=error_msg
            )
            return self._cache_to_dict(cache)