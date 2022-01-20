from logging import basicConfig, INFO, debug, error, info, warning
import traceback

def setup_logging(level = INFO):
	basicConfig(format='[%(filename)s:%(lineno)s %(levelname)s] %(funcName)s: %(message)s',
	            level=level)

LOGD = debug
LOGE = error
LOGI = info
LOGW = warning

def format_exception(exception):
	return ''.join(traceback.format_exception(type(exception), exception,
	                                          exception.__traceback__,
	                                          limit=None, chain=True))
