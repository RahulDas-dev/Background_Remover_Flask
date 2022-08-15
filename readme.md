
# Selfie Image Background App with Flask  + React
![flask-logo](https://www.vectorlogo.zone/logos/pocoo_flask/pocoo_flask-ar21.svg) ![react](https://www.vectorlogo.zone/logos/reactjs/reactjs-ar21.svg)


### Project Directory Strructre
1. database - contains sqlite3.db file Will not be needed for production DB.
2. image_store - uploaded and generated images store.
3. src - main source code.
4. static - html, css, Js files or react build.
5. trained_model - ML model for image background removal.

### Create virtual Environment or use [the link](https://gist.github.com/RahulDas-dev/4324ec7d7f60ff49efd33180c33e6a28) for help.

### Download The Pretained Model Files[onnx] from below Link.

* [Light weight model](https://drive.google.com/uc?id=1tNuFmLv0TSNDjYIkjEdeH1IWKQdUA4HR) md5 = "8e83ca70e441ab06c318d82300c84806"

* [Reguler model ](https://drive.google.com/uc?id=1tCU5MM1LhRgGou5OpmpjBQbSrYIUoYab) md5 = "60024c5c889badc19c04ad937298a77b"

* Place the downloaded model files in `trained_model` directory

### To run the app 
* Set `set FLASK_DEBUG=1` for DEBUG Mode and set `set FLASK_DEBUG=0` for production mode
* Set App Name `set FLASK_APP=run.py`
* Run  `flask run --host 0.0.0.0 --port 5000` from cmd
* Finally point ur browser to `localhost:5000/`


### Some Optional Steps for development

* Run Linter form cmd using `flake8 --config .flake8 . -v`
* Code Formating form cmd using `black . -v`
* For Cleaning run `pyclean -v . & black -v .` [ Deletes __pycacche__ files]


### React UI [repository](https://github.com/RahulDas-dev/-Background_Remover_React.git) 


### Future Development needs to be done

    1. Logging

