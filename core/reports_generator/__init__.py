"""
reports/generators/__init__.py
Convenient imports for all report generators
"""

from .base import BaseReportGenerator
from .activity import ActivityReportGenerator
from .project import ProjectReportGenerator

# Import these when you create them
# from .event import EventReportGenerator

__all__ = [
    'BaseReportGenerator',
    'ActivityReportGenerator',
    'ProjectReportGenerator',
    # 'EventReportGenerator',
]