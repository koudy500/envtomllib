FROM python

RUN pip install --upgrade pip
RUN pip install poetry

COPY . /var/envtoml
WORKDIR /var/envtoml

RUN poetry install --with dev

ENTRYPOINT ["poetry", "run"]
CMD ["pytest"]

