from app.models.project import Project
class ApplicationState:
    """
    Stores the current PKinetix application state.
    """
    def __init__(self) -> None:
        self.project = Project()