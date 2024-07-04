from lifegiver import create_app

app = create_app()

# run
if __name__ == "__main__":
    app.run(debug=True)
