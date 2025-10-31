from app.config import config
from typing import Optional, Dict, Any
import requests
import time

class SOARClient:

    def __init__(self):
        self.base_url = config.SOAR_API_URL
        self.headers = {'hg-token': config.SOAR_API_TOKEN, 'Content-Type': 'application/json'}
        self.timeout = config.SOAR_API_TIMEOUT
        self.retry_count = config.SOAR_RETRY_COUNT
        self.retry_delay = config.SOAR_RETRY_DELAY
        self.verify_ssl = config.SOAR_VERIFY_SSL

    def execute_playbook(self, playbook_id: int, params: Dict[str, Any]) -> Optional[str]:
        """
        执行SOAR剧本
        :param playbook_id: 剧本ID
        :param params: 剧本参数
        :return: 活动ID
        """
        url = f'{self.base_url}/api/event/execution'
        payload = {'eventId': 0, 'executorInstanceId': playbook_id, 'executorInstanceType': 'PLAYBOOK', 'params': [{'key': k, 'value': v} for k, v in params.items()]}
        logger.info(f'执行剧本: {playbook_id}, 参数: {params}')
        logger.debug(f'请求URL: {url}')
        logger.debug(f'请求体: {payload}')
        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=self.timeout, verify=self.verify_ssl)
            response.raise_for_status()
            result = response.json().get('result')
            logger.info(f'剧本执行成功，活动ID: {result}')
            return result
        except Exception as e:
            logger.error(f'剧本执行失败: {str(e)}')
            return None

    def get_playbook_status(self, activity_id: str) -> Optional[Dict[str, Any]]:
        """
        获取剧本执行状态
        :param activity_id: 活动ID
        :return: 状态信息
        """
        url = f'{self.base_url}/odp/core/v1/api/activity/{activity_id}'
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout, verify=self.verify_ssl)
            response.raise_for_status()
            return response.json().get('result')
        except Exception as e:
            logger.error(f'获取剧本状态失败: {str(e)}')
            return None

    def get_playbook_result(self, activity_id: str) -> Optional[Dict[str, Any]]:
        """
        获取剧本执行结果
        :param activity_id: 活动ID
        :return: 执行结果
        """
        url = f'{self.base_url}/odp/core/v1/api/event/activity'
        params = {'activityId': activity_id}
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout, verify=self.verify_ssl)
            response.raise_for_status()
            return response.json().get('result')
        except Exception as e:
            logger.error(f'获取剧本结果失败: {str(e)}')
            return None

    def wait_for_completion(self, activity_id: str, interval: int=5) -> Optional[Dict[str, Any]]:
        """
        等待剧本执行完成
        :param activity_id: 活动ID
        :param interval: 轮询间隔
        :return: 最终结果
        """
        for _ in range(self.retry_count):
            status = self.get_playbook_status(activity_id)
            if status and status.get('executeStatus') == 'SUCCESS':
                result = self.get_playbook_result(activity_id)
                return result
            time.sleep(interval)
        logger.warning(f'剧本执行超时: {activity_id}')
        return None