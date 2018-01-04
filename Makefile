all:
	docker build -t recon .
rm: 
	docker rmi -f recon