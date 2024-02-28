Open a shell, navigate to the directory containing these files, and start an HTTP server:

python -m http.server

Open a shell, navigate to the directory containing app.py, and start the server:

python app.py


Open another shell and run this command:

python -m websockets ws://localhost:8001/