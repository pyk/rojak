# RojakAPI

API untuk komunikasi antara rojak-ui-* dengan rojak-database.

## Development

Pastikan [Docker](https://docs.docker.com/engine/installation/) dan [Docker Compose](https://docs.docker.com/compose/install/) sudah terinstall.

1. Clone repo ini
2. `cd rojak-api`
3. `docker-compose run --rm --no-deps web mix deps.get` (instalasi dependencies)
4. `docker-compose up` (akan menyalakan service web dan db mysql)
5. Setup database lokal [(ikuti petunjuk di sini)](../rojak-database)
6. Open up [docker_host]:4000 and start hacking!

## Notes

### MySQL server

MySQL server untuk development menyala di [docker_host]:3306.

```
$ mysql -u root -h [docker_host]
```

### Konfigurasi port

Jika aplikasi ingin dijalankan di port selain yang telah ditentukan, kita bisa melakukannya dengan memberikan env variable PORT dan DB_PORT untuk perintah `docker-compose up`. Contoh:

```
$ PORT=5000 DB_PORT=3307 docker-compose up
```

Dengan perintah ini, API dapat diakses pada [docker host]:5000 dan MySQL pada [docker host]:3307.

## Spesifikasi API

Spesifikasi API dapat dilihat [di sini](./api-spec.md) (WIP).

Spesifikasi API dibuat dengan menggunakan [RAML](http://raml.org/). Versi RAML yang digunakan adalah RAML 0.8. File [`api-spec.md`](./api-spec.md) di-generate dengan otomatis menggunakan perkakas [`raml2md`](https://github.com/raml2html/raml2md). Untuk mengubah spesifikasi:

1. Pastikan sudah terinstall Node.js
2. Jalankan `npm i -g raml2md`
3. Ubah file [`api-spec.raml`](./api-spec.raml)
4. Jalankan perintah `raml2md api-spec.raml > api-spec.md`
5. Commit kedua file tersebut.

## Docker Production Build Instruction

Kita menggunakan [Distillery](https://github.com/bitwalker/distillery) untuk membuat OTP release dari app. Metode ini membundle Erlang Run Time System (ERTS) agar hasil kompilasi dapat menjadi executable binary tanpa dependency terhadap Erlang dan Elixir. Lebih jauh dapat dilihat [di issue ini](https://github.com/pyk/rojak/issues/15#issue-181098631).

Pastikan kita sudah memiliki image `rojakapi_web` dari hasil build docker-compose (dapat dicek dengan perintah `docker images`). Jika belum ada, jalankan perintah `docker-compose build` sebelum melanjutkan ke bagian selanjutnya.

### Building

Berikut adalah step untuk melakukan build image production:

1. Bump version di file [`mix.exs`](./mix.exs)
2. Lakukan release version tersebut (misal versi 1.0.0):
    ```
    $ ./build-release.sh 1.0.0
    ```
3. Perintah tersebut akan menghasilkan sebuah docker image bernama `rojak/rojak-api` dengan tag sesuai version yang siap untuk dijalankan.

### Usage

```
$ docker run -p [port]:4000 \
    -e SECRET_KEY_BASE=[lengthy_secret_key_base] \
    -e DB_USERNAME=[db_username] \
    -e DB_PASSWORD=[db_password] \
    -e DB_NAME=[db_name] \
    -e DB_HOST=[db_host] \
    rojak/rojak-api:[tag]
```
