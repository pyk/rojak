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
mysql -u root -p rojak_database < rojak_schema_latest.sql
```

Generate the dummy data:

```shell
ROJAK_DB_NAME=rojak_database sh populate_rojak_database_with_dummy_data.sh
```

## Debug

Make sure tables are created succesfully:

```shell
mysqlshow -u root -p -t -v rojak_database $TABLE_NAME
```

## Labelled & Unlabelled data

Labelled & Unlabelled data is available at:

* [Labeling Data detikcom](https://docs.google.com/spreadsheets/d/1F3CI4Kw417-WtwHYxAz0qo9ABgU8c96SHyJuHy7VahA/edit?usp=sharing)
