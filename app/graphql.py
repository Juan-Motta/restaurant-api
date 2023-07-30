import strawberry
from strawberry.fastapi import GraphQLRouter
from app.mutations import HealthcheckMutation
from app.queries import HealthcheckQuery
from app.dependencies.graphql_context import get_context

@strawberry.type
class Query(
    HealthcheckQuery
):
    pass

@strawberry.type
class Mutation(
    HealthcheckMutation
):
    pass


schema: strawberry.Schema = strawberry.Schema(query=Query, mutation=Mutation)

router: GraphQLRouter = GraphQLRouter(
    schema,
    context_getter=get_context
)