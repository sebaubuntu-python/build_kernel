from logging import basicConfig, INFO, debug, error, info, warning
import traceback

basicConfig(format='[%(filename)s:%(lineno)s %(levelname)s] %(funcName)s: %(message)s',
            level=INFO)

LOGD = debug
LOGE = error
LOGI = info
LOGW = warning

def format_exception(exception):
	return ''.join(traceback.format_exception(type(exception), exception,
	                                          exception.__traceback__,
	                                          limit=None, chain=True))
