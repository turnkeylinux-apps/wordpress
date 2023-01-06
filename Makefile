PHP_EXTRA_PINS=libpcre2-8-0 libgd3
PHP_VERSION=8.1

COMMON_CONF = apache-credit

CREDIT_ANCHORTEXT = WordPress Appliance
define CREDIT_STYLE_EXTRA
body.wp-admin #turnkey-credit, body#image #turnkey-credit, body#media-upload #turnkey-credit { 
	display: none; 
}
endef

include $(FAB_PATH)/common/mk/turnkey/lamp.mk
include $(FAB_PATH)/common/mk/turnkey.mk
