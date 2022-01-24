# IoT-AC
App for a smart Air Conditioning device that makes use of IoT  

## DOCS
  - OpenAPI specification
  - MQTT specification
  - Documentation
  - Analysis document

## INSTALLATION

Prerequisite: 
  - You should have python and pip installed.
  - For message broker: install and run [Mosquitto](https://mosquitto.org/download/) (keep default configurations).


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
    flask init-db
  ```
  6. Run project:   
  ```
    python app.py
  ```

## CREDITS
  - App based on official Flask tutorial: https://flask.palletsprojects.com/en/2.0.x/tutorial/
  - MQTT clients: https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
  - Weather data API : https://openweathermap.org/api
