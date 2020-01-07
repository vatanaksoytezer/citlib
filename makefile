ifeq ($(INSTALL_DIR),)
    INSTALL_DIR := /usr/local/bin
endif

install: 
	cp ucit $(INSTALL_DIR)
