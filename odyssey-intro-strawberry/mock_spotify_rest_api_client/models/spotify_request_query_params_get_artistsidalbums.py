from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SpotifyRequestQueryParamsGETArtistsidalbums")


@_attrs_define
class SpotifyRequestQueryParamsGETArtistsidalbums:
    """
    Attributes:
        limit (Union[Unset, float]):
        offset (Union[Unset, float]):
        include_groups (Union[Unset, str]):
    """

    limit: Union[Unset, float] = UNSET
    offset: Union[Unset, float] = UNSET
    include_groups: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        limit = self.limit

        offset = self.offset

        include_groups = self.include_groups

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if limit is not UNSET:
            field_dict["limit"] = limit
        if offset is not UNSET:
            field_dict["offset"] = offset
        if include_groups is not UNSET:
            field_dict["include_groups"] = include_groups

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        limit = d.pop("limit", UNSET)

        offset = d.pop("offset", UNSET)

        include_groups = d.pop("include_groups", UNSET)

        spotify_request_query_params_get_artistsidalbums = cls(
            limit=limit,
            offset=offset,
            include_groups=include_groups,
        )

        return spotify_request_query_params_get_artistsidalbums
