import os
from flask import Flask

def create_app(test_config=None):
    # Create the app.
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
    )

    from . import prediction 
    app.register_blueprint(prediction.bp)
    
    return app
