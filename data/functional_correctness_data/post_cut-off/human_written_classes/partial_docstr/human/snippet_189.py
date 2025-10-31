import os
from typing import List, Dict
from datetime import datetime
import re

class Function:

    @staticmethod
    def detect_language(text):
        """
        判断输入文本是中文还是日文

        参数:
            text (str): 要检测的文本

        返回:
            str: "Chinese", "Japanese" 或 "Unknown"
        """
        chinese_ranges = [(19968, 40959), (13312, 19903), (131072, 173791), (173824, 177983), (177984, 178207), (178208, 183983), (63744, 64255), (13056, 13311)]
        japanese_ranges = [(12352, 12447), (12448, 12543), (12784, 12799), (65381, 65439)]
        chinese_count = 0
        japanese_count = 0
        for char in text:
            code = ord(char)
            for start, end in chinese_ranges:
                if start <= code <= end:
                    chinese_count += 1
                    break
            for start, end in japanese_ranges:
                if start <= code <= end:
                    japanese_count += 1
                    break
        if chinese_count > 0 and japanese_count == 0:
            return 'Chinese_ABS'
        elif japanese_count < chinese_count:
            return 'Chinese'
        else:
            return 'Japanese'

    @staticmethod
    def fix_ai_generated_text(text: str) -> str:
        """规范化带有情绪标签的文本，修正不符合格式的部分"""
        emotion_segments = re.findall('(【(.*?)】)([^【】]*)', text)
        if not emotion_segments:
            return text
        normalized_parts = []
        for full_tag, emotion_tag, following_text in emotion_segments:
            following_text = following_text.replace('(', '（').replace(')', '）')
            japanese_match = re.search('<(.*?)>', following_text)
            japanese_text = japanese_match.group(1).strip() if japanese_match else ''
            motion_match = re.search('（(.*?)）', following_text)
            motion_text = motion_match.group(1).strip() if motion_match else ''
            cleaned_text = re.sub('<.*?>|（.*?）', '', following_text).strip()
            if japanese_text:
                japanese_text = re.sub('（.*?）', '', japanese_text).strip()
            if japanese_text and cleaned_text:
                try:
                    lang_jp = Function.detect_language(japanese_text)
                    lang_clean = Function.detect_language(cleaned_text)
                    if lang_jp in ['Chinese', 'Chinese_ABS'] and lang_clean in ['Japanese', 'Chinese'] and (lang_clean != 'Chinese_ABS'):
                        cleaned_text, japanese_text = (japanese_text, cleaned_text)
                except Exception as e:
                    print(f'语言检测错误: {e}')
            normalized_part = full_tag
            if cleaned_text:
                normalized_part += cleaned_text
            if japanese_text:
                normalized_part += f'<{japanese_text}>'
            if motion_text:
                normalized_part += f'（{motion_text}）'
            if cleaned_text or (japanese_text and (not cleaned_text)):
                normalized_parts.append(normalized_part)
        return ''.join(normalized_parts)

    @staticmethod
    def parse_enhanced_txt(file_path):
        """
        解析settings.txt，包含里面的全部信息并且附带文件路径。

        Args:
            file_path (str): settings.txt的文件路径。

        Returns:
            settings :(dict) 返回角色的所有信息。
        """
        settings = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        single_line_pattern = re.compile('^(\\w+)\\s*=\\s*(.*?)\\s*$', re.MULTILINE)
        multi_line_pattern = re.compile('^(\\w+)\\s*=\\s*"""(.*?)"""\\s*$', re.MULTILINE | re.DOTALL)
        for match in multi_line_pattern.finditer(content):
            key = match.group(1)
            value = match.group(2).strip()
            settings[key] = value
        for match in single_line_pattern.finditer(content):
            key = match.group(1)
            if key not in settings:
                value = match.group(2).strip()
                if value.startswith('"') and value.endswith('"') or (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                settings[key] = value
        dir_path = os.path.dirname(file_path)
        settings['resource_path'] = dir_path
        return settings

    @staticmethod
    def parse_chat_log(content: str) -> List[Dict[str, str]]:
        """
        解析聊天内容字符串，将其转换为JSON所需的聊天记录列表，并提取对话日期。

        Args:
            content (str): 包含聊天记录的字符串内容。

        Returns:
            tuple: (datetime_object, list_of_chat_dicts)
                如果解析失败，则返回 (None, None)。
        """
        chat_records = []
        dialog_datetime = None
        try:
            lines = content.split('\n')
            first_line = lines[0]
            if first_line.startswith('对话日期:'):
                datetime_str = first_line.replace('对话日期:', '').strip()
                try:
                    dialog_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    print('错误: 聊天记录中的时间格式错误')
                    return (None, None)
            else:
                print("错误: 聊天记录格式不正确，未找到 '对话日期:'")
                return (None, None)
            current_speaker = None
            current_content_parts = []
            for line in lines[1:]:
                if line.startswith('设定:'):
                    if current_speaker and current_content_parts:
                        chat_records.append({'role': current_speaker, 'content': '\n'.join(current_content_parts)})
                        current_content_parts = []
                    current_content_parts = [line.replace('设定:', '').strip()]
                    current_speaker = 'system'
                elif line.startswith('用户:'):
                    if current_speaker and current_content_parts:
                        chat_records.append({'role': current_speaker, 'content': '\n'.join(current_content_parts)})
                        current_content_parts = []
                    current_content_parts = [line.replace('用户:', '').strip()]
                    current_speaker = 'user'
                elif line.startswith('钦灵:'):
                    if current_speaker and current_content_parts:
                        chat_records.append({'role': current_speaker, 'content': '\n'.join(current_content_parts)})
                        current_content_parts = []
                    current_content_parts = [line.replace('钦灵:', '').strip()]
                    current_speaker = 'assistant'
                elif current_speaker:
                    current_content_parts.append(line)
            if current_speaker and current_content_parts:
                chat_records.append({'role': current_speaker, 'content': '\n'.join(current_content_parts)})
            if not chat_records:
                print('警告: 未能解析出任何聊天内容')
                return (dialog_datetime, [])
            return (dialog_datetime, chat_records)
        except Exception as e:
            print(f'解析聊天记录时发生错误: {str(e)}')
            return (None, None)