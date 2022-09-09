start_all:
	make -C app build
	make -C app start_db
	make -C app start_scrapper

start_scrapper:
	make -C app start_scrapper

start_db:
	make -C app start_db

stop_db:
	make -C app down_db


