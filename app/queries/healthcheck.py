import strawberry

from app.schemas.healthcheck import HealthCheckQuryOutput

@strawberry.type
class HealthcheckQuery:
    @strawberry.field(description="Returns the state of the server")
    def healthcheck(self) -> HealthCheckQuryOutput:
        return HealthCheckQuryOutput(
            message="OK"
        )
