"""
reports/factory.py
Factory for creating the appropriate report generator based on type
"""
from django.core.exceptions import ObjectDoesNotExist
from .activity import ActivityReportGenerator
from .project import ProjectReportGenerator
from .event import EventReportGenerator


class ReportGeneratorFactory:
    """
    Factory class to create the appropriate report generator
    based on the report type and instance ID.
    """
    
    # Registry mapping report types to (Model, Generator)
    GENERATORS = {
        'activity': {
            'model': None,  # Will be set dynamically to avoid circular imports
            'generator': ActivityReportGenerator,
            'model_path': 'core.models.Activity',  # Update with your app name
        },
        'project': {
            'model': None,
            'generator': ProjectReportGenerator,
            'model_path': 'core.models.Project',
        },
        'event': {
            'model': None,
            'generator': EventReportGenerator,
            'model_path': 'core.models.Event',
        },
    }
    
    @classmethod
    def _get_model_class(cls, report_type):
        """
        Lazy load model class to avoid circular imports.
        
        Args:
            report_type: Type of report ('activity', 'event', 'project')
            
        Returns:
            Model class
        """
        if report_type not in cls.GENERATORS:
            raise ValueError(f"Unknown report type: {report_type}")
        
        config = cls.GENERATORS[report_type]
        
        # Lazy load the model if not already loaded
        if config['model'] is None:
            from django.apps import apps
            model_path = config['model_path']
            # model_path is like 'core.models.Activity'
            parts = model_path.split('.')
            app_label = parts[0]  # 'core'
            model_name = parts[-1]  # 'Activity'
            config['model'] = apps.get_model(app_label, model_name)
        
        return config['model']
    
    @classmethod
    def create(cls, report_type, instance_id, include_custom_sheets=True):
        """
        Create and return the appropriate report generator.
        
        Args:
            report_type: Type of report ('activity', 'event', 'project')
            instance_id: ID of the instance to generate report for
            include_custom_sheets: Whether to include custom sheets (default: True)
            
        Returns:
            Instance of the appropriate ReportGenerator subclass
            
        Raises:
            ValueError: If report_type is unknown
            ObjectDoesNotExist: If instance with given ID doesn't exist
        """
        if report_type not in cls.GENERATORS:
            raise ValueError(
                f"Unknown report type: {report_type}. "
                f"Valid types: {', '.join(cls.GENERATORS.keys())}"
            )
        
        # Get the model and generator classes
        model_class = cls._get_model_class(report_type)
        generator_class = cls.GENERATORS[report_type]['generator']
        
        # Fetch the instance
        try:
            instance = model_class.objects.get(pk=instance_id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                f"{model_class.__name__} with ID {instance_id} does not exist"
            )
        
        # Create and return the generator with context
        return generator_class(instance, include_custom_sheets=include_custom_sheets)