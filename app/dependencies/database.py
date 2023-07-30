from app.database.base import Session


def get_db():
    """
    Context manager for providing a database session within a code block.

    This function creates a database session using the 'Session' object and
    yields it to the calling code, allowing the code within the 'with' block
    to use the session. After the block of code is executed or if an exception
    is raised within the block, the session is automatically closed to release
    the database resources.
    """
    db = Session()
    try:
        yield db
    finally:
        db.close()
