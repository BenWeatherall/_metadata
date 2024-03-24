from pathlib import Path
import argparse

import yaml

from pymeta.models.config import Config
from pymeta.helpers.project_directories import get_project_directories
from pymeta.helpers.environment_vars import generate_env_report

def get_metadata_folder(path: Path, output_folder: Path) -> Path:
    output_path = path / output_folder

    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)

    return output_path

def load_metadata_config(path: Path) -> Config:
    config_path = path / "config.yml"

    if not config_path.exists():
        with open(config_path, "w+") as f:
            f.write(yaml.safe_dump(Config().model_dump()))

    with open(config_path, "r") as f:
        config = Config(**yaml.safe_load(f))

    return config

def main():
    parser = argparse.ArgumentParser(
        description="Generate metadata for a project"
    )
    parser.add_argument("-path", help="Path to target project", type=Path)
    parser.add_argument("-output_folder", help="Project metadata folder. Default = .metadata/", type=Path, default=Path(".metadata"))
    parser.add_argument("-recursive", help="Recursively search for projects within target directory", action="store_true", default=False)
    args = parser.parse_args()

    project_path = args.path

    if args.recursive:
        project_paths = get_project_directories(project_path)
    else:
        project_paths = [project_path]

    for project_path in project_paths:
        print(project_path)
        metadata_folder = get_metadata_folder(project_path, args.output_folder)
        config = load_metadata_config(metadata_folder)
        generate_env_report(project_path, metadata_folder, config)







if __name__ == "__main__":
    main()
