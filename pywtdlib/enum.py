class AuthorizationState(enumerate):
    AUTHORIZATION: str = "updateAuthorizationState"
    WAIT_CODE: str = "authorizationStateWaitCode"
    WAIT_PASSWORD: str = "authorizationStateWaitPassword"
    WAIT_TDLIB_PARAMETERS: str = "authorizationStateWaitTdlibParameters"
    WAIT_ENCRYPTION_KEY: str = "authorizationStateWaitEncryptionKey"
    WAIT_PHONE_NUMBER: str = "authorizationStateWaitPhoneNumber"
    WAIT_REGISTRATION: str = "authorizationStateWaitRegistration"
    WAIT_EMAIL_ADDRESS: str = "authorizationStateWaitEmailAddress"
    WAIT_EMAIL_CODE: str = "authorizationStateWaitEmailCode"
    READY: str = "authorizationStateReady"
    CLOSING: str = "authorizationStateClosing"
    CLOSED: str = "authorizationStateClosed"
    GET_AUTHORIZATION: str = "getAuthorizationState"


class Update(enumerate):
    NEW_MESSAGE: str = "updateNewMessage"
    ERROR: str = "error"
    SEND_MESSAGE: str = "sendMessage"
    FORWARD_MESSAGE: str = "forwardMessages"
    LIMIT_CHATS: int = 100000
