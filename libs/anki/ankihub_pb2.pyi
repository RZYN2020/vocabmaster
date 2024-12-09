"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class LoginResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TOKEN_FIELD_NUMBER: builtins.int
    token: builtins.str
    def __init__(
        self,
        *,
        token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["token", b"token"]) -> None: ...

global___LoginResponse = LoginResponse

@typing.final
class LoginRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    PASSWORD_FIELD_NUMBER: builtins.int
    id: builtins.str
    password: builtins.str
    def __init__(
        self,
        *,
        id: builtins.str = ...,
        password: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["id", b"id", "password", b"password"]) -> None: ...

global___LoginRequest = LoginRequest

@typing.final
class LogoutRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TOKEN_FIELD_NUMBER: builtins.int
    token: builtins.str
    def __init__(
        self,
        *,
        token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["token", b"token"]) -> None: ...

global___LogoutRequest = LogoutRequest
