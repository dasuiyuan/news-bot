# -*- coding: utf-8 -*-
# @Time: 2024/8/28 18:06
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:

from typing import Optional, List, Any, Sequence, Dict, Union
from llama_index.core.bridge.pydantic import Field, PrivateAttr
from llama_index.core.base.llms.types import MessageRole
from llama_index.core.constants import DEFAULT_CONTEXT_WINDOW, DEFAULT_NUM_OUTPUTS
from llama_index.core.llms import (
    CustomLLM,
    CompletionResponse,
    CompletionResponseGen,
    CompletionResponseAsyncGen,
    LLMMetadata,
)
from llama_index.core.llms.callbacks import llm_completion_callback, llm_chat_callback
from openai import OpenAI, AsyncOpenAI
from llama_index.core.base.llms.types import (
    ChatMessage,
    ChatResponse,
    ChatResponseGen,
    ChatResponseAsyncGen,
)
from settings import geoi_settings

DEFAULT_MODEL = geoi_settings.DEEPSEEK_MODEL
DEEPSEEK_API_KEY = geoi_settings.DEEPSEEK_API_KEY
DEEPSEEK_API_URL = geoi_settings.DEEPSEEK_API_URL


def to_message_dicts(messages: Sequence[ChatMessage]) -> List[Dict[str, str]]:
    message_dicts = []
    for message in messages:
        if not hasattr(message, 'role') or message.role is None:
            raise ValueError("Invalid message: missing or invalid 'role' attribute")
        message_dict = {'role': message.role.value, 'content': message.content}
        message_dicts.append(message_dict)
    return message_dicts


def get_additional_kwargs(response) -> Dict:
    return {
        "token_counts": response.usage.total_tokens,
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
    }


class DeepSeekOpenAIClient(OpenAI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"Authorization": f"Bearer {api_key}"}


class AsyncDeepSeekOpenAIClient(AsyncOpenAI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"Authorization": f"{api_key}"}


