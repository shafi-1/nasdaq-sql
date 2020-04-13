# nasdaq-sql

Python script that uses the NASDAQ API to acquire stock data and input this stock data into a MySQL database.  
You can input the stocks you want and the script will feed the obtained data into your MySQL database.

## How to install MySQL Connector

Run the following in terminal:
```
pip3 install mysql-connector
```

## How to install MySQL Server:

Run the following in terminal:
```
sudo apt update
```
```
sudo apt upgrade
```
```
sudo apt install mysql-server
```
```
sudo mysql
```
```
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
```
```
FLUSH PRIVILEGES;
```
```
exit
```

## How to Log In to MySQL:

Execute this command in terminal:
```
mysql -u root -p
```
You will be prompted to enter password:
```
Enter password:
```

## Using MySQL

Create the database:
```
CREATE DATABASE MARKETS;
```
Select the database:
```
USE MARKETS;
```
Create a relation called NASDAQ on database
```
CREATE TABLE NASDAQ(
date DATETIME,
price FLOAT,
stock VARCHAR(10),
date_created TIMESTAMP);
```
Selecting all rows from relation
```
SELECT * from NASDAQ;
```
Deleting all rows from relation
```
DELETE FROM NASDAQ;
```

## Running the script

Execute:
```
python3 nasdaq_sql.py
```

