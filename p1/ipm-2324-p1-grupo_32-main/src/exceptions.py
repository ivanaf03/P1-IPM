class NotInternetException(Exception):
    # Raised when there is no Internet connection
    def __init__(self):
        super().__init__()

class NoResultsException(Exception):
    # Raised when no results are found in a query
    def __init__(self):
        super().__init__()