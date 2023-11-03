import os
from pathlib import Path


def getMainFolderPath() -> Path:
    return Path(os.path.dirname(os.path.realpath(__file__))).parent


def getDockerComposeReference():
    return getMainFolderPath() / 'docker-compose.yml'


def __main():
    main_folder = getDockerComposeReference()
    print(main_folder)
    return


if __name__ == '__main__':
    __main()
