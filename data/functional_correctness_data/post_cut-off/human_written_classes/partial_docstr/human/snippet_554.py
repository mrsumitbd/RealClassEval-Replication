from archipy.helpers.utils.base_utils import BaseUtils
from datetime import datetime
from archipy.models.errors import InvalidArgumentError
import smtplib
from archipy.configs.config_template import EmailConfig

class EmailConnectionManager:
    """Manages SMTP connections with connection pooling and timeout handling."""

    def __init__(self, config: EmailConfig) -> None:
        self.config = config
        self.smtp_connection: smtplib.SMTP | None = None
        self.last_used: datetime | None = None

    def connect(self) -> None:
        """Establish SMTP connection with authentication."""
        if not self.config.SMTP_SERVER:
            raise InvalidArgumentError('SMTP_SERVER is required for email connection')
        try:
            self.smtp_connection = smtplib.SMTP(self.config.SMTP_SERVER, self.config.SMTP_PORT, timeout=self.config.CONNECTION_TIMEOUT)
            self.smtp_connection.starttls()
            if self.config.USERNAME and self.config.PASSWORD:
                self.smtp_connection.login(self.config.USERNAME, self.config.PASSWORD)
            self.last_used = datetime.now()
        except Exception as e:
            BaseUtils.capture_exception(e)
            self.smtp_connection = None

    def disconnect(self) -> None:
        """Close SMTP connection safely."""
        try:
            if self.smtp_connection:
                self.smtp_connection.quit()
                self.smtp_connection = None
        except Exception as e:
            BaseUtils.capture_exception(e)
        finally:
            self.smtp_connection = None

    def refresh_if_needed(self) -> None:
        """Refresh connection if needed based on timeout."""
        if not self.smtp_connection or not self.last_used:
            self.connect()
            return
        time_diff = (datetime.now() - self.last_used).total_seconds()
        if time_diff > 300:
            self.disconnect()
            self.connect()