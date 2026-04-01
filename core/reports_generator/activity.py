"""
reports/generators/activity.py
Activity-specific report generator
"""
import pandas as pd
from .base import BaseReportGenerator


class ActivityReportGenerator(BaseReportGenerator):
    """
    Generates Excel reports for Activity instances.
    Uses the base class methods for automatic field extraction and formatting.
    """
    
    # Optional: Exclude specific fields from the report
    EXCLUDED_FIELDS = ['id']  # Inherit from base and add more if needed
    
    
    def prepare_data(self):
        """
        Convert Activity instance to DataFrame using automatic extraction.
        """
        # Use the base class method to extract all model data automatically
        data = self.extract_model_data()
        
        self.df = pd.DataFrame([data])
    
    def validate_instance(self):
        """
        Validate Activity-specific requirements.
        """
        # Call parent validation first
        is_valid, error_msg = super().validate_instance()
        if not is_valid:
            return is_valid, error_msg
        
        # Add Activity-specific validation
        if not self.instance.proyecto:
            return False, "La actividad debe estar asociada a un proyecto"
        
        if not self.instance.nombre:
            return False, "La actividad debe tener un nombre"
        
        return True, None