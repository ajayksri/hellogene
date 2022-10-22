# Build
# Install python/ dev tools
# Install rpm build
# Build Hello Service

yum install gcc openssl-devel bzip2-devel libffi-devel zlib-devel -y
yum install python3

# for jenkins
yum install git
yum install rpm-build

# Install Mongo Server
cp conf/mongo_repo /etc/yum.repos.d/mongodb.repo
yum -y update
yum install -y mongodb-org

systemctl daemon-reload
systemctl start mongod
sleep 10
mongostat -n 2

# Setup DB
# Install requirements.txt
# Install Hello service rpm