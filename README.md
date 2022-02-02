# IoT-AC
App for a smart Air Conditioning device that makes use of IoT  

## OVERVIEW

With this application, users can easily manipulate a smart Air Conditioning remotely, from the comfort of their personal devices.

The app offers users the possibility to create their own profiles. An user has the posibility to check information about the current temperature and humidity of the room, as well as set their own desired climatization. The smart device's operating hours can be scheduled. The app offers an auto operating mode based on current room temperature, as well as an auto cleaning mode based on a quality score that the device assigns to itself. Naturally, the users can create their own presets for temperature and humidity settings. Users can also make use of customizable audio alerts as well as adjustable device brightness, which can both be handled by an auto mode that adjusts them based on room noise and dimness respectively.

Because the health of a device should be monitored constantly, our app aims to ensure that users are well informed about the quality of their smart device by providing statistics related to usage history across all user profiles, as well as the maintenance/cleaning history of the device.

## FEATURES

- [x] User profiles (authentication)
- [x] Display temperature and humidity level
- [x] Create own Modes/Presets
    - [x] Auto Mode
    - [x] Schedule operating hours
    - [x] Info about the preset currently in use is displayed
- [x] Audio alerts
    - [x] Auto audio adjustment based on room noise
- [x] Customizable brightness
    - [x] Auto birghtness adjustment based on room dimness
- [x] Statistics about usage history across all user profiles
- [x] Display cleaning history
- [x] Self-cleaning mode - device goes into self-cleaning mode if self-assigned quality score falls under a certain threshold. all functions suspended until device is done cleaning

## FUTURE FEATURES

- [ ] Optimal settings suggestions based on the weather forcast
- [ ] Optimal settings recommendations based on usage history (with Machine Learning)


## DOCS
  - [Analysis document](https://github.com/eGirlsAreRuiningMyAC/IoT-AC/blob/main/docs/Document%20de%20analiz%C4%83%20a%20cerin%C8%9Belor%20clientului.docx)
  - [OpenAPI spec file](docs/openapi.yaml)
  - [AsyncAPI spec file](docs/asyncapi.yaml)

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
  You can check all tests by using:   
  ```
  pytest
  ```
  Or each type of tests by adding the name of the file:   
  ```
  pytest test_http_unit.py   
  pytest test_http_integration.py   
  pytest test_mqtt.py
  ```   

![MicrosoftTeams-image (2)](https://user-images.githubusercontent.com/62220895/152160951-95646626-b386-46d7-90c5-76bb7b18fc03.png)


  Automatically testing:
  - Follow these [instructions](https://github.com/microsoft/restler-fuzzer#local) to set up RESTler on local
  - cd to `restler` folder   
  - According to [docs](https://github.com/microsoft/restler-fuzzer/blob/main/docs/user-guide/Compiling.md), to generate the RESTler grammar and templates for other artifacts required for fuzzing, run:   
  ```
  restler.exe compile --api_spec <full path to API specification>
  ```    
  - According to [docs](https://github.com/microsoft/restler-fuzzer/blob/main/docs/user-guide/Testing.md), to invoke RESTler in test mode, run:     
  ```
  restler.exe test --grammar_file  ./Compile/grammar.py --dictionary_file ./Compile/dict.json --settings ./Compile/engine_settings.json --no_ssl
  ```
  
  
  Example:    
  ```
  restler.exe compile --api_spec C:/Users/Depanero/Desktop/Inginerie/IoT-AC/docs/openapi.yaml
  restler.exe test --grammar_file ./Compile/grammar.py --dictionary_file ./Compile/dict.json --settings ./Compile/engine_settings.json --no_ssl
    Starting task Test...
    Using python: 'python.exe' (Python 3.9.5)
    Request coverage (successful / total): 20 / 31
    No bugs were found.
    Task Test succeeded.
    Collecting logs...
  ```

## BUILT WITH
  - App based on official Flask tutorial: https://flask.palletsprojects.com/en/2.0.x/tutorial/
  - MQTT clients: https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
  - Weather data API : https://openweathermap.org/api
  - RESTler: https://github.com/microsoft/restler-fuzzer
  - Python: https://www.python.org/
  - Mosquitto: https://mosquitto.org/download/
