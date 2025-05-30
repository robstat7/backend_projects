from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="SpotifyObjectResumePoint")


@_attrs_define
class SpotifyObjectResumePoint:
    """
    Attributes:
        fully_played (bool):
        resume_position_ms (float):
    """

    fully_played: bool
    resume_position_ms: float

    def to_dict(self) -> dict[str, Any]:
        fully_played = self.fully_played

        resume_position_ms = self.resume_position_ms

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "fully_played": fully_played,
                "resume_position_ms": resume_position_ms,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        fully_played = d.pop("fully_played")

        resume_position_ms = d.pop("resume_position_ms")

        spotify_object_resume_point = cls(
            fully_played=fully_played,
            resume_position_ms=resume_position_ms,
        )

        return spotify_object_resume_point
