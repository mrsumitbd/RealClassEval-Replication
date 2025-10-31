from dashscope.common.error import InvalidParameter, InvalidTask, ModelRequired
from dashscope.api_entities.api_request_factory import _build_api_request
from dashscope.api_entities.dashscope_response import DashScopeAPIResponse
from dashscope.common.api_key import get_default_api_key

class BaseApi:
    """BaseApi, internal use only.

    """

    @classmethod
    def _validate_params(cls, api_key, model):
        if api_key is None:
            api_key = get_default_api_key()
        if model is None or not model:
            raise ModelRequired('Model is required!')
        return (api_key, model)

    @classmethod
    def call(cls, model: str, input: object, task_group: str, task: str=None, function: str=None, api_key: str=None, workspace: str=None, **kwargs) -> DashScopeAPIResponse:
        """Call service and get result.

        Args:
            model (str): The requested model, such as gpt3-v2
            input (object): The api input data, cannot be None.
            task_group (str, optional): The api task group.
            task (str, optional): The task name. Defaults to None.
            function (str, optional): The function of the task.
                Defaults to None.
            api_key (str, optional): The api api_key, if not present,
                will get by default rule(TODO: api key doc). Defaults to None.
            api_protocol (str, optional): Api protocol websocket or http.
                Defaults to None.
            ws_stream_mode (str, optional): websocket stream mode,
                [none, in, out, duplex]. Defaults to out.
            is_binary_input (bool, optional): Is input data binary.
                Defaults to False.
            http_method (str, optional): If api protocol is http, specifies
                method[GET, POST]. Defaults to POST.

        Returns:
            DashScopeAPIResponse: The service response.
        """
        api_key, model = BaseApi._validate_params(api_key, model)
        if workspace is not None:
            headers = {'X-DashScope-WorkSpace': workspace, **kwargs.pop('headers', {})}
            kwargs['headers'] = headers
        request = _build_api_request(model=model, input=input, task_group=task_group, task=task, function=function, api_key=api_key, **kwargs)
        return request.call()