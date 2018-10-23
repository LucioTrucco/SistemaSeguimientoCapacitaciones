from app import app, db
from app.models import User, Training, Class


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Training': Training, 'Class': Class}
