from prometheus_client.metrics_core import InfoMetricFamily
from django.conf import settings

class AppMetricCollector:

    def __init__(self):
        self.info = InfoMetricFamily('mtp_app', 'Details of a money-to-prisoners app', value=dict(app=getattr(settings, 'APP', None) or 'unknown', environment=getattr(settings, 'ENVIRONMENT', None) or 'local', git_commit=getattr(settings, 'APP_GIT_COMMIT', None) or 'unknown', build_tag=getattr(settings, 'APP_BUILD_TAG', None) or 'unknown', build_date=getattr(settings, 'APP_BUILD_DATE', None) or 'unknown'))

    def collect(self):
        return [self.info]