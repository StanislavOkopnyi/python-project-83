from page_analyzer.database import AbstractConnection


class MockConnection(AbstractConnection):

    def __init__(self) -> None:
        ...

    def execute(self, query):
        ...

    def execute_and_get_item(self, query):
        ...

    def execute_and_get_list(self, query):
        ...
