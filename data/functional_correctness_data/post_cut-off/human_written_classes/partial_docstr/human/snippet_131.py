import importlib
from typing import Dict, List
import re

class TranscriptionFilter:
    """Manages transcription filtering logic"""

    def __init__(self):
        self.custom_filters = []
        self.patterns = list(BASE_NON_INFORMATIVE_PATTERNS)
        self.min_character_length = 3
        self.min_real_words = 1
        self.stopwords = {}
        self.processed_segments_cache_by_meeting: Dict[int, List[Dict[str, any]]] = {}
        self.load_config()

    def load_config(self):
        """Load filter configuration from filter_config.py"""
        try:
            config = importlib.import_module('filter_config')
            if hasattr(config, 'ADDITIONAL_FILTER_PATTERNS'):
                self.patterns.extend(config.ADDITIONAL_FILTER_PATTERNS)
                logger.info(f'Added {len(config.ADDITIONAL_FILTER_PATTERNS)} patterns from config')
            if hasattr(config, 'MIN_CHARACTER_LENGTH'):
                self.min_character_length = config.MIN_CHARACTER_LENGTH
                logger.info(f'Set minimum character length to {self.min_character_length}')
            if hasattr(config, 'MIN_REAL_WORDS'):
                self.min_real_words = config.MIN_REAL_WORDS
                logger.info(f'Set minimum real words to {self.min_real_words}')
            if hasattr(config, 'CUSTOM_FILTERS'):
                self.custom_filters.extend(config.CUSTOM_FILTERS)
                logger.info(f'Added {len(config.CUSTOM_FILTERS)} custom filter functions')
            if hasattr(config, 'STOPWORDS'):
                self.stopwords = config.STOPWORDS
                logger.info(f'Loaded stopwords for {len(config.STOPWORDS)} languages')
            logger.info('Successfully loaded filter configuration')
        except ImportError:
            logger.warning('No filter_config.py found, using default settings')
        except Exception as e:
            logger.error(f'Error loading filter configuration: {e}')

    def add_custom_filter(self, filter_function):
        """
        Add a custom filter function

        Args:
            filter_function: Function that takes text and returns True if it should be kept
        """
        self.custom_filters.append(filter_function)

    def is_stop_word(self, word, language='en'):
        """Check if a word is a stopword in the given language"""
        return language in self.stopwords and word.lower() in self.stopwords[language]

    def clear_processed_segments_cache(self, meeting_id: int):
        """Clears the cache of processed segments for a specific meeting."""
        if meeting_id in self.processed_segments_cache_by_meeting:
            del self.processed_segments_cache_by_meeting[meeting_id]
            logger.debug(f'Cleared processed segments cache for meeting_id {meeting_id}.')
        else:
            logger.debug(f'No cache to clear for meeting_id {meeting_id}.')

    def filter_segment(self, text: str, start_time: float, end_time: float, meeting_id: int, language: str='en'):
        """
        Apply all filters to determine if segment should be kept

        Args:
            text (str): Text to filter
            start_time (float): Start time of the segment
            end_time (float): End time of the segment
            meeting_id (int): The ID of the current meeting for context-aware caching
            language (str): Language code for language-specific filtering

        Returns:
            bool: True if segment passes all filters, False otherwise
        """
        original_text_for_logging = text
        text = text.strip()
        if len(text) < self.min_character_length:
            logger.debug(f"Filtering out short text: '{original_text_for_logging}'")
            return False
        for pattern in self.patterns:
            if re.match(pattern, text):
                logger.debug(f"Filtering out text matching pattern {pattern}: '{original_text_for_logging}'")
                return False
        real_words = [w for w in text.split() if len(w) >= 3 and (not w.startswith('<')) and (not w.startswith('[')) and (not self.is_stop_word(w, language))]
        if len(real_words) < self.min_real_words:
            logger.debug(f"Filtering out text with insufficient real words: '{original_text_for_logging}'")
            return False
        current_meeting_cache = self.processed_segments_cache_by_meeting.setdefault(meeting_id, [])
        indices_to_remove_from_cache = []
        should_filter_current = False
        for i, cached_segment in enumerate(current_meeting_cache):
            cached_text = cached_segment['text']
            cached_start = cached_segment['start']
            cached_end = cached_segment['end']
            if text == cached_text:
                if start_time >= cached_start and end_time <= cached_end:
                    logger.debug(f"Filtering segment (identical text, sub-segment/duplicate): MeetingID {meeting_id}, '{text}' ({start_time}-{end_time}) due to cached: '{cached_text}' ({cached_start}-{cached_end})")
                    should_filter_current = True
                    break
                elif cached_start >= start_time and cached_end <= end_time:
                    logger.debug(f"Current segment (identical text, expansion): MeetingID {meeting_id}, '{text}' ({start_time}-{end_time}). Marking cached sub-segment for removal: '{cached_text}' ({cached_start}-{cached_end})")
                    indices_to_remove_from_cache.append(i)
            else:
                current_duration = end_time - start_time
                cached_duration = cached_end - cached_start
                min_duration_for_diff_text_overlap_check = 0.1
                if max(start_time, cached_start) < min(end_time, cached_end) and current_duration > min_duration_for_diff_text_overlap_check and (cached_duration > min_duration_for_diff_text_overlap_check):
                    if start_time >= cached_start and end_time <= cached_end and (cached_duration > current_duration) and (len(text) < len(cached_text)):
                        logger.debug(f"Filtering segment (different text, shorter, and sub-segment of longer cached): MeetingID {meeting_id}, '{text}' ({start_time}-{end_time}) due to overlapping longer cached: '{cached_text}' ({cached_start}-{cached_end})")
                        should_filter_current = True
                        break
                    elif cached_start >= start_time and cached_end <= end_time and (current_duration > cached_duration) and (len(cached_text) < len(text)):
                        logger.debug(f"Current segment (different text, longer, and expansion over cached): MeetingID {meeting_id}, '{text}' ({start_time}-{end_time}). Marking shorter cached sub-segment for removal: '{cached_text}' ({cached_start}-{cached_end})")
                        indices_to_remove_from_cache.append(i)
        if should_filter_current:
            return False
        if indices_to_remove_from_cache:
            for i_val in sorted(indices_to_remove_from_cache, reverse=True):
                del current_meeting_cache[i_val]
            logger.debug(f"Removed {len(indices_to_remove_from_cache)} sub-segments from cache for MeetingID {meeting_id} after processing current segment '{text}'.")
        for custom_filter in self.custom_filters:
            try:
                if not custom_filter(text):
                    logger.debug(f"Text filtered by custom filter {custom_filter.__name__} for MeetingID {meeting_id}: '{original_text_for_logging}'")
                    return False
            except Exception as e:
                logger.error(f'Error in custom filter {custom_filter.__name__} for MeetingID {meeting_id}: {e}')
        current_meeting_cache.append({'text': text, 'start': start_time, 'end': end_time})
        return True