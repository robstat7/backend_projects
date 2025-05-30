from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define

T = TypeVar("T", bound="SpotifyObjectAuthorizationCodeCredentials")


@_attrs_define
class SpotifyObjectAuthorizationCodeCredentials:
    """
    Attributes:
        access_token (str):
        expires_in (float):
        refresh_token (str):
        scope (str):
        token_type (Literal['Bearer']):
    """

    access_token: str
    expires_in: float
    refresh_token: str
    scope: str
    token_type: Literal["Bearer"]

    def to_dict(self) -> dict[str, Any]:
        access_token = self.access_token

        expires_in = self.expires_in

        refresh_token = self.refresh_token

        scope = self.scope

        token_type = self.token_type

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "access_token": access_token,
                "expires_in": expires_in,
                "refresh_token": refresh_token,
                "scope": scope,
                "token_type": token_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        access_token = d.pop("access_token")

        expires_in = d.pop("expires_in")

        refresh_token = d.pop("refresh_token")

        scope = d.pop("scope")

        token_type = cast(Literal["Bearer"], d.pop("token_type"))
        if token_type != "Bearer":
            raise ValueError(
                f"token_type must match const 'Bearer', got '{token_type}'"
            )

        spotify_object_authorization_code_credentials = cls(
            access_token=access_token,
            expires_in=expires_in,
            refresh_token=refresh_token,
            scope=scope,
            token_type=token_type,
        )

        return spotify_object_authorization_code_credentials
