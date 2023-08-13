# repo-harvester

Harvest information & documentation from repositories and images. Easily extensible to work with multiple Git & Image hosts. Store it all as linked data. 

## Tutorial
Prerequisites: Docker, (git if building from source)

The repo-harvester is built to collect information about mu-semtech repositories, into app-mu-info. This tutorial will show how to get a basic version up and running. It assumes a basic understanding of mu-semtech.

```yml
# docker-compose.yml
version: '3.4'

services:
  db:
    image: redpencil/virtuoso:feature-woodpecker-feature-builds
    environment:
      SPARQL_UPDATE: "true"
      DEFAULT_GRAPH: "http://mu.semte.ch/application"
    volumes:
      - ./data/db:/data
  harvester:
    image: repo-harvester
    ports:
      - "5000:80"  # Remove this in production
    links:
      - db:database
    volumes:
      - ./config:/usr/src/app/config
```

Now all you have to do is run the following commands:
```bash
docker-compose up  # Starts the stack
curl localhost:5000/init  # Populates the database
curl localhost:5000/update  # Updates the database
```

And that's it! However, if you wish, you can change the [repo/image sources](#changing-sources) and [categories](#changing-categories) of this app rather easily. For a production-ready example usage, view [app-mu-info](https://github.com/mu-semtech/app-mu-info).

## How to's
### Configuration through config/*.conf
- [repos.conf - Where to find repositores](#reposconf)
- [categories.conf - How to categorise the repositories](#categoriesconf)
- [overrides.conf - In case some of your repositories/images do not follow your other conventions](#overridesconf)

For all of these files, an example is provided in the [config/](config/) folder. You can apply the provided ones by simply removing `.example` from the filename.

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
| name/id     | type          | Link to code                                          | 
| ----------- | ------------- | ----------------------------------------------------- |
| GitHub      | Repositories  | [reposource/GitHub.py](reposource/GitHub.py)          |
| DockerHub   | Images        | [imagesource/DockerHub.py](imagesource/DockerHub.py)  |


#### categories.conf
For info on what categories are, please see the [discussions section](#categories)

Categories are defined as follows:
```conf
[templates]  # Section name, arbitrary
name=Templates  # Human readable name
id=templates  # id, will be used to generate a linked data url
regex=.*-template  # regex which will be ran against the repository name to check whether it's part of the category
```


The order in which you add them *does* matter, as every repo only has one category. If you add a category with a `.*` regex on the top of the file, it will subsequently match everything. Make sure to work down from most specific to less specific/catch-all.

#### overrides.conf
You can configure [overrides.conf](config/overrides.conf) in case you break your own Category naming convention, or want to archive specific repositories without changing anything in the repository itself.
The syntax is as follows:
```conf
[regex-.*-for-repo-name]
Category=tools  # Optional, reassigns to the category with specified 
ImageName=mu-login-service  # Optional, overrides the container image name for this repo
```

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
      - ./cache/:/tmp/repo-harvester/
    ports:
      - "5000:80"
    environment:
      MODE: "development"  # mu-python-template variable
      LOG_LEVEL: "debug"  # mu-python-template variable
      RH_CACHE: "True"  # Save requested API data to cache
      RH_PRINT: "True"  # Print to stdout
```
It is only intended to be used during development.


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

## Discussions
### Categories
Categories are arbitrary. We've added these because a lot of organisations - mu-semtech included - have a lot of different types of repos. More specifically, repos that are no longer in active use, as well as repos that are closely related to eachother. Categories allow you to categorise your repos in any way you want. See it as an html `data-` tag.

### Revisions
We've implemented revisions to allow easy traversal through current & past documentation.
However, there was no set way to define a revision. Using Image tags would be useless, as there are often projects with multiple images per release (alpine vs regular for example). Using GitHub releases would break this projects rule of being platform-independent. Using solely Git Tags could lead to a lack of relevant Image releases.

Thus revisions are found & added by the following logic: **if a Git tag has a *corresponding* image tag, it is counted as a revision.**


## License
This project is licensed under [the MIT License](LICENSE).
