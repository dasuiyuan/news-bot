# -*- coding: utf-8 -*-
# @Time: 2024/8/28 17:50
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:
from llama_index.core import SimpleDirectoryReader
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex
from util import llm_util
from util.log_util import logger

import llama_index.core.instrumentation as instrument
from llama_index.core.instrumentation.event_handlers.base import (
    BaseEventHandler,
)

from llama_index.core.instrumentation.events.retrieval import (
    RetrievalStartEvent,
    RetrievalEndEvent,
)
from llama_index.core.instrumentation.events.query import (
    QueryEndEvent,
    QueryStartEvent,
)
import inspect
from datetime import datetime
from typing import Any, Dict, Optional, cast
from llama_index.core.instrumentation.span_handlers.simple import SimpleSpanHandler
from llama_index.core.instrumentation.span import SimpleSpan

from llama_index.core.instrumentation.events.base import BaseEvent

from llama_index.core.instrumentation.span.base import BaseSpan
from llama_index.core.instrumentation.span_handlers import BaseSpanHandler


class MyEventHandler(BaseEventHandler):
    """My custom EventHandler."""

    @classmethod
    def class_name(cls) -> str:
        """Class name."""
        return "MyEventHandler"

    def handle(self, event: BaseEvent, **kwargs) -> Any:
        """Logic for handling event."""
        # print(event.class_name())
        if isinstance(event, QueryStartEvent):
            logger.info("query start...")
        elif isinstance(event, RetrievalStartEvent):
            logger.info("retrieval start...")
        elif isinstance(event, RetrievalEndEvent):
            logger.info("retrieval end...")
        elif isinstance(event, QueryEndEvent):
            logger.info("query end...")


class MyCustomSpanHandler(SimpleSpanHandler):
    @classmethod
    def class_name(cls) -> str:
        """Class name."""
        return "MyCustomSpanHandler"

    def new_span(
            self,
            id_: str,
            bound_args: inspect.BoundArguments,
            instance: Optional[Any] = None,
            parent_span_id: Optional[str] = None,
            tags: Optional[Dict[str, Any]] = None,
            **kwargs: Any,
    ) -> SimpleSpan:
        """Create a span."""
        # logger.info(f"new span {id_}...")
        return super().new_span(id_, bound_args, instance, parent_span_id, tags)

    def span_enter(
            self,
            id_: str,
            bound_args: inspect.BoundArguments,
            instance: Optional[Any] = None,
            parent_id: Optional[str] = None,
            tags: Optional[Dict[str, Any]] = None,
            **kwargs: Any,
    ) -> None:
        logger.info(f"span enter {id_}")
        super().span_enter(id_, bound_args, instance, parent_id, tags)

    def span_exit(
            self,
            id_: str,
            bound_args: inspect.BoundArguments,
            instance: Optional[Any] = None,
            result: Optional[Any] = None,
            **kwargs: Any,
    ) -> None:
        span = self.open_spans[id_]
        span = cast(SimpleSpan, span)
        end_time = datetime.now()
        logger.info(f"span exit  {id_} cost 【{(end_time - span.start_time).total_seconds()}】 秒")
        super().span_exit(id_, bound_args, instance, result)

    def clear_span(self) -> None:
        with super().lock:
            super().completed_spans.clear()
            super().dropped_spans.clear()


if __name__ == '__main__':
    # define our LLM
    Settings.llm = llm_util.chat_qwen()

    # define embed model
    Settings.embed_model = llm_util.bge_m3_huggingface()

    my_event_handler = MyEventHandler()

    # simpleSpan = SimpleSpan()
    my_span_handler = MyCustomSpanHandler()

    dispatcher = instrument.get_dispatcher()
    dispatcher.add_event_handler(my_event_handler)
    dispatcher.add_span_handler(my_span_handler)

    # Load the your data
    documents = SimpleDirectoryReader(input_files=[r"../data/部门bp.txt"]).load_data()

    index = VectorStoreIndex.from_documents(documents, show_progress=True)
    query_engine = index.as_query_engine()
    response = query_engine.query("税务BP是谁？")
    logger.info(response)
    my_span_handler.print_trace_trees()
    print(my_span_handler.current_span_ids)
