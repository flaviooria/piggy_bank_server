import toml

if __name__ == "__main__":
    with open("pyproject.toml") as file:
        project = file.read()

    project_toml = toml.loads(project)

    print(project_toml["tool"]["poetry"]["version"])
