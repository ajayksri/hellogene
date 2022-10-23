# Prepare build environment
yum install gcc openssl-devel bzip2-devel libffi-devel zlib-devel -y
yum install python3 -y
# for jenkins
yum install git -y
yum install rpm-build -y

# Build the package
sh build.sh

# Install Mongo Server
cp conf/mongo_repo /etc/yum.repos.d/mongodb.repo
yum -y update
yum install -y mongodb-org
systemctl daemon-reload
systemctl start mongod
sleep 10
mongostat -n 2

# Setup DB
python3 conf/db_setup.py

# Install requirements.txt
pip3 install -r requirements.txt

# Install Hello service rpm, should pick from version file
rpm -ivh dist/HelloService-0.2.0-1.noarch.rpm