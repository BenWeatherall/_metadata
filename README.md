# pymeta

A Python package to identify and analyze Python program metadata including required environment variables, packages, and more.

## Description

pymeta scans Python projects to extract and report on metadata such as:
- Environment variables used in the code
- Project directory structure
- Configuration management

This tool is useful for documentation, dependency management, and understanding Python project requirements.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/pymeta.git
cd pymeta

# Install the package
pip install -e .

# For development
pip install -e ".[development]"

# For testing
pip install -e ".[testing]"
```

## Requirements

- Python 3.9 or higher
- Dependencies:
  - PyYAML
  - pydantic
  - aiofiles

## Usage

### Basic Usage

```bash
python -m pymeta.main -path /path/to/your/project
```

### Options

- `-path`: Path to target project
- `-output_folder`: Project metadata folder (Default: `.metadata/`)
- `-recursive`: Recursively search for projects within target directory

### Example

```bash
# Generate metadata for a single project
python -m pymeta.main -path ./my_project

# Generate metadata recursively for multiple projects
python -m pymeta.main -path ./projects_directory -recursive
```

## Output Examples

When run against a project, pymeta generates multiple YAML files in the designated metadata folder:

### Example 1: Project with Environment Variables

After running pymeta on a project with environment variables, the following metadata files are generated:

**config.yml**
```yaml
include_venv: false
```

**env_vars.yml** (Lists all environment variables with details)
```yaml
API_KEY:
- default: null
  file: src/publish/confluence.py
  is_required: false
DATAFORM_ASSERTIONS_PUB:
- file: utils/commit-assertions/commit_assertions/main.py
  is_required: true
DATAFORM_ASSERTIONS_SSH:
- file: utils/commit-assertions/commit_assertions/main.py
  is_required: true
```

**env_var_files.yml** (Maps files to their used environment variables)
```yaml
src/publish/confluence.py:
- API_KEY
utils/commit-assertions/commit_assertions/main.py:
- DATAFORM_ASSERTIONS_SSH
- DATAFORM_ASSERTIONS_PUB
```

### Example 2: Project with No Environment Variables

For projects without environment variables, the output is minimal:

**env_vars.yml**
```yaml
{}
```

**env_var_files.yml**
```yaml
{}
```

## Features

- **Environment Variable Detection**: Identifies environment variables used in your Python code
- **Project Structure Analysis**: Maps directory structures and relationships
- **Configuration Management**: Reads and generates configuration files for your projects
- **Recursive Analysis**: Can analyze multiple projects in a directory structure

## Development

```bash
# Install development dependencies
pip install -e ".[development]"

# Run tests
pytest
```

## License

MIT License

## Author

Ben Weatherall
