import json
from urllib.error import URLError
from unittest.mock import patch

from django.test import TestCase

from core.services import OutreachMetricsService


class MockResponse:
    def __init__(self, payload):
        self.payload = payload

    def read(self):
        return json.dumps(self.payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False


class OutreachMetricsServiceTests(TestCase):
    def setUp(self):
        self.service = OutreachMetricsService()

    def test_parse_human_number(self):
        self.assertEqual(self.service.parse_human_number("3M"), 3000000)
        self.assertEqual(self.service.parse_human_number("12K"), 12000)
        self.assertEqual(self.service.parse_human_number("2.72M"), 2720000)
        self.assertEqual(self.service.parse_human_number("1,234"), 1234)
        self.assertEqual(self.service.parse_human_number(None), 0)

    @patch("core.services.urlopen")
    def test_fetch_metrics_success(self, mock_urlopen):
        mock_urlopen.return_value = MockResponse(
            {
                "campaign": {
                    "courses_count": "22",
                    "user_count": "396",
                    "word_count_human": "3M",
                    "references_count_human": "12K",
                    "view_sum_human": "2.72M",
                    "article_count_human": "1.65K",
                    "new_article_count_human": "760",
                    "upload_count_human": "3.87K",
                }
            }
        )

        metrics = self.service.fetch_metrics()

        self.assertEqual(metrics["programs"], 22)
        self.assertEqual(metrics["editors"], 396)
        self.assertEqual(metrics["words_added"], 3000000)
        self.assertEqual(metrics["references_added"], 12000)
        self.assertEqual(metrics["article_views"], 2720000)
        self.assertEqual(metrics["articles_edited"], 1650)
        self.assertEqual(metrics["articles_created"], 760)
        self.assertEqual(metrics["commons_uploads"], 3870)
        self.assertFalse(metrics["error"])

    @patch("core.services.urlopen")
    def test_fetch_metrics_failure(self, mock_urlopen):
        mock_urlopen.side_effect = URLError("network error")

        metrics = self.service.fetch_metrics()

        self.assertEqual(metrics["programs"], 0)
        self.assertEqual(metrics["editors"], 0)
        self.assertEqual(metrics["words_added"], 0)
        self.assertEqual(metrics["references_added"], 0)
        self.assertEqual(metrics["article_views"], 0)
        self.assertEqual(metrics["articles_edited"], 0)
        self.assertEqual(metrics["articles_created"], 0)
        self.assertEqual(metrics["commons_uploads"], 0)
        self.assertTrue(metrics["error"])
