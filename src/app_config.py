from pathlib import Path
import typing as t

from pydantic import BaseModel, validator
from strictyaml import load, YAML

# Directories
APP_ROOT = Path(__file__).resolve().parent
DOCS_ROOT = APP_ROOT.parent.joinpath('docs/').resolve()
CONFIG_FILE_PATH = APP_ROOT.joinpath('conf/base/conf.yml').resolve()
EXT_STYLESHEETS_REL_PATH = ['.assets/bWlwgP.css']

class AppConfig(BaseModel):

    app_name: str
    app_title: str
    host: str
    port: int
    debug: bool

class LayoutConfig(BaseModel):
    banner_txt_color: str
    banner_bkg_color: str
    banner_width: str
    dash_bkg_color: str
    dash_txt_color: str
    plt_markers_color: str
    plt_markers_outliers_color: str
    plt_txt_color: str
    plt_paper_color: str
    plt_line_color: str
    plt_lim_line_color: str
    plt_lim_control_line: str
    plt_template_name: str

class DocumentationTabConfig(BaseModel):
    basics_on_cap_control_file: str
    doc_tab_width: str

class Config(BaseModel):
    app_config: AppConfig
    layout_config: LayoutConfig
    documentation_tab_config: DocumentationTabConfig

def find_config_file() -> Path:
    """Locate the configuration file."""
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"Config not found at {CONFIG_FILE_PATH!r}")


def fetch_config_from_yaml(cfg_path: Path = None) -> YAML:
    """Parse YAML containing the package configuration."""

    if not cfg_path:
        cfg_path = find_config_file()

    if cfg_path:
        with open(cfg_path, "r") as conf_file:
            parsed_config = load(conf_file.read())
            return parsed_config
    raise OSError(f"Did not find config file at path: {cfg_path}")


def create_and_validate_config(parsed_config: YAML = None) -> Config:
    """Run validation on config values."""
    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

    # specify the data attribute from the strictyaml YAML type.
    _config = Config(
        app_config=AppConfig(**parsed_config.data),
        layout_config=LayoutConfig(**parsed_config.data),
        documentation_tab_config=DocumentationTabConfig(**parsed_config.data),
    )

    return _config


config = create_and_validate_config()
