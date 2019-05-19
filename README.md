# Hypersurfaces Software Development Challenge

# How to run

 1. build images
    ```
    docker-compose up
    ```
 2. load the data.json into db
    ```
    docker-compose run flaskapp python setup.py db
    ```
 3. go to
    [http://localhost](http://localhos)
 
 4. Integration Test - PyTest + Mock<br>
    Testing on flaskapp container is not possible due to a problem in the numpy module.
    I had no time to fix it. So you have to run the test on your machine.
    I also added a couple of fake wav file for testing purpose (ch-zero.wav, ch-invalid.wav).
    
    Be sure to have all the required modules running
    ```
    pip install -r requirements.txt
    ```
    Be sure to have all the containers up and running (the db must be initialized)
    ```
    docker-compose up
    ```
    Then run all tests through pytest
    ```
    pytest -r w --disable-pytest-warnings
    ```
    