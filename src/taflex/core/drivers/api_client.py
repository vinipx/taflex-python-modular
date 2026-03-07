from abc import ABC, abstractmethod

class ApiClient(ABC):
    @abstractmethod
    def get(self, url):
        pass

    @abstractmethod
    def post(self, url, data):
        pass
