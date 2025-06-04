import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '3DPrintSystem'))
from app import create_app
from app.routes.dashboard import _move_file_between_status_dirs


def test_move_file_updates_metadata_path(tmp_path):
    os.environ['SECRET_KEY'] = 'test'
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    os.environ['STAFF_PASSWORD'] = 'pass'

    app = create_app()
    app.config['APP_STORAGE_ROOT'] = str(tmp_path)
    app.config['UPLOAD_FOLDER'] = str(tmp_path / 'Uploaded')

    upload_dir = Path(app.config['UPLOAD_FOLDER'])
    upload_dir.mkdir(parents=True)
    pending_dir = Path(app.config['APP_STORAGE_ROOT']) / 'Pending'
    pending_dir.mkdir()

    test_file = upload_dir / 'model.stl'
    test_file.write_text('data')
    meta_file = upload_dir / 'model.metadata.json'
    meta_file.write_text('{}')

    with app.app_context():
        new_file, new_meta = _move_file_between_status_dirs(str(test_file), 'Uploaded', 'Pending')

    assert Path(new_file).exists()
    assert Path(new_meta).exists()
    assert Path(new_file).parent == pending_dir
    assert Path(new_meta).parent == pending_dir
