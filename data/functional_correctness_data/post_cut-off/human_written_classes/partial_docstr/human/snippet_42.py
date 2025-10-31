import json
import stripe
from datetime import datetime

class StripeManager:

    def __init__(self):
        logger.info('🔄 Initializing StripeManager')
        self.audit_entries = []
        logger.info('✅ Stripe configured')
        logger.debug('Test connection...')
        try:
            stripe.Customer.list(limit=1)
        except stripe.error.AuthenticationError as e:
            logger.critical('🔴 Invalid API key: %s', e)
            raise

    def log_operation(self, operation: str, parameters: dict) -> None:
        """Log all Stripe operations for audit purposes."""
        logger.debug('📝 Logging operation: %s with params: %s', operation, parameters)
        audit_entry = {'timestamp': datetime.utcnow().isoformat(), 'operation': operation, 'parameters': parameters}
        self.audit_entries.append(audit_entry)

    def _synthesize_audit_log(self) -> str:
        """Generate a human-readable audit log of all operations."""
        logger.debug('Generating audit log with %d entries', len(self.audit_entries))
        if not self.audit_entries:
            return 'No Stripe operations performed yet.'
        report = '📋 Stripe Operations Audit Log 📋\n\n'
        for entry in self.audit_entries:
            report += f"[{entry['timestamp']}]\n"
            report += f"Operation: {entry['operation']}\n"
            report += f"Parameters: {json.dumps(entry['parameters'], indent=2)}\n"
            report += '-' * 50 + '\n'
        return report