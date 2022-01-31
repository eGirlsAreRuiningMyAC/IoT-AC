# IoT-AC
App for a smart Air Conditioning device that makes use of IoT  

## DOCS
  - [Analysis document](docs/Document de analiză a cerințelor clientului.docx)
  - [OpenAPI spec file](docs/openapi.json)
  - [AsyncAPI spec file](docs/)

## INSTALLATION

Prerequisite: 
  - You should have python and pip installed.
  - For message broker: install and run [Mosquitto](https://mosquitto.org/download/) (keep default configurations).
    If you get ConnectionRefusedError when running the app, run cmd as admin, cd to Mosquitto file and try:   
    ```
    net start mosquitto
    ```


Running steps:
  1. Open CMD and cd in project folder
  
  2. Install venv, create an environment and activate the environment:  
  ```
    pip install virtualenv  
    python -m venv venv  
    venv\Scripts\activate.bat
  ```
    
  3. Install libraries/project requirements:  
  ```
    pip install -r requirements.txt
  ```
  4. Set environment value for development:  
  ```
    set FLASK_ENV=development
  ```
  5. (Re)Initialize database:   
  ```
    flask init_db
  ```
  6. Run project:   
  ```
    python my_app.py
  ```

## TESTING   
  ```
  pytest test_http.py
  pytest test_mqtt.py
  ```

## CREDITS
  - App based on official Flask tutorial: https://flask.palletsprojects.com/en/2.0.x/tutorial/
  - MQTT clients: https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
  - Weather data API : https://openweathermap.org/api
