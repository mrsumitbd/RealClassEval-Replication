import django
import platform

class DeploymentMonitoringMiddleware:
    """
    Middleware to record environment values at the time of deployment for each service.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.record_python_version()
        self.record_django_version()
        response = self.get_response(request)
        return response

    @staticmethod
    def record_django_version():
        """
        Record the installed Django version as custom attribute

        .. custom_attribute_name: django_version
        .. custom_attribute_description: The django version in use (e.g. '2.2.24').
           Set by DeploymentMonitoringMiddleware.
        """
        _set_custom_attribute('django_version', django.__version__)

    @staticmethod
    def record_python_version():
        """
        Record the Python version as custom attribute

        .. custom_attribute_name: python_version
        .. custom_attribute_description: The Python version in use (e.g. '3.8.10').
           Set by DeploymentMonitoringMiddleware.
        """
        _set_custom_attribute('python_version', platform.python_version())