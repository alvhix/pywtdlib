from typing import Any, Dict, Optional, Union
from ctypes import CDLL, CFUNCTYPE, c_int, c_char_p, c_double, c_void_p
from sys import exit
from os import path
import logging
import platform
import json


class TdJson:
    def __init__(
        self, wait_timeout: Optional[int] = 1, verbosity: Optional[int] = 1
    ) -> None:
        self.logger = logging.getLogger(__name__)

        extension = ""
        if platform.system() == "Windows":
            extension = "dll"
        elif platform.system() == "Linux":
            extension = "so"

        tdlib_path = path.join(
            path.dirname(__file__),
            f"lib/{platform.system()}/{platform.machine()}/libtdjson.{extension}",
        )

        # load shared library
        _tdjson = CDLL(tdlib_path)
        self.logger.info(f"TDLib located in {tdlib_path}")

        # tdlib wait time out between updates
        self.wait_timeout = wait_timeout

        # load TDLib functions from shared library
        self._create = _tdjson.td_json_client_create
        self._create.restype = c_void_p
        self._create.argtypes = []

        self._receive = _tdjson.td_json_client_receive
        self._receive.restype = c_char_p
        self._receive.argtypes = [c_void_p, c_double]

        self._send = _tdjson.td_json_client_send
        self._send.restype = None
        self._send.argtypes = [c_void_p, c_char_p]

        self._execute = _tdjson.td_json_client_execute
        self._execute.restype = c_char_p
        self._execute.argtypes = [c_void_p, c_char_p]

        self._destroy = _tdjson.td_json_client_destroy
        self._destroy.restype = None
        self._destroy.argtypes = [c_void_p]

        self._verbosity = _tdjson.td_set_log_verbosity_level
        self._verbosity.restype = None
        self._verbosity.argtypes = [c_int]

        # setting TDLib log verbosity
        self._verbosity(verbosity)

        fatal_error_callback_type = CFUNCTYPE(None, c_char_p)
        self._error_callback = _tdjson.td_set_log_fatal_error_callback
        self._error_callback.restype = None
        self._error_callback.argtypes = [fatal_error_callback_type]

        c_on_fatal_error_callback = fatal_error_callback_type(
            self.on_fatal_error_callback
        )
        self._error_callback(c_on_fatal_error_callback)

        # create client
        self.client = self._create()
        self.logger.debug(f"Client created: {self.client}")

    def on_fatal_error_callback(self, message) -> None:
        self.logger.critical(message)
        exit()

    # simple wrappers for tdlib client usage
    def send(self, query: Dict[Any, Any]) -> None:
        query = json.dumps(query).encode("utf-8")
        self._send(self.client, query)

    def receive(self) -> Union[Dict[Any, Any], Any]:
        result: Dict[Any, Any] = self._receive(self.client, self.wait_timeout)
        if result:
            result = json.loads(result.decode("utf-8"))
        return result

    def execute(self, query: Dict[Any, Any]) -> Union[Dict[Any, Any], Any]:
        query = json.dumps(query).encode("utf-8")
        result: Dict[Any, Any] = self._execute(self.client, query)
        if result:
            result = json.loads(result.decode("utf-8"))
        return result

    def stop(self) -> None:
        self._destroy(self.client)
