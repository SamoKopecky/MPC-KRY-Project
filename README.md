# MPC-KRY-Projekt

## FileSending
- spustenie z `./app.py`
- treba vygenerovat certifikaty so skriptom v zlozke `certs` pre 2 mena
- pri spustati programu je potrebne zadat rovnake mena ako pri vytvarani certifikatov

Header format:

| HEADER_START | FILE_LENGHT [64bit] | FILE_NAME | HEADER_END | DATA | DATA_END | FIN |
|:------------:|:-------------------:|:---------:|:----------:|:----:|:--------:|:---:|
