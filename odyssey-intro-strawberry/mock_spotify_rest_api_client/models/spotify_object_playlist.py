from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.spotify_object_external_url import SpotifyObjectExternalUrl
    from ..models.spotify_object_followers import SpotifyObjectFollowers
    from ..models.spotify_object_image import SpotifyObjectImage
    from ..models.spotify_object_paginated_spotify_object_playlist_track import (
        SpotifyObjectPaginatedSpotifyObjectPlaylistTrack,
    )
    from ..models.spotify_object_user_simplified import SpotifyObjectUserSimplified


T = TypeVar("T", bound="SpotifyObjectPlaylist")


@_attrs_define
class SpotifyObjectPlaylist:
    """
    Attributes:
        collaborative (bool):
        description (str):
        external_urls (SpotifyObjectExternalUrl):
        followers (SpotifyObjectFollowers):
        href (str):
        id (str):
        images (list['SpotifyObjectImage']):
        name (str):
        owner (SpotifyObjectUserSimplified):
        public (bool):
        snapshot_id (str):
        tracks (SpotifyObjectPaginatedSpotifyObjectPlaylistTrack):
        type_ (Literal['playlist']):
        uri (str):
    """

    collaborative: bool
    description: str
    external_urls: "SpotifyObjectExternalUrl"
    followers: "SpotifyObjectFollowers"
    href: str
    id: str
    images: list["SpotifyObjectImage"]
    name: str
    owner: "SpotifyObjectUserSimplified"
    public: bool
    snapshot_id: str
    tracks: "SpotifyObjectPaginatedSpotifyObjectPlaylistTrack"
    type_: Literal["playlist"]
    uri: str

    def to_dict(self) -> dict[str, Any]:
        collaborative = self.collaborative

        description = self.description

        external_urls = self.external_urls.to_dict()

        followers = self.followers.to_dict()

        href = self.href

        id = self.id

        images = []
        for images_item_data in self.images:
            images_item = images_item_data.to_dict()
            images.append(images_item)

        name = self.name

        owner = self.owner.to_dict()

        public = self.public

        snapshot_id = self.snapshot_id

        tracks = self.tracks.to_dict()

        type_ = self.type_

        uri = self.uri

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "collaborative": collaborative,
                "description": description,
                "external_urls": external_urls,
                "followers": followers,
                "href": href,
                "id": id,
                "images": images,
                "name": name,
                "owner": owner,
                "public": public,
                "snapshot_id": snapshot_id,
                "tracks": tracks,
                "type": type_,
                "uri": uri,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.spotify_object_external_url import SpotifyObjectExternalUrl
        from ..models.spotify_object_followers import SpotifyObjectFollowers
        from ..models.spotify_object_image import SpotifyObjectImage
        from ..models.spotify_object_paginated_spotify_object_playlist_track import (
            SpotifyObjectPaginatedSpotifyObjectPlaylistTrack,
        )
        from ..models.spotify_object_user_simplified import SpotifyObjectUserSimplified

        d = dict(src_dict)
        collaborative = d.pop("collaborative")

        description = d.pop("description")

        external_urls = SpotifyObjectExternalUrl.from_dict(d.pop("external_urls"))

        followers = SpotifyObjectFollowers.from_dict(d.pop("followers"))

        href = d.pop("href")

        id = d.pop("id")

        images = []
        _images = d.pop("images")
        for images_item_data in _images:
            images_item = SpotifyObjectImage.from_dict(images_item_data)

            images.append(images_item)

        name = d.pop("name")

        owner = SpotifyObjectUserSimplified.from_dict(d.pop("owner"))

        public = d.pop("public")

        snapshot_id = d.pop("snapshot_id")

        tracks = SpotifyObjectPaginatedSpotifyObjectPlaylistTrack.from_dict(
            d.pop("tracks")
        )

        type_ = cast(Literal["playlist"], d.pop("type"))
        if type_ != "playlist":
            raise ValueError(f"type must match const 'playlist', got '{type_}'")

        uri = d.pop("uri")

        spotify_object_playlist = cls(
            collaborative=collaborative,
            description=description,
            external_urls=external_urls,
            followers=followers,
            href=href,
            id=id,
            images=images,
            name=name,
            owner=owner,
            public=public,
            snapshot_id=snapshot_id,
            tracks=tracks,
            type_=type_,
            uri=uri,
        )

        return spotify_object_playlist
