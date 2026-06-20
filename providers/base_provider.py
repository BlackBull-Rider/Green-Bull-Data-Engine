class BaseProvider:

    def get_history(
        self,
        symbol,
        start_date,
        end_date
    ):
        raise NotImplementedError

    def get_fundamentals(
        self,
        symbol
    ):
        raise NotImplementedError
