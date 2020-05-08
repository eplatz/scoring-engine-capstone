# Scoring-engine-capstone

This scoring engine is to be used to practice for the Cyberpatriot competition. It is designed to work with the linux operating system.

# Running the Flask App
1. Install Python3, Python3-Pip, and Python3-venv
2. Make a directory for virtual environments and a sub-directory to run the Flask app
* Ex: ~/Environments/flask
3. Within the flask directory, initiate and activate a new virtual environment
* All packages required for the flask app will be installed within this virtual environment
* The flask app will be run from this virtual environment 
4. Installed required packages in virtual environment via pip3
* Flask
* Packaging 
5. Pull code from github into virtual environment directory 
* scoring-engine-app.py
* config.ini
* home.html
6. Run the flask app
* env FLASK_APP=scoring-engine-app.py FLASK_DEBUG=1 flask run
** Setting debug=1 will allow for debugging, which will display errors 
* Keep this terminal window open when running the app
7. View the flask app in a web browser
* 127.0.0.1:5000


## Built With

* [Python Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Packaging.version](https://packaging.pypa.io/en/latest/version/) - Python Module
* [OS](https://docs.python.org/3/library/os.html) - Python Module
* [PWD](https://docs.python.org/2/library/pwd.html) - Python Module
* [GRP](https://docs.python.org/2/library/grp.html) - Python Module
* [Subprocess](https://docs.python.org/3/library/subprocess.html) - Python Module
* [Configparser](https://docs.python.org/3/library/configparser.html) - Python Module

## Author

Emily Platz

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


