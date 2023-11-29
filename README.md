<p align="center">
    <a href="https://jhunufernandes.github.io/sthali-crud/images/crud.svg">
        <img src="https://jhunufernandes.github.io/sthali-crud/images/crud.svg" alt="SthaliCRUD" height="35%">
    </a>
    <em>A FastAPI package for CRUD operations</em>
</p>
<p align="center">
    <a href="https://pypi.org/project/sthali-crud/" target="_blank">
        <img src="https://img.shields.io/pypi/v/sthali-crud?label=Python%20Version&logo=python&color=%23ca5b32&logoColor=white" alt="">
    </a>
    <a href="https://github.com/jhunufernandes/sthali-crud/blob/main/docs/LICENSE" target="_blank">
        <img src="https://img.shields.io/github/license/jhunufernandes/sthali-crud?label=License&logo=opensourceinitiative&color=%23ca5b32&logoColor=white" alt="">
    </a>
</p>
<p align="center">
    <a href="https://github.com/jhunufernandes/sthali-crud/actions/workflows/test-package.yml" target="_blank">
        <img src="https://github.com/jhunufernandes/sthali-crud/actions/workflows/test-package.yml/badge.svg" alt="">
    </a>
    <a href="https://github.com/jhunufernandes/sthali-crud/actions/workflows/build-upload-pypi.yml" target="_blank">
        <img src="https://github.com/jhunufernandes/sthali-crud/actions/workflows/build-upload-pypi.yml/badge.svg" alt="">
    </a>
    <a href="https://github.com/jhunufernandes/sthali-crud/actions/workflows/build-upload-dockerhub.yml" target="_blank">
        <img src="https://github.com/jhunufernandes/sthali-crud/actions/workflows/build-upload-dockerhub.yml/badge.svg" alt="">
    </a>
    <a href="https://github.com/jhunufernandes/sthali-crud/actions/workflows/build-upload-ghcr.yml" target="_blank">
        <img src="https://github.com/jhunufernandes/sthali-crud/actions/workflows/build-upload-ghcr.yml/badge.svg" alt="">
    </a>
</p>

**Docs**: [https://jhunufernandes.github.io/sthali-crud/](https://jhunufernandes.github.io/sthali-crud/)

**PyPI**: [https://pypi.org/project/sthali-crud/](https://pypi.org/project/sthali-crud/)

**Source Code**: [https://github.com/jhunufernandes/sthali-crud/](https://github.com/jhunufernandes/sthali-crud/)

**Sthali Board**: [https://github.com/users/jhunufernandes/projects/4/](https://github.com/users/jhunufernandes/projects/4/)



---



## Requirements

Python >= 3.11
* [FastAPI](https://fastapi.tiangolo.com/)
* [TinyDB](https://tinydb.readthedocs.io/)
* [Pydantic](https://docs.pydantic.dev/latest/)
* [PyYAML](https://pypi.org/project/PyYAML/)



## Test

You can test this package alone by cloning the repo

```console
$ git clone https://github.com/jhunufernandes/sthali-crud/
...
config your env
...
(.venv)$ export ENV=DOCKER
(.venv)$ ./run.sh
```

or pulling the container.

```console
$ docker pull jhunufernandes/sthali-crud
$ export ENV=DOCKER
$ ./run.sh
```

#### Automatic API docs

Now go to [http://127.0.0.1:9000/docs](http://127.0.0.1:9000/docs). You will see the automatic interactive API documentation (provided by [Swagger UI](https://github.com/swagger-api/swagger-ui)).

#### Alternative API docs

And now, go to [http://127.0.0.1:9000/redoc](http://127.0.0.1:9000/redoc). You will see the alternative automatic documentation (provided by <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>).



## Usage

```console
$ pip install sthali-crud
```



## License

This project is licensed under the terms of the [MIT license](docs/LICENSE).
