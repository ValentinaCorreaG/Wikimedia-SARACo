"""
reports/generators/project.py
Project-specific report generator
"""
import pandas as pd
from .base import BaseReportGenerator
from .activity import ActivityReportGenerator
# from .event import EventReportGenerator

class ProjectReportGenerator(BaseReportGenerator):
    """
    Generates Excel reports for Project instances.
    Includes project summary on main sheet and related activities on a separate sheet.
    """
    
    # Optional: Exclude specific fields from the report
    EXCLUDED_FIELDS = ['id']  # Inherit from base and add more if needed
    
    
    def prepare_data(self):
        """
        Convert Project instance to DataFrame using automatic extraction.
        Adds custom columns for related activities and events counts.
        """
        # Use the base class method to extract all model data automatically
        data = self.extract_model_data()
        
        # Add custom columns
        data['Total  Actividades'] = self.instance.activities.count()
        data['Total  Eventos'] = self.instance.events.count()
        
        self.df = pd.DataFrame([data])
    
    def add_custom_sheets(self, writer):
        """
        Add sheets with all related activities and events for this project.
        
        Args:
            writer: pandas ExcelWriter object
        """
        self._add_activities_sheet(writer)
        
        # self._add_events_sheet(writer)
    
    def _add_activities_sheet(self, writer):
        """
        Add a sheet with all related activities for this project.
        Uses ActivityReportGenerator without custom sheets to avoid nesting.
        
        Args:
            writer: pandas ExcelWriter object
        """
        activities = self.instance.activities.all()
        
        if activities.exists():
            # Prepare activities data - use generator WITHOUT custom sheets
            activities_data = []
            for activity in activities:
                # Pass include_custom_sheets=False to prevent nested sheets
                activity_gen = ActivityReportGenerator(activity, include_custom_sheets=False)
                activity_data = activity_gen.extract_model_data()
                activities_data.append(activity_data)
            
            activities_df = pd.DataFrame(activities_data)
            
            # Write to a new sheet
            activities_df.to_excel(writer, index=False, sheet_name='Actividades')
            
            # Apply formatting using base class method
            # Temporarily store the current df and use activities_df for formatting
            original_df = self.df
            self.df = activities_df
            self.apply_formatting(writer, sheet_name='Actividades')
            self.df = original_df
    
    # def _add_events_sheet(self, writer):
    #     """
    #     Add a sheet with all related events for this project.
    #     Uses EventReportGenerator without custom sheets to avoid nesting.
    #     
    #     Args:
    #         writer: pandas ExcelWriter object
    #     """
    #     events = self.instance.events.all()
    #     
    #     if events.exists():
    #         # Prepare events data - use generator WITHOUT custom sheets
    #         events_data = []
    #         for event in events:
    #             # Pass include_custom_sheets=False to prevent nested sheets
    #             event_gen = EventReportGenerator(event, include_custom_sheets=False)
    #             event_data = event_gen.extract_model_data()
    #             events_data.append(event_data)
    #         
    #         events_df = pd.DataFrame(events_data)
    #         
    #         # Write to a new sheet
    #         events_df.to_excel(writer, index=False, sheet_name='Eventos')
    #         
    #         # Apply formatting using base class method
    #         original_df = self.df
    #         self.df = events_df
    #         self.apply_formatting(writer, sheet_name='Eventos')
    #         self.df = original_df
    
    def validate_instance(self):
        """
        Validate Project-specific requirements.
        """
        # Call parent validation first
        is_valid, error_msg = super().validate_instance()
        if not is_valid:
            return is_valid, error_msg
        
        # Add Project-specific validation
        if not self.instance.name:
            return False, "El proyecto debe tener un nombre"
        
        if not self.instance.program:
            return False, "El proyecto debe estar asociado a un programa"
        
        return True, None
