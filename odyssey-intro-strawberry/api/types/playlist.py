import strawberry
from .track import Track
from mock_spotify_rest_api_client.api.playlists import get_playlists_tracks

@strawberry.type(
    description="A curated collection of tracks designed for a specific activity or mood."
)
class Playlist:
    # Playlist properties go here
    id: strawberry.ID = strawberry.field(description="The ID for the playlist.")
    name: str = strawberry.field(description="The name of the playlist.")
    description: str | None = strawberry.field(
    description="Describes the playlist, what to expect and entices the user to listen."
) # A description can be null
    # tracks: list[Track] = strawberry.field(description="The playlist's tracks.")
    _tracks: strawberry.Private[list[Track] | None] = None

    @strawberry.field(description="The tracks in the playlist.")
    async def tracks(
        self,
        info: strawberry.Info
    ) -> list[Track]:
        if self._tracks is None:
            spotify_client = info.context["spotify_client"]
            data = await get_playlists_tracks.asyncio(
      client=spotify_client, playlist_id=self.id
  )
            self._tracks = [
      Track(
          id=strawberry.ID(item.track.id),
          name=item.track.name,
          duration_ms=item.track.duration_ms,
          explicit=item.track.explicit,
          uri=item.track.uri,
      )
      for item in data.items
  ]

        return self._tracks
