import requests
import logging

logger = logging.getLogger(__name__)

class OutreachService:
    """Servicio simple para obtener estadísticas de Outreach Dashboard"""
    
    BASE_URL = 'https://outreachdashboard.wmflabs.org'
    CAMPAIGN_SLUG = 'wikimedia_colombia_2025'
    
    def parse_human_number(self, human_str):
        """Convierte "3M" -> 3000000, "1.65K" -> 1650"""
        if not human_str or human_str == "0":
            return 0
        
        human_str = str(human_str).strip()
        
        try:
            if 'K' in human_str:
                return int(float(human_str.replace('K', '').replace(',', '')) * 1000)
            if 'M' in human_str:
                return int(float(human_str.replace('M', '').replace(',', '')) * 1000000)
            return int(float(human_str.replace(',', '')))
        except:
            return 0
    
    def get_stats(self):
        """Obtiene estadísticas del Outreach Dashboard"""
        try:
            url = f'{self.BASE_URL}/campaigns/{self.CAMPAIGN_SLUG}.json'
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            campaign = data.get('campaign', {})
            
            return {
                'programs': int(campaign.get('courses_count', 0)),
                'editors': int(campaign.get('user_count', 0)),
                'words_added': self.parse_human_number(campaign.get('word_count_human', 0)),
                'references_added': self.parse_human_number(campaign.get('references_count_human', 0)),
                'article_views': self.parse_human_number(campaign.get('view_sum_human', 0)),
                'articles_edited': self.parse_human_number(campaign.get('article_count_human', 0)),
                'articles_created': self.parse_human_number(campaign.get('new_article_count_human', 0)),
                'commons_uploads': self.parse_human_number(campaign.get('upload_count_human', 0)),
                'error': False
            }
        except Exception as e:
            logger.error(f"Error obteniendo stats de Outreach: {e}")
            return {
                'programs': 0, 'editors': 0, 'words_added': 0, 'references_added': 0,
                'article_views': 0, 'articles_edited': 0, 'articles_created': 0,
                'commons_uploads': 0, 'error': True
            }