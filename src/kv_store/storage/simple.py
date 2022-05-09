from threading import Lock
from storage.facade import Capability


class DictionaryStorage:
    def __init__(self):
        self.capability = Capability(
            self, set(["get", "set", "delete", "exists", "reset"]), "DictionaryStorage"
        )
        self.storage = {}
        self.lock = Lock()

    def get(self, name: str) -> str:
        return self.storage[name]

    def exists(self, name: str) -> bool:
        return name in self.storage

    def set(self, name: str, value: str):
        locked = False
        try:
            self.lock.acquire()
            locked = True
            self.storage[name] = value
        finally:
            if locked:
                self.lock.release()

    def reset(self):
        locked = False
        try:
            self.lock.acquire()
            locked = True
            self.storage = {}
        finally:
            if locked:
                self.lock.release()

    def delete(self, name) -> bool:
        locked = False
        try:
            self.lock.acquire()
            locked = True

            if name not in self.storage:
                return False

            del self.storage[name]
            return True
        finally:
            if locked:
                self.lock.release()
