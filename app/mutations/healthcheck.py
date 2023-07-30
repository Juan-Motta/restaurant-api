import strawberry

from app.schemas.healthcheck import HealthCheckQuryOutput

@strawberry.type
class HealthcheckMutation:
    @strawberry.mutation
    def healthcheck(self, message: str) -> HealthCheckQuryOutput:
        return HealthCheckQuryOutput(
            message=message
        )
