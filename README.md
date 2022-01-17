# TimeReleaseClient
## TimeReleaseClient is NexToken's Centralized Client System

## Flask Backend

## Directories
* frontend - React app using for show datasets
* Time-Release-Blockchain - Time release submodule using in SQLAlchemy operations

## Files in Root Dir
* app.py - the Flask app to provide web service for frontend react app.
if running the Flask app with an ip and port, please use below shell script.
```shell
    python3 -m flask run --host=127.0.0.1 --port=5000
   ```
* client_config.py - default configuration settings for current app and postgreSQL, you may add your customize configurations
* dbmodel.py - models and keys defines for Block、Transaction and so on
* decrypt_tools - tools for decrypting time release msg
* model_tools - generate block and transaction model for operation

### Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Frontend Scripts

In the project's frontend directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

# venv script
```shell
source ./venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ deactivate
```

# Crpyto import error notice:
If you have installed pycryptodome as requirements.txt file show.
Then you also have an error like 'No Module Found 'Crypto'',
You should find your external lib,and find crypto.
Refactor 'crypto' to 'Crypto',that will be ok.


