"""
Services for external metrics integrations.
"""
import json
from urllib.error import URLError
from urllib.request import urlopen


class OutreachMetricsService:
    """
    Fetch and normalize Wikimedia Outreach Dashboard campaign metrics.
    """
    CAMPAIGN_URL = (
        "https://outreachdashboard.wmflabs.org/campaigns/"
        "wikimedia_colombia_2025.json"
    )

    @staticmethod
    def parse_human_number(value):
        """
        Convert values like 3M, 12K, 2.72M or 1,234 to int.
        """
        if value in (None, ""):
            return 0

        if isinstance(value, (int, float)):
            return int(value)

        text = str(value).strip().upper().replace(",", "")
        multiplier = 1

        if text.endswith("K"):
            multiplier = 1_000
            text = text[:-1]
        elif text.endswith("M"):
            multiplier = 1_000_000
            text = text[:-1]
        elif text.endswith("B"):
            multiplier = 1_000_000_000
            text = text[:-1]

        try:
            return int(float(text) * multiplier)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def humanize_number(value):
        """
        Convert int to human format: 1234 -> 1.2K, 1200000 -> 1.2M
        """
        try:
            value = float(value)
        except (TypeError, ValueError):
            return "0"

        if value >= 1_000_000_000:
            return f"{value / 1_000_000_000:.1f}B".rstrip("0").rstrip(".")
        elif value >= 1_000_000:
            return f"{value / 1_000_000:.1f}M".rstrip("0").rstrip(".")
        elif value >= 1_000:
            return f"{value / 1_000:.1f}K".rstrip("0").rstrip(".")
        else:
            return str(int(value))

    def fetch_metrics(self):
        """
        Fetch campaign metrics from Outreach Dashboard.
        """
        try:
            with urlopen(self.CAMPAIGN_URL, timeout=15) as response:
                payload = json.loads(response.read().decode("utf-8"))

            campaign = payload.get("campaign", {})

            return {
                "programs": int(campaign.get("courses_count", 0)),
                "editors": int(campaign.get("user_count", 0)),

                "words_added": self.humanize_number(
                    self.parse_human_number(
                        campaign.get("word_count_human", 0)
                    )
                ),
                "references_added": self.humanize_number(
                    self.parse_human_number(
                        campaign.get("references_count_human", 0)
                    )
                ),
                "article_views": self.humanize_number(
                    self.parse_human_number(
                        campaign.get("view_sum_human", 0)
                    )
                ),
                "articles_edited": self.humanize_number(
                    self.parse_human_number(
                        campaign.get("article_count_human", 0)
                    )
                ),
                "articles_created": self.humanize_number(
                    self.parse_human_number(
                        campaign.get("new_article_count_human", 0)
                    )
                ),
                "commons_uploads": self.humanize_number(
                    self.parse_human_number(
                        campaign.get("upload_count_human", 0)
                    )
                ),

                "error": False,
            }

        except (URLError, TimeoutError, ValueError, json.JSONDecodeError):
            return {
                "programs": 0,
                "editors": 0,
                "words_added": "0",
                "references_added": "0",
                "article_views": "0",
                "articles_edited": "0",
                "articles_created": "0",
                "commons_uploads": "0",
                "error": True,
            }