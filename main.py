from __init__ import create_app, db

app = create_app()
app.app_context().push()
db.create_all()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(port=8000, debug=True)