class ChatDeepSeek(CustomLLM):
    num_output: int = DEFAULT_NUM_OUTPUTS
    context_window: int = Field(default=DEFAULT_CONTEXT_WINDOW,
                                description="The maximum number of context tokens for the model.", gt=0, )
    model: str = Field(default=DEFAULT_MODEL, description="The ChatQwen model to use.")
    api_url: str = Field(default=None, description="The Qwen API url.")
    api_key: str = Field(default=None, description="The Qwen API key.")
    reuse_client: bool = Field(default=True, description=(
        "Reuse the client between requests. When doing anything with large "
        "volumes of async API calls, setting this to false can improve stability."
    ),
                               )

    _client: Optional[Any] = PrivateAttr()
    _aclient: Optional[Any] = PrivateAttr()

    def __init__(
            self,
            model: str = DEFAULT_MODEL,
            reuse_client: bool = True,
            api_key: Optional[str] = None,
            **kwargs: Any,
    ) -> None:
        super().__init__(
            model=model,
            api_key=api_key,
            reuse_client=reuse_client,
            **kwargs,
        )
        self._client = None
        self._aclient = None

    def _get_client(self) -> DeepSeekOpenAIClient:
        if not self.reuse_client:
            return DeepSeekOpenAIClient(base_url=self.api_url, api_key=self.api_key)

        if self._client is None:
            self._client = DeepSeekOpenAIClient(base_url=self.api_url, api_key=self.api_key)
        return self._client

    def _get_async_client(self) -> AsyncDeepSeekOpenAIClient:
        if not self.reuse_client:
            return AsyncDeepSeekOpenAIClient(base_url=self.api_url, api_key=self.api_key)

        if self._aclient is None:
            self._aclient = AsyncDeepSeekOpenAIClient(base_url=self.api_url, api_key=self.api_key)
        return self._aclient

    @classmethod
    def class_name(cls) -> str:
        return "chatDeepSeek_llm"

    @property
    def metadata(self) -> LLMMetadata:
        """Get LLM metadata."""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.num_output,
            model_name=self.model,
        )

    async def _achat(self, messages: List, stream=False) -> Any:

        response = await self._get_async_client().chat.completions.create(
            model=self.model,
            messages=messages,
            stream=stream
        )
        return response

    @llm_chat_callback()
    async def achat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        message_dicts: List = to_message_dicts(messages)
        response = await self._achat(message_dicts, stream=False)
        rsp = ChatResponse(
            message=ChatMessage(content=response.choices[0].message.content,
                                role=MessageRole(response.choices[0].message.role),
                                additional_kwargs={}),
            raw=response, additional_kwargs=get_additional_kwargs(response),
        )
        print(f"chat: {rsp} ")

        return rsp

    @llm_chat_callback()
    async def astream_chat(
            self,
            messages: Sequence[ChatMessage],
            **kwargs: Any,
    ) -> ChatResponseAsyncGen:

        message_dicts: List = to_message_dicts(messages)
        response = await self._achat(message_dicts, stream=True)

        async def gen() -> ChatResponseAsyncGen:
            response_txt = ""
            async for chunk in response:
                token = chunk.choices[0].delta.content
                response_txt += token
                yield ChatResponse(
                    message=ChatMessage(content=response_txt, role=MessageRole(chunk.choices[0].message.role),
                                        additional_kwargs={}, ), delta=token, raw=chunk, )

        return gen()

    @llm_completion_callback()
    async def acomplete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        messages = [{"role": "user", "content": prompt}]
        rsp = None
        try:
            response = await self._achat(messages, stream=False)

            rsp = CompletionResponse(text=str(response.choices[0].message.content),
                                     raw=response,
                                     additional_kwargs=get_additional_kwargs(response), )
        except Exception as e:
            print(f"complete: exception {e}")

        return rsp

    @llm_completion_callback()
    async def astream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseAsyncGen:
        messages = [{"role": "user", "content": prompt}]
        response = await self._achat(messages, stream=True)

        async def gen() -> CompletionResponseAsyncGen:
            response_txt = ""
            async for chunk in response:
                token = chunk.choices[0].delta.content
                response_txt += token
                yield CompletionResponse(text=response_txt, delta=token)

        return gen()

    def _chat(self, messages: List, stream=False) -> Any:

        response = self._get_client().chat.completions.create(
            model=self.model,  # 填写需要调用的模型名称
            messages=messages,
            stream=stream
        )
        return response

    @llm_chat_callback()
    def chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        message_dicts: List = to_message_dicts(messages)
        response = self._chat(message_dicts, stream=False)
        rsp = ChatResponse(
            message=ChatMessage(content=response.choices[0].message.content,
                                role=MessageRole(response.choices[0].message.role),
                                additional_kwargs={}),
            raw=response, additional_kwargs=get_additional_kwargs(response),
        )
        print(f"chat: {rsp} ")

        return rsp

    @llm_chat_callback()
    def stream_chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponseGen:
        response_txt = ""
        message_dicts: List = to_message_dicts(messages)
        response = self._chat(message_dicts, stream=True)
        for chunk in response:
            token = chunk.choices[0].delta.content
            response_txt += token
            yield ChatResponse(
                message=ChatMessage(content=response_txt, role=MessageRole(chunk.choices[0].message.role),
                                    additional_kwargs={}, ), delta=token, raw=chunk, )

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        messages = [{"role": "user", "content": prompt}]
        # print(f"complete: messages {messages} ")
        rsp = None
        try:
            response = self._chat(messages, stream=False)

            rsp = CompletionResponse(text=str(response.choices[0].message.content),
                                     raw=response,
                                     additional_kwargs=get_additional_kwargs(response), )
            # print(f"complete: {rsp} ")
        except Exception as e:
            print(f"complete: exception {e}")

        return rsp

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        response_txt = ""
        messages = [{"role": "user", "content": prompt}]
        response = self._chat(messages, stream=True)
        # print(f"stream_complete: {response} ")
        for chunk in response:
            # chunk.choices[0].delta # content='```' role='assistant' tool_calls=None
            token = chunk.choices[0].delta.content
            response_txt += token
            yield CompletionResponse(text=response_txt, delta=token)

    def stream_complete_origin(self, prompt: str, **kwargs: Any) -> Any:
        messages = [{"role": "user", "content": prompt}]
        response = self._chat(messages, stream=True)
        return response
