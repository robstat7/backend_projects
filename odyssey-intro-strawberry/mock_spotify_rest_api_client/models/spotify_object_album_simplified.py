from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..models.spotify_object_album_type import SpotifyObjectAlbumType
from ..models.spotify_object_release_date_precision import (
    SpotifyObjectReleaseDatePrecision,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.spotify_object_artist_simplified import SpotifyObjectArtistSimplified
    from ..models.spotify_object_external_url import SpotifyObjectExternalUrl
    from ..models.spotify_object_image import SpotifyObjectImage
    from ..models.spotify_object_restrictions import SpotifyObjectRestrictions


T = TypeVar("T", bound="SpotifyObjectAlbumSimplified")


@_attrs_define
class SpotifyObjectAlbumSimplified:
    """
    Attributes:
        album_type (SpotifyObjectAlbumType):
        artists (list['SpotifyObjectArtistSimplified']):
        available_markets (list[str]):
        external_urls (SpotifyObjectExternalUrl):
        href (str):
        id (str):
        images (list['SpotifyObjectImage']):
        name (str):
        release_date (str):
        release_date_precision (SpotifyObjectReleaseDatePrecision):
        total_tracks (float):
        type_ (Literal['album']):
        uri (str):
        restrictions (Union[Unset, SpotifyObjectRestrictions]):
    """

    album_type: SpotifyObjectAlbumType
    artists: list["SpotifyObjectArtistSimplified"]
    available_markets: list[str]
    external_urls: "SpotifyObjectExternalUrl"
    href: str
    id: str
    images: list["SpotifyObjectImage"]
    name: str
    release_date: str
    release_date_precision: SpotifyObjectReleaseDatePrecision
    total_tracks: float
    type_: Literal["album"]
    uri: str
    restrictions: Union[Unset, "SpotifyObjectRestrictions"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        album_type = self.album_type.value

        artists = []
        for artists_item_data in self.artists:
            artists_item = artists_item_data.to_dict()
            artists.append(artists_item)

        available_markets = self.available_markets

        external_urls = self.external_urls.to_dict()

        href = self.href

        id = self.id

        images = []
        for images_item_data in self.images:
            images_item = images_item_data.to_dict()
            images.append(images_item)

        name = self.name

        release_date = self.release_date

        release_date_precision = self.release_date_precision.value

        total_tracks = self.total_tracks

        type_ = self.type_

        uri = self.uri

        restrictions: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.restrictions, Unset):
            restrictions = self.restrictions.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "album_type": album_type,
                "artists": artists,
                "available_markets": available_markets,
                "external_urls": external_urls,
                "href": href,
                "id": id,
                "images": images,
                "name": name,
                "release_date": release_date,
                "release_date_precision": release_date_precision,
                "total_tracks": total_tracks,
                "type": type_,
                "uri": uri,
            }
        )
        if restrictions is not UNSET:
            field_dict["restrictions"] = restrictions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.spotify_object_artist_simplified import (
            SpotifyObjectArtistSimplified,
        )
        from ..models.spotify_object_external_url import SpotifyObjectExternalUrl
        from ..models.spotify_object_image import SpotifyObjectImage
        from ..models.spotify_object_restrictions import SpotifyObjectRestrictions

        d = dict(src_dict)
        album_type = SpotifyObjectAlbumType(d.pop("album_type"))

        artists = []
        _artists = d.pop("artists")
        for artists_item_data in _artists:
            artists_item = SpotifyObjectArtistSimplified.from_dict(artists_item_data)

            artists.append(artists_item)

        available_markets = cast(list[str], d.pop("available_markets"))

        external_urls = SpotifyObjectExternalUrl.from_dict(d.pop("external_urls"))

        href = d.pop("href")

        id = d.pop("id")

        images = []
        _images = d.pop("images")
        for images_item_data in _images:
            images_item = SpotifyObjectImage.from_dict(images_item_data)

            images.append(images_item)

        name = d.pop("name")

        release_date = d.pop("release_date")

        release_date_precision = SpotifyObjectReleaseDatePrecision(
            d.pop("release_date_precision")
        )

        total_tracks = d.pop("total_tracks")

        type_ = cast(Literal["album"], d.pop("type"))
        if type_ != "album":
            raise ValueError(f"type must match const 'album', got '{type_}'")

        uri = d.pop("uri")

        _restrictions = d.pop("restrictions", UNSET)
        restrictions: Union[Unset, SpotifyObjectRestrictions]
        if isinstance(_restrictions, Unset):
            restrictions = UNSET
        else:
            restrictions = SpotifyObjectRestrictions.from_dict(_restrictions)

        spotify_object_album_simplified = cls(
            album_type=album_type,
            artists=artists,
            available_markets=available_markets,
            external_urls=external_urls,
            href=href,
            id=id,
            images=images,
            name=name,
            release_date=release_date,
            release_date_precision=release_date_precision,
            total_tracks=total_tracks,
            type_=type_,
            uri=uri,
            restrictions=restrictions,
        )

        return spotify_object_album_simplified
