from pathlib import Path
from unittest.mock import MagicMock, patch
import importlib.util
import requests
from click.testing import CliRunner

root = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('stage_app', root/'tile-based-classification/command-line-tools/stage-in/app.py')
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)

def test_download_http_error_does_not_write_zip():
    item = MagicMock()
    item.get_assets.return_value = {'PRODUCT': MagicMock(href='https://catalogue.example/product')}
    session = MagicMock()
    session.get.return_value.raise_for_status.side_effect = requests.HTTPError('unauthorized')
    with patch.object(app.requests, 'Session', return_value=session), patch('builtins.open') as opened:
        import pytest
        with pytest.raises(requests.HTTPError):
            app.download_and_extract_file(item, 'test-token')
        opened.assert_not_called()

def test_missing_token_fails_staging():
    with patch.dict(app.os.environ, {}, clear=True), patch.object(app.pystac, 'read_file'):
        result = CliRunner().invoke(app.stage, ['--input-item', 'https://example/item'])
        assert result.exit_code != 0
        assert 'CDSE_ACCESS_TOKEN' in result.output

def test_workflow_passes_correct_token_variable():
    import yaml
    document = yaml.safe_load((root/'cwl-workflow/stage-and-cog.cwl').read_text())
    tool = next(p for p in document['$graph'] if p['id'] == 'stage-in')
    assert tool['requirements']['EnvVarRequirement']['envDef']['CDSE_ACCESS_TOKEN'] == '$(inputs.access_token)'


def test_staging_declares_required_network_access():
    import yaml
    document = yaml.safe_load((root/'cwl-workflow/stage-and-cog.cwl').read_text())
    tool = next(p for p in document['$graph'] if p['id'] == 'stage-in')
    assert tool['requirements']['NetworkAccess']['networkAccess'] is True
