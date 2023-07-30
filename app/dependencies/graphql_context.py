from functools import cached_property
from typing import Dict, Union

from fastapi import Depends
from sqlalchemy.orm import Session
from strawberry.fastapi import BaseContext
from strawberry.types import Info

from app.dependencies.database import get_db


class GraphQLContext(BaseContext):
    """
    Custom context class for handling GraphQL requests.

    This class provides a database session that can be accessed
    and used within GraphQL resolvers to interact with the database.

    Args:
        - session (Session): The database session to be used within GraphQL
        resolver functions. This session is created when the 'GraphQLContext'
        is initialized and is properly managed to ensure appropriate session
        handling throughout the GraphQL request processing.
    """

    def __init__(self, session: Session = Depends(get_db)) -> None:
        self.session = session


async def get_context(custom_context=Depends(GraphQLContext)):
    """
    This function acts as a dependency provider for GraphQL context in FastAPI

    Args:
        - custom_context (GraphQLContext): a custom GraphQL context that is to
        be provided to the GraphQL resolvers.


    Returns:
        - An instance of the 'GraphQLContext' class, which contains the database
        session and is available for use within GraphQL resolvers.
    """
    return custom_context


class CustomInfo(Info[GraphQLContext, Dict]):
    pass
