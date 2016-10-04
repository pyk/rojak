# RojakAPI

API untuk komunikasi antara rojak-ui-* dengan rojak-database.

## Development

Pastikan [Docker](https://docs.docker.com/engine/installation/) dan [Docker Compose](https://docs.docker.com/compose/install/) sudah terinstall.

1. Clone repo ini
2. `cd rojak-api`
3. `docker-compose up` (akan menyalakan service web dan db mysql)
4. Setup database lokal [(ikuti petunjuk di sini)](../rojak-database)
5. Open up [docker_host]:4000 and start hacking!

## Notes

### MySQL server

MySQL server untuk development menyala di [docker_host]:3306.

```
mysql -u root -h [docker_host]
```
