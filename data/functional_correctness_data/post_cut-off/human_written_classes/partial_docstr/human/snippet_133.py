import logging
import datetime
import json
import uuid
import threading
import redis
import time
import threading
import os

class TranscriptionCollectorClient:
    """Client that maintains connection to Redis on a separate thread
    and attempts auto-reconnection when the connection is lost."""

    def __init__(self, redis_stream_url=None):
        """Initialize client with redis connection URL.
        The connection will be established in a separate thread
        when connect() is called.

        Args:
            redis_stream_url: URL to redis server with the stream
        """
        self.redis_url = redis_stream_url or os.getenv('REDIS_STREAM_URL') or 'redis://localhost:6379/0'
        logging.info(f'TranscriptionCollectorClient instance creating with Redis URL: {self.redis_url}')
        self.redis_client = None
        self.is_connected = False
        self.connection_lock = threading.Lock()
        self.connection_thread = None
        self.stop_requested = False
        self.server_ref = None
        self.stream_key = os.getenv('REDIS_STREAM_KEY', 'transcription_segments')
        self.speaker_events_stream_key = os.getenv('REDIS_SPEAKER_EVENTS_RELATIVE_STREAM_KEY', 'speaker_events_relative')
        self.session_starts_published = set()
        self.connect()

    def connect(self):
        """Connect to Redis in a separate thread with auto-reconnection."""
        with self.connection_lock:
            if self.connection_thread and self.connection_thread.is_alive():
                logging.info('Connection thread already running.')
                return
            self.stop_requested = False
            self.connection_thread = threading.Thread(target=self._connection_worker, daemon=True)
            self.connection_thread.start()
            logging.info('Started connection thread.')

    def _connection_worker(self):
        """Worker thread that establishes and maintains Redis connection.
        Handles automatic reconnection with exponential backoff."""
        retry_delay = 1
        max_retry_delay = 30
        while not self.stop_requested:
            try:
                logging.info(f'Connecting to Redis at {self.redis_url}')
                self.redis_client = redis.from_url(self.redis_url, decode_responses=True)
                self.redis_client.ping()
                with self.connection_lock:
                    self.is_connected = True
                logging.info(f'Connected to Redis, stream key: {self.stream_key}')
                retry_delay = 1
                while not self.stop_requested:
                    self.redis_client.ping()
                    time.sleep(5)
            except redis.ConnectionError as e:
                logging.error(f'Redis connection error: {e}')
                with self.connection_lock:
                    self.is_connected = False
                    self.redis_client = None
            except Exception as e:
                logging.error(f'Redis error: {e}')
                with self.connection_lock:
                    self.is_connected = False
                    self.redis_client = None
            if self.stop_requested:
                break
            logging.info(f'Retrying connection in {retry_delay} seconds...')
            time.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, max_retry_delay)

    def disconnect(self):
        """Disconnect from Redis and stop the connection thread."""
        with self.connection_lock:
            self.stop_requested = True
            self.is_connected = False
            if self.redis_client:
                try:
                    self.redis_client.close()
                except Exception as e:
                    logging.error(f'Error closing Redis connection: {e}')
                self.redis_client = None
        if self.connection_thread and self.connection_thread.is_alive():
            self.connection_thread.join(timeout=5.0)
            logging.info('Disconnected from Redis')

    def publish_session_start_event(self, token, platform, meeting_id, session_uid):
        """Publish a session_start event to the Redis stream.

        Args:
            token: User's API token
            platform: Platform identifier (e.g., 'google_meet') 
            meeting_id: Platform-specific meeting ID
            session_uid: Unique identifier for this session

        Returns:
            Boolean indicating success or failure
        """
        if session_uid in self.session_starts_published:
            logging.debug(f'Session start already published for {session_uid}')
            return True
        if not self.is_connected or not self.redis_client:
            logging.warning('Cannot publish session_start: Not connected to Redis')
            return False
        if not all([token, platform, meeting_id, session_uid]):
            logging.error('Missing required fields for session_start event')
            return False
        try:
            now = datetime.datetime.utcnow()
            timestamp_iso = now.isoformat() + 'Z'
            payload = {'type': 'session_start', 'token': token, 'platform': platform, 'meeting_id': meeting_id, 'uid': session_uid, 'start_timestamp': timestamp_iso}
            message = {'payload': json.dumps(payload)}
            result = self.redis_client.xadd(self.stream_key, message)
            if result:
                logging.info(f'Published session_start event for session {session_uid}')
                self.session_starts_published.add(session_uid)
                return True
            else:
                logging.error(f'Failed to publish session_start event for {session_uid}')
                return False
        except Exception as e:
            logging.error(f'Error publishing session_start event: {e}')
            return False

    def publish_speaker_event(self, event_data: dict):
        """Publish a speaker_activity event to the new Redis stream.

        Args:
            event_data: The payload from the Vexa Bot's speaker_activity message.
                        This includes uid, relative_client_timestamp_ms, participant_name, etc.

        Returns:
            Boolean indicating success or failure
        """
        if not self.is_connected or not self.redis_client:
            logging.warning(f'Cannot publish speaker event to {self.speaker_events_stream_key}: Not connected to Redis')
            return False
        if not event_data or not isinstance(event_data, dict):
            logging.error(f'Invalid event_data for publishing to {self.speaker_events_stream_key}')
            return False
        try:
            now = datetime.datetime.utcnow()
            timestamp_iso = now.isoformat() + 'Z'
            redis_message_payload = event_data.copy()
            redis_message_payload['server_received_timestamp_iso'] = timestamp_iso
            result = self.redis_client.xadd(self.speaker_events_stream_key, redis_message_payload)
            if result:
                uid = redis_message_payload.get('uid', 'N/A')
                event_type = redis_message_payload.get('event_type', 'N/A')
                logging.info(f'Published speaker event ({event_type}) for UID {uid} to {self.speaker_events_stream_key}')
                return True
            else:
                uid = redis_message_payload.get('uid', 'N/A')
                logging.error(f'Failed to publish speaker event for UID {uid} to {self.speaker_events_stream_key}')
                return False
        except Exception as e:
            uid = event_data.get('uid', 'N/A')
            logging.error(f'Error publishing speaker event for UID {uid} to {self.speaker_events_stream_key}: {e}')
            logging.error(f'Error publishing transcription: {e}')
            return False

    def publish_session_end_event(self, token, platform, meeting_id, session_uid):
        if not self.is_connected or not self.redis_client:
            logging.warning(f'Cannot publish session_end for UID {session_uid}: Not connected to Redis')
            return False
        try:
            now = datetime.datetime.utcnow()
            timestamp_iso = now.isoformat() + 'Z'
            payload = {'type': 'session_end', 'token': token, 'platform': platform, 'meeting_id': meeting_id, 'uid': session_uid, 'end_timestamp': timestamp_iso}
            message = {'payload': json.dumps(payload)}
            result = self.redis_client.xadd(self.stream_key, message)
            if result:
                logging.info(f'Published session_end event for UID {session_uid} to {self.stream_key}')
                if session_uid in self.session_starts_published:
                    self.session_starts_published.remove(session_uid)
                return True
            else:
                logging.error(f'Failed to publish session_end for UID {session_uid} to {self.stream_key}')
                return False
        except Exception as e:
            logging.error(f'Error publishing session_end for UID {session_uid} to {self.stream_key}: {e}')
            return False

    def send_transcription(self, token, platform, meeting_id, segments, session_uid=None):
        """Send transcription segments to Redis stream (self.stream_key).

        Args:
            token: User's API token
            platform: Platform identifier (e.g., 'google_meet') 
            meeting_id: Platform-specific meeting ID
            segments: List of transcription segments
            session_uid: Optional unique identifier for this session

        Returns:
            Boolean indicating success or failure
        """
        if not self.is_connected or not self.redis_client:
            logging.warning(f'Cannot send transcription to {self.stream_key}: Not connected to Redis')
            return False
        if not all([token, platform, meeting_id]):
            logging.error(f'Missing required fields (token, platform, or meeting_id) for transcription UID {session_uid}')
            return False
        if not session_uid:
            logging.warning('session_uid not provided to send_transcription, generating one.')
            session_uid = str(uuid.uuid4())
        if session_uid not in self.session_starts_published:
            self.publish_session_start_event(token, platform, meeting_id, session_uid)
        try:
            payload = {'type': 'transcription', 'token': token, 'platform': platform, 'meeting_id': meeting_id, 'segments': segments, 'uid': session_uid}
            message = {'payload': json.dumps(payload)}
            result = self.redis_client.xadd(self.stream_key, message)
            if result:
                logging.debug(f'Published transcription with {len(segments)} segments for UID {session_uid} to {self.stream_key}')
                return True
            else:
                logging.error(f'Failed to publish transcription for UID {session_uid} to {self.stream_key}')
                return False
        except Exception as e:
            logging.error(f'Error publishing transcription for UID {session_uid} to {self.stream_key}: {e}')
            return False