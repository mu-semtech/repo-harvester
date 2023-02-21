# repo-harvester

Harvest information from repositories and images. Easily extensible to work with multiple Git & Image hosts. Store it all as linked data. 

## How to
Prerequisites: Docker, git*
*if building from source

### Use in docker-compose (recommended)
```yaml
services:
    # ...
    harvester:
        image: semtech/repo-harvester
        # Below is optional; mainly useful in dev environments
        ports:
            - "5000:80"
        environment:
            MODE: "development"
            LOG_LEVEL: "debug"
```
For example usage, check out [app-mu-info](https://github.com/mu-semtech/app-mu-info)


### Build & run the image locally
```bash
git clone https://github.com/mu-semtech/repo-harvester.git
cd repo-harvester
docker build -t repo-harvester .
docker run -p 80:80 repo-harvester
```


## Reference
Please also check the docstrings and typing included in the code!

For the model which this service uses, check [the reference in mu-app-info](https://github.com/mu-semtech/app-mu-info#reference).


### Structure
- [imagesource/](imagesource/): Code to handle image sources (e.g. Docker Hub)
    - [Imagesource.py](imagesource/Imagesource.py): The base class for image sources. This allows the rest of the code to work no matter what source is used.
    - [DockerHub.py](imagesource/DockerHub.py): The class for the Docker Hub image source. All Docker Hub specific code should be in here.
- [reposource/](reposource/): Code to handle repository soruces (e.g. GitHub, Gitea...)
    - [Reposource.py](reposource/Reposource.py): The base class for repo sources. This allows the reset of the code to work no matter what source is used.
    - [GitHub.py](reposource/GitHub.py): The class for the GitHub repo source. All GitHub specific code should be in here.
- [categories.py](categories.py): Defines & handles categories to sort the repositories in. These are arbitrary and user-defined.
- [Dockerfile](Dockerfile): Dockerfile for the microservice.
- [overrides.conf](overrides.conf): Configure overrides for repositories. Whether it be about their Category or Image source.
- [overrides.py](overrides.py): Code to handle overrides.conf.
- [Repo.py](Repo.py): Repo & Revision classes.
- [request.py](request.py): Tools for requesting & caching data.
- [sparql.py](sparql.py): Code that stores collected data into a triplestore through SPARQL.
- [web.py](web.py): Entrypoint, a Flask app.

### overrides.conf
You can configure [overrides.conf](overrides.conf) in case you break your own Category naming convention, or want to archive specific repositories without changing the git repository.
The syntax is as follows:
```conf
[regex-.*-for-repo-name]
Category=tools  # Optional, reassigns to the category with specified 
ImageName=mu-login-service  # Optional, overrides the container image name for this repo
```

## License
This project is licensed under [the MIT License](LICENSE).
