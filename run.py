from lms_app import starter
from lms_app import db

if __name__ == "__main__":
    with starter.app_context():
        db.create_all()
    starter.run(debug=True)

