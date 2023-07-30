import strawberry


@strawberry.type(description="Output schema for healthCheck query")
class HealthCheckQuryOutput:
    message: str
