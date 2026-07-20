from app.models.project import Project

class ApplicationState:
    """
    Stores the application's current state.
    """
    def __init__(self) -> None:
        self.project = Project()