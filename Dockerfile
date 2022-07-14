FROM python:3.9

WORKDIR /code

COPY ../requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt && \
    groupadd -g 999 mediauser && \
    useradd -r -u 999 mediauser -g mediauser

COPY ../app /code/app

USER mediauser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]