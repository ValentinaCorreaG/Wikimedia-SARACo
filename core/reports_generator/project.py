"""
reports/generators/project.py
Project-specific report generator
"""
import pandas as pd
from .base import BaseReportGenerator
from .activity import ActivityReportGenerator
from .event import EventReportGenerator

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
        
        # Add event metrics if there are events
        if self.instance.events.exists():
            data['Total de Participantes en Eventos'] = self._get_total_event_participants()
            data['Diversidad Geográfica en Eventos'] = self._get_total_geographic_diversity()
            data['Satisfacción Promedio en Eventos'] = self._get_total_average_satisfaction()
            data['Tasa de Retención (2+ eventos) %'] = self._get_retention_rate()
        
        self.df = pd.DataFrame([data])
    
    def add_custom_sheets(self, writer):
        """
        Add sheets with all related activities and events for this project.
        
        Args:
            writer: pandas ExcelWriter object
        """
        self._add_activities_sheet(writer)
        
        self._add_events_sheet(writer)
        
        # Add attendance sheet if there are events
        if self.instance.events.exists():
            self._add_attendance_sheet(writer)
    
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
    
    def _add_events_sheet(self, writer):
        """
        Add a sheet with all related events for this project.
        Uses EventReportGenerator without custom sheets to avoid nesting.
        
        Args:
            writer: pandas ExcelWriter object
        """
        events = self.instance.events.all()
        
        if events.exists():
            # Prepare events data - use generator WITHOUT custom sheets
            events_data = []
            for event in events:
                # Pass include_custom_sheets=False to prevent nested sheets
                event_gen = EventReportGenerator(event, include_custom_sheets=False)
                event_data = event_gen.extract_model_data()
                
                # Add event-specific metrics
                event_data['Total de Participantes'] = event_gen._get_total_participants()
                event_data['Diversidad Geográfica'] = event_gen._get_geographic_diversity()
                event_data['Satisfacción Promedio'] = event_gen._get_average_satisfaction()
                
                events_data.append(event_data)
            
            events_df = pd.DataFrame(events_data)
         
            # Write to a new sheet
            events_df.to_excel(writer, index=False, sheet_name='Eventos')
         
            # Apply formatting using base class method
            original_df = self.df
            self.df = events_df
            self.apply_formatting(writer, sheet_name='Eventos')
            self.df = original_df
    
    def _add_attendance_sheet(self, writer):
        """
        Add a sheet with all attendance records from all events in this project.
        
        Args:
            writer: pandas ExcelWriter object
        """
        events = self.instance.events.all()
        
        if events.exists():
            # Collect all attendance records from all events
            attendance_data = []
            
            for event in events:
                attendances = event.attendances.all()
                
                for attendance in attendances:
                    # Extract attendance fields
                    row = {
                        'Evento': event.name,
                    }
                    
                    # Add all attendance fields
                    attendance_dict = self._extract_attendance_fields(attendance)
                    row.update(attendance_dict)
                    
                    attendance_data.append(row)
            
            if attendance_data:
                attendance_df = pd.DataFrame(attendance_data)
                
                # Write to a new sheet
                attendance_df.to_excel(writer, index=False, sheet_name='Asistencias')
                
                # Apply formatting
                original_df = self.df
                self.df = attendance_df
                self.apply_formatting(writer, sheet_name='Asistencias')
                self.df = original_df
    
    def _extract_attendance_fields(self, attendance):
        """
        Extract all fields from an Attendance model instance.
        Handles field formatting and display values.
        
        Args:
            attendance: Attendance model instance
        
        Returns:
            Dictionary with formatted attendance data
        """
        from core.models import Attendance
        
        data = {}
        
        # Get all fields from Attendance model
        fields = Attendance._meta.get_fields()
        
        for field in fields:
            # Skip excluded fields and reverse relations
            if field.name in ['id', 'event']:  # Skip primary key and foreign key to Event
                continue
            
            # Skip reverse relations
            if field.one_to_many or field.many_to_many:
                continue
            
            # Get label and value using base class methods
            label = self.get_field_label(field)
            
            # Get the value from the attendance instance
            value = getattr(attendance, field.name)
            
            # Handle different field types
            if field.choices:
                # Get the display value for choice fields
                get_display_method = f'get_{field.name}_display'
                if hasattr(attendance, get_display_method):
                    value = getattr(attendance, get_display_method)()
            elif hasattr(field, '__class__') and 'DateTimeField' in field.__class__.__name__:
                value = self.format_date(value, include_time=True)
            elif hasattr(field, '__class__') and 'DateField' in field.__class__.__name__:
                value = self.format_date(value, include_time=False)
            
            # Handle None values
            if value is None:
                value = ''
            
            data[label] = value
        
        return data
    
    def _get_total_event_participants(self):
        """
        Calculate total number of participants across all events in this project.
        
        Returns:
            int: Total number of attendance records across all events
        """
        total = 0
        for event in self.instance.events.all():
            total += event.attendances.count()
        return total
    
    def _get_total_geographic_diversity(self):
        """
        Calculate total geographic diversity as the number of unique departments
        represented across all events in this project.
        
        Returns:
            int: Number of unique departments
        """
        departments = set()
        
        for event in self.instance.events.all():
            for attendance in event.attendances.all():
                if attendance.department and attendance.department.strip():
                    departments.add(attendance.department)
        
        return len(departments)
    
    def _get_total_average_satisfaction(self):
        """
        Calculate weighted average satisfaction rating across all events in this project.
        
        Returns:
            float: Average satisfaction rating (rounded to 2 decimals), or 0 if no data
        """
        total_satisfaction = 0
        count = 0
        
        for event in self.instance.events.all():
            for attendance in event.attendances.all():
                if attendance.satisfaction:
                    total_satisfaction += attendance.satisfaction
                    count += 1
        
        if count == 0:
            return 0
        
        average = total_satisfaction / count
        return round(average, 2)
    
    def _get_retention_rate(self):
        """
        Calculate retention rate as the percentage of unique participants who 
        participated in 2 or more events within this project.
        
        Uses wiki_username as the primary identifier, falling back to email if needed.
        
        Returns:
            float: Retention rate percentage (rounded to 2 decimals), or 0 if no data
        """
        # Collect all participants and count their event participation
        participant_events = {}  # {identifier: set(event_ids)}
        
        for event in self.instance.events.all():
            for attendance in event.attendances.all():
                # Use wiki_username if available, otherwise use email
                identifier = attendance.wiki_username if attendance.wiki_username else attendance.email
                
                if identifier:
                    if identifier not in participant_events:
                        participant_events[identifier] = set()
                    participant_events[identifier].add(event.id)
        
        # If no participants, return 0
        if not participant_events:
            return 0
        
        # Count total unique participants
        total_unique = len(participant_events)
        
        # Count participants who attended 2 or more events
        repeat_participants = sum(1 for events in participant_events.values() if len(events) >= 2)
        
        # Calculate retention rate as percentage
        retention_rate = (repeat_participants / total_unique) * 100
        
        return round(retention_rate, 2)
    
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
