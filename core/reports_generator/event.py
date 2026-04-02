"""
reports/generators/event.py
Event-specific report generator
"""
import pandas as pd
from .base import BaseReportGenerator


class EventReportGenerator(BaseReportGenerator):
    """
    Generates Excel reports for Event instances.
    Includes event summary on main sheet and all attendance records on a separate sheet.
    """

    # Optional: Exclude specific fields from the report
    EXCLUDED_FIELDS = ['id']  # Inherit from base and add more if needed

    def prepare_data(self):
        """
        Convert Event instance to DataFrame using automatic extraction.
        Adds custom columns for event-specific metrics.
        """
        # Use the base class method to extract all model data automatically
        data = self.extract_model_data()

        # Add custom columns for event metrics
        data['Total de Participantes'] = self._get_total_participants()
        data['Diversidad Geográfica'] = self._get_geographic_diversity()
        data['Satisfacción Promedio'] = self._get_average_satisfaction()

        self.df = pd.DataFrame([data])

    def add_custom_sheets(self, writer):
        """
        Add sheets with all attendance records for this event.

        Args:
            writer: pandas ExcelWriter object
        """
        self._add_attendance_sheet(writer)

    def _add_attendance_sheet(self, writer):
        """
        Add a sheet with all attendance records for this event.
        First column contains the event name, followed by all attendance fields.

        Args:
            writer: pandas ExcelWriter object
        """
        attendances = self.instance.attendances.all()

        if attendances.exists():
            # Prepare attendance data
            attendance_data = []

            for attendance in attendances:
                # Extract attendance fields
                row = {
                    'Evento': self.instance.name,
                }

                # Add all attendance fields using base extraction method
                attendance_dict = self._extract_attendance_fields(attendance)
                row.update(attendance_dict)

                attendance_data.append(row)

            attendance_df = pd.DataFrame(attendance_data)

            # Write to a new sheet
            attendance_df.to_excel(writer, index=False, sheet_name='Asistencias')

            # Apply formatting to the attendance sheet
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

    def _get_total_participants(self):
        """
        Calculate total number of participants in this event.
        
        Returns:
            int: Total number of attendance records
        """
        return self.instance.attendances.count()
    
    def _get_geographic_diversity(self):
        """
        Calculate geographic diversity as the number of unique departments
        represented in the event's attendance records.
        
        Returns:
            int: Number of unique departments
        """
        attendances = self.instance.attendances.all()
        
        # Get unique, non-empty departments
        departments = set()
        for attendance in attendances:
            if attendance.department and attendance.department.strip():
                departments.add(attendance.department)
        
        return len(departments)
    
    def _get_average_satisfaction(self):
        """
        Calculate average satisfaction rating for this event.
        
        Returns:
            float: Average satisfaction rating (rounded to 2 decimals), or 0 if no data
        """
        attendances = self.instance.attendances.all()
        
        if not attendances.exists():
            return 0
        
        # Sum all satisfaction ratings
        total_satisfaction = sum(
            attendance.satisfaction for attendance in attendances 
            if attendance.satisfaction
        )
        
        # Count how many records have satisfaction data
        count = sum(1 for attendance in attendances if attendance.satisfaction)
        
        if count == 0:
            return 0
        
        average = total_satisfaction / count
        return round(average, 2)

    def validate_instance(self):
        """
        Validate Event-specific requirements.
        """
        # Call parent validation first
        is_valid, error_msg = super().validate_instance()
        if not is_valid:
            return is_valid, error_msg

        # Add Event-specific validation
        if not self.instance.name:
            return False, "El evento debe tener un nombre"

        if not self.instance.start_date:
            return False, "El evento debe tener una fecha de inicio"

        if not self.instance.end_date:
            return False, "El evento debe tener una fecha de fin"

        return True, None
