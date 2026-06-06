from abc import ABC, abstractmethod


class MemoryStore(ABC):

    @abstractmethod
    def create_session(
        self,
        user_id: str
    ):
        pass

    @abstractmethod
    def get_latest_session(
        self,
        user_id: str
    ):
        pass

    @abstractmethod
    def save_message(
        self,
        user_id: str,
        session_id: str,
        role: str,
        content: str
    ):
        pass

    @abstractmethod
    def get_history(
        self,
        user_id: str
    ):
        pass

    @abstractmethod
    def save_fact(
        self,
        user_id: str,
        fact: str
    ):
        pass

    @abstractmethod
    def get_facts(
        self,
        user_id: str
    ):
        pass

    @abstractmethod
    def clear_memory(
        self,
        user_id: str
    ):
        pass