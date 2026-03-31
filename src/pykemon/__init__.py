# read version from installed package
from importlib.metadata import version

__version__ = version("pykemon")


from pykemon.CRUD.team_editor import team_editor
