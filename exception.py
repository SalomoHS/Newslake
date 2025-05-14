class SourceNotAvailable(Exception):
    def __init__(self, source):
        self.message = f"Source {source} not avaliable for all available regions."
        super().__init__(self.message)

class RegionNotAvailable(Exception):
    def __init__(self, region):
        self.message = f"Region '{region}' not avaliable."
        super().__init__(self.message)

class TopicNotAvailable(Exception):
    def __init__(self, topic):
        self.message = f"Topic '{topic}' not avaliable in all available regions."
        super().__init__(self.message)

class InvalidNNewsNumber(Exception):
    def __init__(self, n_news):
        self.message = f"Found n_news = {n_news}. n_news must be more than 0."
        super().__init__(self.message)

class InvalidEndDateError(Exception):
    def __init__(self):
        self.message = f"Invalid end date: expected a date in the past or present."
        super().__init__(self.message)

class InvalidDateRangeError(Exception):
    def __init__(self):
        self.message = f"Invalid date range: start date must be before or equal end date."
        super().__init__(self.message)