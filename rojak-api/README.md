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

## Spesifikasi API

Spesifikasi API dapat dilihat [di sini](api-spec.md) (WIP).

Spesifikasi API dibuat dengan menggunakan [RAML](http://raml.org/). Versi RAML yang digunakan adalah RAML 0.8. File [`api-spec.md`](api-spec.md) di-generate dengan otomatis menggunakan perkakas [`raml2md`](https://github.com/raml2html/raml2md). Untuk mengubah spesifikasi:

1. Pastikan sudah terinstall Node.js
2. Jalankan `npm i -g raml2md`
3. Ubah file [`api-spec.raml`](api-spec.raml)
4. Jalankan perintah `raml2md api-spec.raml > api-spec.md`
5. Commit kedua file tersebut.
