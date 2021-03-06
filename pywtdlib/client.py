import logging
from pywtdlib import __version__
from typing import Any, Callable, Dict, Optional
from getpass import getpass
from pywtdlib.enum import AuthorizationState, Update
from pywtdlib.tdjson import TdJson


class Client:
    def __init__(
        self,
        api_id: int,
        api_hash: str,
        use_file_database: Optional[bool] = False,
        use_chat_info_database: Optional[bool] = False,
        use_message_database: Optional[bool] = False,
        use_secret_chats: Optional[bool] = False,
        use_test_dc: Optional[bool] = False,
        enable_storage_optimizer: Optional[bool] = True,
        wait_timeout: Optional[int] = 1,
        verbosity: Optional[int] = 1,
    ) -> None:
        self.logger = logging.getLogger(__name__)

        # initial parameters
        self.api_id = api_id
        self.api_hash = api_hash
        self.use_file_database = use_file_database
        self.use_chat_info_database = use_chat_info_database
        self.use_message_database = use_message_database
        self.use_secret_chats = use_secret_chats
        self.use_test_dc = use_test_dc
        self.system_language = "en"
        self.device_model = "pywtdlib"
        self.app_version = __version__
        self.enable_storage_optimizer = enable_storage_optimizer
        self.authorized = False
        self.database_directory = "tdlib"
        self.tdjson = TdJson(wait_timeout, verbosity)
        self.error_handler = self.log_error

    def send_message(
        self,
        chat_id: int,
        message_thread_id: int,
        reply_to_message_id: int,
        options: Dict[Any, Any],
        reply_markup: Dict[Any, Any],
        input_message_content: Dict[Any, Any],
    ) -> None:
        self.tdjson.send(
            {
                "@type": Update.SEND_MESSAGE,
                "chat_id": chat_id,
                "message_thread_id": message_thread_id,
                "reply_to_message_id": reply_to_message_id,
                "options": options,
                "reply_markup": reply_markup,
                "input_message_content": input_message_content,
            }
        )

    def forward_message(
        self,
        chat_id: int,
        from_chat_id: int,
        messages_ids: list[int],
        options: Dict[Any, Any],
        send_copy: bool,
        remove_caption: bool,
    ) -> None:
        self.tdjson.send(
            {
                "@type": Update.FORWARD_MESSAGE,
                "chat_id": chat_id,
                "from_chat_id": from_chat_id,
                "message_ids": messages_ids,
                "options": options,
                "send_copy": send_copy,
                "remove_caption": remove_caption,
            }
        )

    def get_authorization_state(self) -> None:
        self.tdjson.send({"@type": AuthorizationState.GET_AUTHORIZATION})
        self.logger.info("Authorization started")

    def get_all_chats(self) -> None:
        self.tdjson.send({"@type": "getChats", "limit": Update.LIMIT_CHATS})

    def log_error(self, event: Dict[Any, Any]) -> None:
        event_encoded = str(event).encode("utf-8")
        self.logger.error(event_encoded)

    def authenticate_user(self, event: Dict[Any, Any]) -> None:
        # process authorization states
        if event["@type"] == AuthorizationState.AUTHORIZATION:
            auth_state = event["authorization_state"]

            # if client is closed, we need to destroy it and create new client
            if auth_state["@type"] == AuthorizationState.CLOSED:
                self.logger.critical(event)
                raise ValueError(event)

            # set TDLib parameters
            # you MUST obtain your own api_id and api_hash at https://my.telegram.org
            # and use them in the setTdlibParameters call
            if auth_state["@type"] == AuthorizationState.WAIT_TDLIB_PARAMETERS:
                self.tdjson.send(
                    {
                        "@type": "setTdlibParameters",
                        "parameters": {
                            "use_test_dc": self.use_test_dc,
                            "database_directory": self.database_directory,
                            "use_file_database": self.use_file_database,
                            "use_chat_info_database": self.use_chat_info_database,
                            "use_message_database": self.use_message_database,
                            "use_secret_chats": self.use_secret_chats,
                            "api_id": self.api_id,
                            "api_hash": self.api_hash,
                            "system_language_code": self.system_language,
                            "device_model": self.device_model,
                            "application_version": self.app_version,
                            "enable_storage_optimizer": self.enable_storage_optimizer,
                        },
                    }
                )
                self.logger.debug("TDLib parameters sent")

            # set an encryption key for database to let know TDLib how to open the database
            if auth_state["@type"] == AuthorizationState.WAIT_ENCRYPTION_KEY:
                self.tdjson.send(
                    {
                        "@type": "checkDatabaseEncryptionKey",
                        "encryption_key": "",
                    }
                )

            # enter phone number to log in
            if auth_state["@type"] == AuthorizationState.WAIT_PHONE_NUMBER:
                phone_number = input("Please enter your phone number: ")
                self.tdjson.send(
                    {
                        "@type": "setAuthenticationPhoneNumber",
                        "phone_number": phone_number,
                    }
                )
                self.logger.debug(f"Phone number sent: {phone_number}")

            # wait for authorization code
            if auth_state["@type"] == AuthorizationState.WAIT_CODE:
                code = input("Please enter the authentication code you received: ")
                self.tdjson.send({"@type": "checkAuthenticationCode", "code": code})
                self.logger.debug(f"Authentication code sent: {code}")

            # wait for first and last name for new users
            if auth_state["@type"] == AuthorizationState.WAIT_REGISTRATION:
                first_name = input("Please enter your first name: ")
                last_name = input("Please enter your last name: ")
                self.tdjson.send(
                    {
                        "@type": "registerUser",
                        "first_name": first_name,
                        "last_name": last_name,
                    }
                )

            # wait for password if present
            if auth_state["@type"] == AuthorizationState.WAIT_PASSWORD:
                password = getpass("Please enter your password: ")
                self.tdjson.send(
                    {
                        "@type": "checkAuthenticationPassword",
                        "password": password,
                    }
                )
                self.logger.debug("Password sent")

            # user authenticated
            if auth_state["@type"] == AuthorizationState.READY:
                # get all chats
                self.get_all_chats()

                self.authorized = True
                self.logger.info("User authorized")

    def set_update_handler(
        self, update_handler: Callable[[Dict[Any, Any]], None]
    ) -> None:
        self.update_handler = update_handler

    def set_routine_handler(self, routine_handler: Callable[[None], None]) -> None:
        self.routine_handler = routine_handler

    def set_error_handler(
        self, error_handler: Callable[[Dict[Any, Any]], None]
    ) -> None:
        self.error_handler = error_handler

    def start(self):
        # start the client by sending request to it
        self.get_authorization_state()

        try:
            # main events cycle
            while True:
                event = self.tdjson.receive()
                if event:
                    if not self.authorized:
                        self.authenticate_user(event)

                    if hasattr(self, "update_handler"):
                        self.update_handler(event)

                    if event["@type"] == "error":
                        self.error_handler(event)

                if hasattr(self, "routine_handler"):
                    self.routine_handler()

        except KeyboardInterrupt:
            self.tdjson.stop()
            self.logger.info("Execution stopped by the user")
