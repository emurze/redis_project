import logging

from dispather.exceptions import ParseCommandError
from apps.feature_app.container import FeatureAppContainer

lg = logging.getLogger(__name__)


def dispatch(args: list):
    feature_container = FeatureAppContainer()
    feature_commands = feature_container.get_commands()
    request = feature_container.get_request()

    try:
        cmd = args[0]
    except (KeyError, IndexError):
        raise ParseCommandError("I don't understand your command.")

    if service := feature_commands.get(cmd):
        service.run(request)
    else:
        lg.error('You have typed the incorrect command')
