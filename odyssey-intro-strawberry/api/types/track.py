import strawberry

@strawberry.type(
    description = "A track of a playlist."
)
class Track:
    # Track properties go here
    id: strawberry.ID = strawberry.field(description = "The ID for the track.")
    name: str = strawberry.field(description="The name of the track.")
    duration_ms: int = strawberry.field(description = "The duration of the track in ms.")
    uri: str = strawberry.field(description = "The link to the track.")
    explicit: bool = strawberry.field(description = "Denotes if the track is explicit.")
