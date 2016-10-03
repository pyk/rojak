wget http://dev.mysql.com/get/mysql-apt-config_0.8.0-1_all.deb
sudo dpkg -i mysql-apt-config_0.8.0-1_all.deb
sudo apt-get update
sudo apt-get install -y mysql-server
sudo apt-get install -y libmysqlclient-dev
sudo service mysql status

