ifeq ($(INSTALL_DIR),)
    INSTALL_DIR := /usr/local/bin
endif

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
	COMMAND := sudo apt install --assume-yes gcc shc  
else
	COMMAND := brew install shc 
endif

install:
	$(COMMAND)
	shc -T -f ucit.sh
	rm -rf ucit.sh.x.c
	mv ucit.sh.x ucit
	cp ucit $(INSTALL_DIR)
