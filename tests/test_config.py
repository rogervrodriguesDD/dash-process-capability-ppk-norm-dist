from pathlib import Path
import pytest
from pydantic import ValidationError

from src.app_config import ( create_and_validate_config,
                            fetch_config_from_yaml)

TEST_CONFIG_TEXT = """
# App config
app_name: dash_process_capability_ppk_norm_dist
app_title: Report for Process Capability Index (PPK)
host: 0.0.0.0
port: 8080
debug: False

# Layout config
banner_bkg_color: "#004c6d"
banner_txt_color: "#F1F1F1"
banner_width: "100%"
dash_bkg_color: "#F1F1F1"
dash_txt_color: "#7E909A"
plt_markers_color: "#004c6d"
plt_markers_outliers_color:  "#AC3E31"
plt_txt_color: "#202020"
plt_paper_color: "#7E909A"
plt_line_color: "#00f5ff"
plt_lim_line_color: red
plt_average_line:  "#000000"

plt_lim_line_dash: longdash
plt_average_line_dash: solid

plt_control_chart_width: 1400
plt_control_chart_height: 400
plt_full_report_width: 1400
plt_full_report_height: 400

plt_template_name: seaborn

# Documentation tab config
basics_on_cap_control_file: 'basics_on_cap_control.md'
doc_tab_width: '50%'
"""

INCOMPLETE_CONFIG_TEXT = """
app_name: dash_process_capability_ppk_norm_dist
"""

class TestConfiguration(object):

    def test_fetch_config_structure(self, tmpdir):

        # Writting a tmp file (pytest built-in tmpdir fixture)
        configs_dir = Path(tmpdir)
        config_1 = configs_dir / "sample_config.yml"
        config_1.write_text(TEST_CONFIG_TEXT)
        parsed_config = fetch_config_from_yaml(cfg_path=config_1)

        # Creating the config object
        config = create_and_validate_config(parsed_config=parsed_config)

        assert config.app_config
        assert config.layout_config
        assert config.documentation_tab_config

    def test_missing_config_field_raises_error(self, tmpdir):

        # Writting a tmp file (pytest built-in tmpdir fixture)
        configs_dir = Path(tmpdir)
        config_1 = configs_dir / "sample_config.yml"
        config_1.write_text(INCOMPLETE_CONFIG_TEXT)
        parsed_config = fetch_config_from_yaml(cfg_path=config_1)

        # Creating the config object (Validation error expected)
        with pytest.raises(ValidationError) as excinfo:
            create_and_validate_config(parsed_config=parsed_config)

        assert "field required" in str(excinfo.value)
        assert "host" in str(excinfo.value)
        assert "port" in str(excinfo.value)
        assert "debug" in str(excinfo.value)
