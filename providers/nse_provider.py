import pandas as pd

from providers.base_provider import (
    BaseProvider
)


class NSEProvider(BaseProvider):

    def get_history(
        self,
        symbol,
        start_date,
        end_date
    ):

        print(
            f"NSE History Request: {symbol}"
        )

        return pd.DataFrame()

    def get_fundamentals(
        self,
        symbol
    ):

        print(
            f"NSE Fundamental Request: {symbol}"
        )

        return {}
