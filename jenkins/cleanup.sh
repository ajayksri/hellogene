# Stop the web app
pid=`ps -aef | grep app | grep python3 | awk '{print $2}'`
kill -9 $pid

rpm -e HelloService

# Uninstall packages from requirements.txt
pip3 uninstall -r requirements.txt

systemctl stop mongod
yum remove -y mongodb-org
rm -f /etc/yum.repos.d/mongodb.repo
yum -y update

# Prepare build environment
yum remove rpm-build -y

# for jenkins
yum remove python3 -y
yum remove gcc openssl-devel bzip2-devel libffi-devel zlib-devel -y

