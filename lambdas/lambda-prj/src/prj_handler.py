class PrjHandler:
    def __init__(self, config: Config) -> None:
        self.__config = config

    def do_something(self, event: events.SQSEvent) -> None:
        pass
