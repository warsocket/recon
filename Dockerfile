FROM debian
RUN apt update && apt upgrade -y
ADD recon.py /opt/
ADD scripts /opt/scripts
RUN apt install -y python python-dnspython python-requests whois
ENTRYPOINT ["/opt/recon.py"]
