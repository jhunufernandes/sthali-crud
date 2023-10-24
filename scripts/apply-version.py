def get_branch() -> str:
    git_head_relative_path = ".git/HEAD"
    with open(git_head_relative_path, encoding="utf-8") as _file:
        head_content = _file.read().splitlines()[0]
    branch_version = head_content.split("/")[-1]
    return branch_version


def replace_pyproject_version(pyproject_path: str, version: str) -> None:
    def read_file(file_path: str) -> list[str]:
        with open(file_path, encoding="utf-8") as _file:
            return _file.readlines()

    def replace_version(lines: list[str], version: str) -> list[str]:
        for i, line in enumerate(lines):
            if line.startswith('version = "'):
                lines[i] = f'version = "{version}"\n'
        return lines

    def write_file(file_path: str, lines: list[str]) -> None:
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(lines)

    write_file(pyproject_path, replace_version(read_file(pyproject_path), version))


if __name__ == "__main__":
    PYPROJECT_PATH = "./pyproject.toml"
    new_version = get_branch()
    replace_pyproject_version(PYPROJECT_PATH, new_version)
