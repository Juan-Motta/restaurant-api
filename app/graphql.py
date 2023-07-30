import strawberry
from strawberry.fastapi import GraphQLRouter

from app.dependencies.graphql_context import get_context
from app.mutations import HealthcheckMutation
from app.queries import HealthcheckQuery


@strawberry.type
class Query(HealthcheckQuery):
    pass


@strawberry.type
class Mutation(HealthcheckMutation):
    pass


schema: strawberry.Schema = strawberry.Schema(query=Query, mutation=Mutation)

router: GraphQLRouter = GraphQLRouter(schema, context_getter=get_context)
