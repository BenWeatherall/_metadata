import re
import asyncio
import aiofiles
from pathlib import Path
from typing import List, Tuple
import yaml

from pymeta.models.config import Config
from pymeta.models.env_var import EnvVar, EnvironVar, GetEnvVar

environ_pattern = re.compile(r'environ\[[\n\r\s]*[\'"](.*?)[\'"][\n\r\s]*\]')
getenv_pattern = re.compile(r'getenv\([\n\r\s]*[\'"]+(.*?)[\'"][\n\r\s]*(?:,[\n\r\s]*[\'"]*(.*?)[\'"]*[\n\r\s]*\)|\))')

def generate_env_report(project_path: Path, metadata_folder: Path, config: Config):
    project_env_variables = asyncio.run(
        find_environment_variables(
            project_path=project_path,
            config=config
        )
    )

    variables = {}
    files = {}
    for path, env_vars in project_env_variables:
        file_path = str(path)
        files[file_path] = []
        for env_var in env_vars:
            if env_var.name not in files[file_path]:
                files[file_path].append(env_var.name)

            if env_var.name not in variables:
                variables[env_var.name] = []

            details = {
                'file': file_path,
                'is_required': env_var.is_required,
            }

            if env_var.has_default:
                details['default'] = env_var.default

            variables[env_var.name].append(details)


    with open(metadata_folder / "env_vars.yml", "w+") as f:
        f.write(yaml.safe_dump(variables))

    with open(metadata_folder / "env_var_files.yml", "w+") as f:
        f.write(yaml.safe_dump(files))

async def find_env_vars(parent_path: Path, file_path: Path) -> Tuple[Path, List[EnvVar]]:
    variables = []
    file_local_path = file_path.relative_to(parent_path)
    try:
        async with aiofiles.open(file_path, mode='r') as f:
            content = await f.read()
            content.replace("\n", " ")

            # environ matches (single match, no default value)
            matches = environ_pattern.findall(content)
            variables.extend([EnvironVar(name=match) for match in matches])

            # getenv matches
            matches = getenv_pattern.findall(content)
            variables.extend([GetEnvVar(name=match[0], default=match[1] if len(match) > 1 else None, is_required=False) for match in matches])

            return file_local_path, variables
    except Exception as e:
        print(f"Error reading file: {file_path}")
        print(e)
        return file_local_path, []

async def find_environment_variables(project_path: Path, config: Config):
    assert project_path.exists(), f"{project_path} does not exist"

    full_path_list = project_path.rglob("*.py")

    pathlist = []

    for path in full_path_list:
        if not config.include_venv and ".venv" in str(path):
            continue
        else:
            pathlist.append(path)

    tasks = [find_env_vars(parent_path=project_path, file_path=path) for path in pathlist]
    results = await asyncio.gather(*tasks)

    results = [result for result in results if result[1]]

    return results
