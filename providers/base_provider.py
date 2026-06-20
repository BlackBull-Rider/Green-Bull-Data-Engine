# providers/base_provider.py

class BaseProvider:

    def get_daily_data(self, date):
        raise NotImplementedError

    def get_history(self, symbol):
        raise NotImplementedError
