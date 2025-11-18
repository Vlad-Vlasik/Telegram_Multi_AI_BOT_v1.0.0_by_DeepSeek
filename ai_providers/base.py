from abc import ABC, abstractmethod

class BaseAIProvider(ABC):
    @abstractmethod
    async def generate_response(self, prompt: str) -> str:
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass