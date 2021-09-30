from logging import basicConfig, INFO, debug, error, info, warning

basicConfig(format='[%(filename)s:%(lineno)s %(levelname)s] %(funcName)s: %(message)s',
            level=INFO)

LOGD = debug
LOGE = error
LOGI = info
LOGW = warning
