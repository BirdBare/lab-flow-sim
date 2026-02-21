import typing

import streamlit


class SessionStateManager:
    class SessionStateItem[T]:
        @staticmethod
        def get(*args: typing.Any, **kwargs: typing.Any) -> T:
            raise NotImplementedError

        @staticmethod
        def set(value: T, *args: typing.Any, **kwargs: typing.Any) -> None:
            raise NotImplementedError

        @staticmethod
        def key(*args: typing.Any, **kwargs: typing.Any) -> str:
            raise NotImplementedError

    def __init__(self, *persistent_keys: str):
        self._skip_delete = False
        self._persistent_keys: set[str] = set()
        self._persistent_keys.add("orm_setup")
        # never remove the django state. It will cause multiple django instances which can cause db errors

        self.add_persistent_keys(*persistent_keys)

    def add_persistent_keys(self, *persistent_keys: str):
        self._persistent_keys |= set(persistent_keys)

    def skip_deletion_round(self):
        self._skip_delete = True

    def force_clear(self):
        if self._skip_delete:
            self._skip_delete = False
            return

        for key in streamlit.session_state:
            if key not in self._persistent_keys:
                del streamlit.session_state[key]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.force_clear()
