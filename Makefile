COMMON_CONF = apache-credit

PHP_MEMORY_LIMIT = 128M
PHP_UPLOAD_MAX_FILESIZE = 16M
PHP_POST_MAX_SIZE = 48M

CREDIT_ANCHORTEXT = WordPress Appliance
define CREDIT_STYLE_EXTRA
body.wp-admin #turnkey-credit, body#image #turnkey-credit, body#media-upload #turnkey-credit { 
	display: none; 
}
endef

include $(FAB_PATH)/common/mk/turnkey/lamp.mk
include $(FAB_PATH)/common/mk/turnkey.mk
