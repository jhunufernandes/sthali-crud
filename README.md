<p align="center">
    <a href="https://jhunufernandes.github.io/sthali-crud/images/crud.svg">
        <img src="https://jhunufernandes.github.io/sthali-crud/images/crud.svg" alt="SthaliCRUD" height=25%>
    </a>
    <em>A FastAPI package for CRUD operations</em>
</p>
<p align="center">
    <a href="https://pypi.org/project/sthali-crud" target="_blank">
        <img src="https://img.shields.io/pypi/v/sthali-crud?label=Version&color=%232EBC4F" alt="">
    </a>
    <a href="https://pypi.org/project/sthali-crud" target="_blank">
        <img src="https://img.shields.io/pypi/pyversions/sthali-crud.svg?label=Python&color=%232EBC4F" alt="">
    </a>
    <a href="https://pypi.org/project/sthali-crud" target="_blank">
        <img src="https://img.shields.io/github/license/jhunufernandes/sthali-crud?label=License&color=%232EBC4F" alt="">
    </a>
    <a href="https://github.com/jhunufernandes/sthali-crud/actions/workflows/test-package.yml" target="_blank">
        <img src="https://github.com/jhunufernandes/sthali-crud/actions/workflows/test-package.yml/badge.svg" alt="">
    </a>
    <a href="https://github.com/jhunufernandes/sthali-crud/actions/workflows/upload-package.yml" target="_blank">
        <img src="https://github.com/jhunufernandes/sthali-crud/actions/workflows/upload-package.yml/badge.svg" alt="">
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

or pulling our container

```console
$ docker pull jhunufernandes/sthali-crud
$ export ENV=DOCKER
$ ./run.sh
```

#### Automatic API docs

Now go to [http://127.0.0.1:9000/docs](http://127.0.0.1:9000/docs). You will see the automatic interactive API documentation (provided by [Swagger UI](https://github.com/swagger-api/swagger-ui)):

#### Alternative API docs

And now, go to [http://127.0.0.1:9000/redoc](http://127.0.0.1:9000/redoc). You will see the alternative automatic documentation (provided by <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):



## Usage

```console
$ pip install sthali-crud
```



## License

This project is licensed under the terms of the MIT license.
