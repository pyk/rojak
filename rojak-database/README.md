# rojak-database

```
mysql-5.7
```

## Usage

Create the database first

```shell
mysql -u root -p
```

Afte loged in:

```sql
CREATE DATABASE rojak_database;
```

then exit.

Insert the tables:

```shell
mysql -u root -p rojak_database < mysql_tables.sql
```

## Debug

Make sure tables are created succesfully:

```shell
mysqlshow -u root -p -t -v rojak_database $TABLE_NAME
```
