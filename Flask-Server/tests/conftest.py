import pytest

from timeswitch.server import prepare_app, create_db, app_setup

from tests.helper import Bunch

@pytest.fixture
def app_model(tmpdir):
    file = tmpdir.join("test_db.sqlite3").strpath
    dir = tmpdir.mkdir("test_static_dir").strpath
    cmd_args = Bunch(
        schedule_file=file,
        debug=True,
        static_dir=dir,
        create=True
    )
    app = prepare_app(cmd_args)
    create_db(app)
    model = app_setup(app)
    return (app, model)
