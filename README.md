# Настройка проекта
    pip install -r requrements.txt
    cp config.dist.yaml config.yaml
    docker-compose -f tests/docker-compose.yml up -d

## Запуск для разработки
```shell
uvicorn api.images:app --reload
```