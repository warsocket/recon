all:
	docker build -t recon .
purge:
	docker rmi -f recon