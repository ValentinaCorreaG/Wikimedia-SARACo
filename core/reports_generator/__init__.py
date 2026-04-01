"""
reports/generators/__init__.py
Convenient imports for all report generators
"""

from .base import BaseReportGenerator
from .activity import ActivityReportGenerator

# Import these when you create them
# from .event import EventReportGenerator
# from .project import ProjectReportGenerator

__all__ = [
    'BaseReportGenerator',
    'ActivityReportGenerator',
    # 'EventReportGenerator',
    # 'ProjectReportGenerator',
]