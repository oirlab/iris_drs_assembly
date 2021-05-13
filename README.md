# IRIS DRS Assembly
TMT-IRIS Data Reduction System Assembly

Testing on `irisdev`, a Virtual Machine setup by Chris with CSW services already preinstalled.

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

## Build and launch Scala HCD to launch commands

Following instructions at:

<https://github.com/tmtsoftware/pycsw/tree/master/tests>

```
source configure_env.sh
cd pycsw/tests/
cd testSupport
sbt stage
test-deploy/target/universal/stage/bin/test-container-cmd-app --local test-deploy/src/main/resources/TestContainer.conf
```

We first need to have the Python component running, then once we launch
the Java component we can see the commands coming in looking through the logs
of the Python server.

### Modify the Scala HCD

We can modify what commands the Scala HCD sends to Python:

https://github.com/tmtsoftware/pycsw/blob/7bf54d1883c5ad8e2276a26672e0c4c245fd3901/tests/testSupport/test-assembly/src/main/scala/org/tmt/csw/testassembly/TestAssemblyHandlers.scala#L253-L260
