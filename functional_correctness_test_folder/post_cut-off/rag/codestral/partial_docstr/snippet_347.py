
class MessageBuilder:
    '''增强的消息构建器'''

    @staticmethod
    def build_text_message(content: str) -> Dict[str, Any]:
        '''构建文本消息'''
        return {
            "content": content,
            "type": "text"
        }

    @staticmethod
    def build_markdown_message(content: str, markdown: Dict[str, Any]) -> Dict[str, Any]:
        '''构建Markdown消息'''
        return {
            "content": content,
            "markdown": markdown,
            "type": "markdown"
        }

    @staticmethod
    def build_image_message(url: str) -> Dict[str, Any]:
        '''构建图片消息'''
        return {
            "url": url,
            "type": "image"
        }

    @staticmethod
    def build_file_message(file_info: Dict[str, Any]) -> Dict[str, Any]:
        '''构建文件消息'''
        return {
            "file_info": file_info,
            "type": "file"
        }

    @staticmethod
    def build_keyboard_message(content: str, keyboard: Dict[str, Any]) -> Dict[str, Any]:
        '''构建带按钮的消息'''
        return {
            "content": content,
            "keyboard": keyboard,
            "type": "keyboard"
        }

    @staticmethod
    def build_ark_message(ark: Dict[str, Any]) -> Dict[str, Any]:
        '''构建ARK消息'''
        return {
            "ark": ark,
            "type": "ark"
        }
