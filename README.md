# collect-media-service
All commands should be execute next commands from root project directory.

### Set up a local development environment:
````
    docker build --tag collect-media .
    docker-compose -f docker-compose.yml up -d
````
### If you don't need a separate container for collect-media-service:
1. ```` cp docker-compose.yml backup.docker-compose.yml ````
2. Remove section "app" from docker-compose.yml.
3. ```` cp config.yaml backup.config.yaml ````
4. Replaced all hostnames in config.yml with "127.0.0.1".
5. Execute next commands from root project directory:
6. ```` docker-compose -f docker-compose.yml up -d ````
7. ```` python3 -m venv .venv ```` use python 3.9
8. ```` source .venv/bin/activate ````
9. ```` pip install -r requrements ````
10. ```` uvicorn api.images:app --reload ````