from botcity.maestro._version import get_versions

from .model import *  # noqa: F401, F403
from .sdk import BotMaestroSDK  # noqa: F401, F403

__version__ = get_versions()['version']
del get_versions
