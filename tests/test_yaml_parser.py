import pytest
from utils.yaml_parser import parse_yaml_file
import yaml
import os

# Sample YAML content for testing
sample_yaml_content = """
- name: endpoint 1
  url: https://example.com
  method: GET
- name: endpoint 2
  url: https://another-example.com
  headers:
    user-agent: test-agent
"""

@pytest.fixture
def tmp_yaml_file(tmp_path):
    """Creates a temporary YAML file for testing."""
    file_path = tmp_path / "test_config.yaml"
    with open(file_path, 'w') as f:
        f.write(sample_yaml_content)
    return file_path

def test_parse_yaml_file_success(tmp_yaml_file):
    parsed_data = parse_yaml_file(tmp_yaml_file)
    assert isinstance(parsed_data, list)
    assert len(parsed_data) == 2
    assert parsed_data[0]['name'] == 'endpoint 1'

def test_parse_yaml_file_not_found():
    with pytest.raises(SystemExit):
        parse_yaml_file("non_existent_file.yaml")

def test_parse_yaml_file_invalid_yaml(tmp_path):
    invalid_yaml_path = tmp_path / "invalid.yaml"
    with open(invalid_yaml_path, 'w') as f:
        f.write("invalid: [unclosed_list")

    with pytest.raises(SystemExit):
        parse_yaml_file(invalid_yaml_path)
