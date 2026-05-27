from typing import Annotated

from fastapi import Depends


class FakeSession:
    def __init__(self):
        self.open = True

    def close(self):
        self.open = False


def get_db_session():
    session = FakeSession()
    try:
        yield session
    finally:
        session.close()


DBSessionDep = Annotated[FakeSession, Depends(get_db_session)]
