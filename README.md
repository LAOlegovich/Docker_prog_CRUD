# Docker_prog_CRUD
## Описание процесса создания образа и запуска контейнера 
### Выполнить в powershell команду: docker build --tag=image_crud . (создание образа)
##### Примечание: в конце команда стоит точка, т.к. докерфайл лежит в корне каталога
### Выполнить в powershell команду: docker run -d --name=crud_container -p 8088:7777 image_crud (запуск контейнера)

### Http-запросы формируется через REST Client (файл requests-examples.http)
