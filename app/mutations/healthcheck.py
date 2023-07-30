import strawberry

from app.config.permissions import IsAuthenticated
from app.dependencies.graphql_context import CustomInfo
from app.schemas.healthcheck import HealthCheckQuryOutput


@strawberry.type
class HealthcheckMutation:
    @strawberry.mutation(
        description="Returns the message given in the input",
    )
    def healthcheck(
        self, message: str, info: CustomInfo
    ) -> HealthCheckQuryOutput:
        return HealthCheckQuryOutput(message=message)

    @strawberry.mutation(
        description="Returns the message given in the input only if user is authenticated",
        permission_classes=[IsAuthenticated],
    )
    def authenticated_healthcheck(
        self, message: str, info: CustomInfo
    ) -> HealthCheckQuryOutput:
        return HealthCheckQuryOutput(message=message)
