from django.apps import AppConfig


class MaintenanceConfig(AppConfig):
    """
    🔍 EXPLANATION: App Configuration
    This class configures the maintenance app.
    The ready() method is called when Django starts.
    We use it to connect signals.
    """
    name = 'maintenance'
    
    def ready(self):
        """
        🔍 EXPLANATION: ready() method
        Called when Django starts.
        We import signals here to ensure they are connected.
        
        Why import here?
        - Signals need to be imported to be registered
        - Importing in ready() prevents circular imports
        - Ensures signals are connected when app loads
        """
        import maintenance.signals  # noqa
