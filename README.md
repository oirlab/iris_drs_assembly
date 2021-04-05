# IRIS DRS Assembly
TMT-IRIS Data Reduction System Assembly

## Start and stop CSW services

    bash csw_start.sh

This saves logs in `logs/csw.log`, it needs about a minute
to start all services

    bash csw_stop.sh

## Start example command server in Python

    python example_command/TestCommandServer.py

This will start this service and print out:

```
Registering with location service using port 8082
Starting test command server on port 8082
======== Running on http://0.0.0.0:8082 ========
(Press CTRL+C to quit)
```
