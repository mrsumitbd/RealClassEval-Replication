from lpm_kernel.utils import load_config
import json
from lpm_kernel.kernel import SecondMeKernel

class WeChatBot:

    def __init__(self):
        self.bot = Bot(cache_path='wxpy.pkl')
        logger.info('微信机器人初始化成功')
        try:
            config = load_config()
            self.second_me = SecondMeKernel(config)
            logger.info('Second-Me初始化成功')
        except Exception as e:
            logger.error(f'Second-Me初始化失败: {str(e)}')
            self.second_me = None

    def handle_message(self, msg):
        """处理接收到的消息"""
        try:
            content = msg.text
            sender = msg.sender
            logger.info(f'收到来自 {sender.name} 的消息: {content}')
            if self.second_me is None:
                msg.reply('抱歉，Second-Me服务未正确初始化，请稍后再试。')
                return
            response = self.second_me.process_message(content)
            if isinstance(response, dict):
                response = json.dumps(response, ensure_ascii=False)
            msg.reply(response)
        except Exception as e:
            logger.error(f'处理消息时出错: {str(e)}')
            msg.reply('抱歉，处理消息时出现错误。')

    def run(self):
        """运行机器人"""
        try:

            @self.bot.register()
            def print_messages(msg):
                self.handle_message(msg)
            self.bot.join()
        except Exception as e:
            logger.error(f'运行机器人时出错: {str(e)}')
            self.bot.logout()