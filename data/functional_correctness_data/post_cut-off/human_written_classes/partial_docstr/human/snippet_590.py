import dashscope
from dashscope.api_entities.dashscope_response import DashScopeAPIResponse
import requests
from typing import Any, Dict, Iterator, List, Union
from dashscope.common.logging import logger
from dashscope.common.utils import _handle_http_failed_response, _handle_http_response, _handle_http_stream_response, default_headers, join_url
from http import HTTPStatus
from dashscope.common.constants import DEFAULT_REQUEST_TIMEOUT_SECONDS, REPEATABLE_STATUS, REQUEST_TIMEOUT_KEYWORD, SSE_CONTENT_TYPE, TaskStatus, HTTPMethod

class StreamEventMixin:

    @classmethod
    def _handle_stream(cls, response: requests.Response):
        is_error = False
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        for line in response.iter_lines():
            if line:
                line = line.decode('utf8')
                line = line.rstrip('\n').rstrip('\r')
                if line.startswith('event:error'):
                    is_error = True
                elif line.startswith('status:'):
                    status_code = line[len('status:'):]
                    status_code = int(status_code.strip())
                elif line.startswith('data:'):
                    line = line[len('data:'):]
                    yield (is_error, status_code, line)
                    if is_error:
                        break
                else:
                    continue

    @classmethod
    def _handle_response(cls, response: requests.Response):
        request_id = ''
        if response.status_code == HTTPStatus.OK and SSE_CONTENT_TYPE in response.headers.get('content-type', ''):
            for is_error, status_code, data in cls._handle_stream(response):
                if is_error:
                    yield DashScopeAPIResponse(request_id=request_id, status_code=status_code, output=None, code='', message='')
                else:
                    yield DashScopeAPIResponse(request_id=request_id, status_code=HTTPStatus.OK, output=data, usage=None)
        elif response.status_code == HTTPStatus.OK:
            json_content = response.json()
            request_id = ''
            if 'request_id' in json_content:
                request_id = json_content['request_id']
            yield DashScopeAPIResponse(request_id=request_id, status_code=HTTPStatus.OK, output=json_content, usage=None)
        else:
            yield _handle_http_failed_response(response)

    @classmethod
    def stream_events(cls, target, api_key: str=None, workspace: str=None, **kwargs) -> Iterator[DashScopeAPIResponse]:
        """Get job log.

        Args:
            target (str): The target to get, such as model_id.
            api_key (str, optional): The api api_key, if not present,
                will get by default rule(TODO: api key doc). Defaults to None.

        Returns:
            DashScopeAPIResponse: The target outputs.
        """
        custom_base_url = kwargs.pop('base_address', None)
        if custom_base_url:
            base_url = custom_base_url
        else:
            base_url = dashscope.base_http_api_url
        url = join_url(base_url, cls.SUB_PATH.lower(), target, 'stream')
        timeout = kwargs.pop(REQUEST_TIMEOUT_KEYWORD, DEFAULT_REQUEST_TIMEOUT_SECONDS)
        with requests.Session() as session:
            logger.debug('Starting request: %s' % url)
            response = session.get(url, headers={**_workspace_header(workspace), **default_headers(api_key), **kwargs.pop('headers', {})}, stream=True, timeout=timeout)
            logger.debug('Starting processing response: %s' % url)
            for rsp in cls._handle_response(response):
                yield rsp