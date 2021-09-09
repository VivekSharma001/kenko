from website import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=80,host="0.0.0.0")