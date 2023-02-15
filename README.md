# repo-harvester

Harvest information from repositories and images.

## How to
### Use in docker-compose (recommended)
```yaml
services:
    # ...
    harvester:
        image: semtech/repo-harvester
        # Below is optional; mainly useful in dev environments
        ports:
            - "5000:80"
        volumes:
            - ../repo-harvester/:/app
            - ../cache/:/usr/src/app/cache/Tailwind
        environment:
            MODE: "development"
            LOG_LEVEL: "debug"
```
For example usage, check out [app-mu-info](https://github.com/mu-semtech/app-mu-info)


### Build & run the image locally
Prerequisites: 
```bash
git clone https://github.com/mu-semtech/repo-harvester.git
cd repo-harvester
docker build -t repo-harvester .
docker run -p 80:80 repo-harvester
```


## Reference
Please also check the docstrings and typing included in the code!

For the model which this service uses, check [the reference in mu-app-info](https://github.com/mu-semtech/app-mu-info#reference).

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
