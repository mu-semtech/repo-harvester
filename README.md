# repo-harvester

Harvest information & documentation from repositories and images. Easily extensible to work with multiple Git & Image hosts. Store it all as linked data. 

## Tutorial (getting started)
The repo-harvester is built to collect information about mu-semtech repositories, into app-mu-info. This tutorial will show how to get a basic version up and running. It assumes a basic understanding of mu-semtech.

```yml
# docker-compose.yml
version: '3.4'

services:
  dispatcher:
    image: semtech/mu-dispatcher:1.1.2
    links:
      - resource:resource
    volumes:
      - ./config/dispatcher:/config
  db:
    image: redpencil/virtuoso:feature-woodpecker-feature-builds
    environment:
      SPARQL_UPDATE: "true"
      DEFAULT_GRAPH: "http://mu.semte.ch/application"
    volumes:
      - ./data/db:/data
  resource:
    image: semtech/mu-cl-resources:1.17.1
    links:
      - db:database
    volumes:
      - ./config/resources:/config
  harvester:
    image: repo-harvester
    ports:
      - "5000:80"  # Remove this in production
    links:
      - db:database
```

Optionally, you can clone this repository and [enable development mode](#enable-development-mode).

Now all you have to do is run the following commands:
```bash
docker-compose up  # Starts the stack
curl localhost:5000/init  # Populates the database
curl localhost:5000/update  # Updates the database
```

And that's it! However, if you wish, you can change the [repo/image sources](#changing-sources) and [categories](#changing-categories) of this app rather easily.


## How to's
Prerequisites: Docker, (git if building from source)

### Use in docker-compose
```yaml
services:
    # ...
    harvester:
        image: semtech/repo-harvester
        links:
          - db:database
    # ...
```

For example usage, check out [app-mu-info](https://github.com/mu-semtech/app-mu-info)

### Enable development mode
Thanks to [mu-python-template](https://github.com/mu-semtech/mu-python-template#development-mode), you can mount the following volumes to save cache, as well as enable live-reload.
```yaml
version: '3.4'

services:
  # ...
  harvester:
    # ...
    volumes:
      - /path/to/repo-harvester/:/app
      - cache/:/usr/src/app/cache/
    ports:
      - "5000:80"
    environment:
      MODE: "development"
      LOG_LEVEL: "debug"
```
Caching is only enabled when MODE is set to development, and will not auto-clear. It is only intended to be used during development.

### Configuration through config/*.conf
For all of these files, an example is provided in the [config/](config/) folder. You can apply them by simply removing `.example` from the filename.

They can also be loaded in through docker-compose. See [app-mu-info/docker-compose.yml](https://github.com/mu-semtech/app-mu-info/blob/master/docker-compose.yml) for an example.

#### repos.conf
```conf
[mu-semtech GitHub + DockerHub]  # Section name, arbitrary
repos_host=GitHub  # Host on which the repos are hosted. Case-insensitive
repos_username=mu-semtech  # Username/org name on the repos' host
images_host=DockerHub  # Host on which the repos' relevant iamges are hosted. Case-insensitive
images_username=semtech  # Username/org name on the images' host
```

Currently supported hosts are:
| name/id     | type          | Link to code                                          | notes       |    
| ----------- | ------------- | ----------------------------------------------------- | ----------- |
| GitHub      | Repositories  | [reposource/GitHub.py](reposource/GitHub.py)          | Default     |
| DockerHub   | Images        | [imagesource/DockerHub.py](imagesource/DockerHub.py)  | Default     |



#### categories.conf
For info on what categories are, please see the [discussions section](#categories)

Categories are defined as follows:
```conf
[templates]  # Section name, arbitrary
name=Templates  # Human readable name
id=templates  # id, will be used to generate a linked data url
regex=.*-template  # regex which will be ran against the repository name to check whether it's part of the category
```


The order in which you add them *does* matter. If you add a category with a `.*` regex on the top of the file, it will subsequently match everything. Make sure to work down from most specific to less specific/catch-all.

#### overrides.conf
You can configure [overrides.conf](config/overrides.conf) in case you break your own Category naming convention, or want to archive specific repositories without changing anything in the repository itself.
The syntax is as follows:
```conf
[regex-.*-for-repo-name]
Category=tools  # Optional, reassigns to the category with specified 
ImageName=mu-login-service  # Optional, overrides the container image name for this repo
```


### Build & run the image locally
```bash
git clone https://github.com/mu-semtech/repo-harvester.git
cd repo-harvester
docker build -t repo-harvester .
docker run -p 80:80 repo-harvester
```


## Reference
Please also check the docstrings and typing included in the code!

For the model which this microservice uses, check [the reference in mu-app-info](https://github.com/mu-semtech/app-mu-info#reference).


### Structure
- [imagesource/](imagesource/): Code to handle image sources (e.g. Docker Hub)
    - [Imagesource.py](imagesource/Imagesource.py): The base class for image sources. This allows the rest of the code to work no matter what source is used.
    - [DockerHub.py](imagesource/DockerHub.py): The class for the Docker Hub image source. All Docker Hub specific code should be in here.
- [reposource/](reposource/): Code to handle repository sources (e.g. GitHub, Gitea...)
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


## Discussions
### Categories
Categories are arbitrary. We've added these because a lot of organisations - mu-semtech included - have a lot of different types of repos. More specifically, repos that are no longer in active use, as well as repos that are closely related to eachother. Categories allow you to categorise your repos in any way you want. See it as an html `data-` tag.

### Revisions
We've implemented revisions to allow easy traversal through current & past documentation.
However, there was no set way to define a revision. Using Image tags would be useless, as there are often projects with multiple images per release (alpine vs regular for example). Using GitHub releases would break this projects rule of being platform-independent. Using solely Git Tags could lead to a lack of relevant Image releases.

Thus revisions are found & added by the following logic: **if a Git tag has a *corresponding* image tag, it is counted as a revision.**


## License
This project is licensed under [the MIT License](LICENSE).
