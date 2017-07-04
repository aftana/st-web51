sudo /etc/init.d/mysql start
mysql -uroot -e "CREATE USER 'admin'@'localhost'"
mysql -uroot -e "SET PASSWORD FOR 'admin'@'localhost' = PASSWORD('123')"
mysql -uroot -e "CREATE DATABASE stbase"
mysql -uroot -e "GRANT ALL ON stbase.* TO 'admin'@'localhost'"
