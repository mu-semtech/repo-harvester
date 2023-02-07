# repo-harvester

Harvest information from repositories and images.

## How to
### Run locally
```bash
export FLASK_APP=web.py
flask run
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
