# Run hello server in background
# Ideally the systemd should be setup

SITE_PACKAGES=`python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])'`
HELLO_APP=${SITE_PACKAGES}/hello/app.py
nohup python3 ${HELLO_APP} 2>&1 >> /opt/helloservice/app.log