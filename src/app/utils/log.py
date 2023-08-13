"Contains functions to combine logging.Logger, mu-python-template log & print"

# Built-in imports
from os import environ
from logging import log as logging_log, basicConfig, INFO, WARNING, ERROR, CRITICAL

# mu-python-template import
try:
    from helpers import log as _mu_log 
except ModuleNotFoundError:
    _mu_log = None


def env_var_rh_print_is_true() -> bool:
    """Returns True if the RH_PRINT environment variable is defined"""
    return bool(environ.get("RH_PRINT"))



def _log(message: str, level=int, console=env_var_rh_print_is_true()):
    """
    Runs the following commands:

    -                       logging.log                     with the specified level AND message
    - (If available)        mu-python-template.helpers.log  with the specified message
    - (If console=True)     Python print                    with the specified message
    """
    logging_log(level, message)

    if _mu_log:
        _mu_log(message)
    
    if console:
        print(message)


def log(level: str, message: str, console=env_var_rh_print_is_true()):
    """
    Wraps the _log function,
    converting the level string (INFO/WARNING/ERROR/CRITICAL) to its corresponding level integer
    """
    level = level.lower()
    if level == "info":
        level = INFO
    elif level == "warning":
        level = WARNING
    elif level == "error":
        level = ERROR
    elif level == "critical":
        level = CRITICAL
    
    _log(message, level, console)
    

def info(message: str, console=env_var_rh_print_is_true()):
    """Wraps _log, with the INFO level"""
    _log(message, INFO, console)

def warning(message: str, console=env_var_rh_print_is_true()):
    """Wraps _log, with the WARNING level"""
    _log(message, WARNING, console)

def error(message: str, console=env_var_rh_print_is_true()):
    """Wraps _log, with the ERROR level"""
    _log(message, ERROR, console)

def critical(message: str, console=env_var_rh_print_is_true()):
    """Wraps _log, with the CRITICAL level"""
    _log(message, CRITICAL, console)

