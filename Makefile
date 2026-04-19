install:
	sudo cp swapman.py /usr/local/bin/swapman
	sudo chmod +x /usr/local/bin/swapman

uninstall:
	sudo rm /usr/local/bin/swapman

.PHONY: install uninstall
