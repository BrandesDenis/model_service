import importlib

from nc_service.model import MLModelLoader


def test__load_imports(mocker):
    mocker.patch('importlib.import_module')

    MLModelLoader('', ['test1', 'test2'])._load_imports()

    importlib.import_module.assert_called_with('test2')
    importlib.import_module.assert_called_with('test2')


def test__load_model(mocker):
    mocker.patch('joblib.load', return_value='test')

    ml_model = MLModelLoader('test', )

    assert ml_model._load_model().model == 'test'
