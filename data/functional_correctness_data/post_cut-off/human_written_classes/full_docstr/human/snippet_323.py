from homeassistant.util import dt as dt_util
import json
from homeassistant.const import EntityCategory
from typing import Dict, Any, Optional, List

class AttributeManager:
    """Manager for entity attributes."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the attribute manager."""
        self.config = config

    def prepare_attributes(self, topic: str, category: str, parts: List[str], metric_info: Optional[Dict]=None) -> Dict[str, Any]:
        """Prepare entity attributes."""
        try:
            attributes = {'topic': topic, 'category': category, 'parts': parts, 'last_updated': dt_util.utcnow().isoformat()}
            if metric_info:
                for key, value in metric_info.items():
                    if key not in ['name', 'device_class', 'state_class', 'unit']:
                        attributes[key] = value
            return attributes
        except Exception as ex:
            _LOGGER.exception('Error preparing attributes: %s', ex)
            return {'topic': topic, 'category': category}

    def process_json_payload(self, payload: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Process JSON payload to extract additional attributes."""
        try:
            json_data = json.loads(payload)
            if isinstance(json_data, dict):
                for key, value in json_data.items():
                    if key not in ['value', 'state', 'status'] and key not in attributes:
                        attributes[key] = value
                if 'timestamp' in json_data:
                    attributes['device_timestamp'] = json_data['timestamp']
            attributes['last_updated'] = dt_util.utcnow().isoformat()
        except (ValueError, json.JSONDecodeError):
            pass
        return attributes

    def determine_entity_category(self, category: str) -> Optional[EntityCategory]:
        """Determine EntityCategory from attribute category."""
        if category in ['diagnostic', 'network', 'system']:
            return EntityCategory.DIAGNOSTIC
        return None

    def get_gps_attributes(self, topic: str, payload: Any) -> Dict[str, Any]:
        """Extract and prepare GPS-related attributes."""
        attributes = {}
        try:
            if 'gpshdop' in topic.lower():
                try:
                    value = float(payload) if payload else None
                    attributes['gps_hdop'] = value
                    if value is not None:
                        accuracy = max(5, value * 5)
                        attributes['gps_accuracy'] = accuracy
                        attributes['gps_accuracy_unit'] = 'm'
                except (ValueError, TypeError):
                    pass
            elif 'gpssq' in topic.lower():
                try:
                    value = float(payload) if payload else None
                    attributes['gps_signal_quality'] = value
                    if value is not None:
                        accuracy = max(5, 100 - value)
                        attributes['gps_accuracy'] = accuracy
                        attributes['gps_accuracy_unit'] = 'm'
                except (ValueError, TypeError):
                    pass
            elif 'gpsspeed' in topic.lower():
                try:
                    value = float(payload) if payload else None
                    attributes['gps_speed'] = value
                except (ValueError, TypeError):
                    pass
        except Exception as ex:
            _LOGGER.exception('Error processing GPS attributes: %s', ex)
        return attributes