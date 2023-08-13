# Built-in imports
from os import environ
from logging import log as logging_log, basicConfig, INFO, WARNING, ERROR, CRITICAL

# mu-python-template import
try:
    from helpers import log as _mu_log 
except ModuleNotFoundError:
    _mu_log = None


def env_var_rh_print_is_true() -> bool:
    return bool(environ.get("RH_PRINT"))



def _log(message: str, level=int, console=env_var_rh_print_is_true()):
    logging_log(level, message)

    if _mu_log:
        _mu_log(message)
    
    if console:
        print(message)


def log(level: str, message: str, console=env_var_rh_print_is_true()):
    """Wraps _log"""
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
    _log(message, INFO, console)

def warning(message: str, console=env_var_rh_print_is_true()):
    _log(message, WARNING, console)

def error(message: str, console=env_var_rh_print_is_true()):
    _log(message, ERROR, console)

def critical(message: str, console=env_var_rh_print_is_true()):
    _log(message, CRITICAL, console)

