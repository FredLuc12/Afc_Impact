# app/state/app_state.py

from uuid import UUID


class AppState:
    def __init__(self) -> None:
        self.current_installation_id: UUID | None = None
        self.current_page: str = 'dashboard'
        self.is_loading: bool = False
        self.last_error: str | None = None

    def set_installation(self, installation_id: UUID | None) -> None:
        self.current_installation_id = installation_id

    def set_page(self, page_name: str) -> None:
        self.current_page = page_name

    def start_loading(self) -> None:
        self.is_loading = True
        self.last_error = None

    def stop_loading(self) -> None:
        self.is_loading = False

    def set_error(self, message: str) -> None:
        self.last_error = message
        self.is_loading = False

    def clear_error(self) -> None:
        self.last_error = None


app_state = AppState()