import strawberry

from app.schemas.healthcheck import HealthCheckQuryOutput

@strawberry.type
class HealthcheckMutation:
    @strawberry.mutation(description="Returns the message given in the input")
    def healthcheck(self, message: str) -> HealthCheckQuryOutput:
        return HealthCheckQuryOutput(
            message=message
        )
