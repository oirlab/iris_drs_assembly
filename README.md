# IRIS DRS Assembly
TMT-IRIS Data Reduction System Assembly

Testing on `irisdev`, a Virtual Machine setup by Chris with CSW services already preinstalled.

## Start and stop CSW services

    bash csw_start.sh

This saves logs in `logs/csw.log`, it needs about a minute
to start all services

    bash csw_stop.sh

## Preparing `iris_pipeline`

Make sure you have `iris_pipeline` installed, including the CRDS cache (it requires `git lfs`).

Download the input data:

    cd iris_drs_assembly
    python download_iris_data.py

Preprocess the flat frame:

    bash run_flat.sh

this should create the file `raw_flat_frame_flat.fits`.

## Start the DRS prototype

    cd iris_drs_assembly
    python DRSAssembly.py

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
bash launch_HCD.sh
```

We first need to have the Python component running, then once we launch
the Java component we can see the commands coming in looking through the logs
of the Python server.

## DRS Assembly receives command and executes `iris_pipeline`

The DRS Assembly receives via CSW services a command, currently it doesn't parse
the command parameters.
It just runs the [example pipeline](https://oirlab.github.io/iris-pipeline/example-run.html).

The Assembly should print out the logs of `stpipe` processing the data and create the output
file (a reduced science frame):

    test_iris_subtract_bg_flat_cal.fits

## Modify the Scala HCD

We can modify what commands the Scala HCD sends to Python:

https://github.com/tmtsoftware/pycsw/blob/7bf54d1883c5ad8e2276a26672e0c4c245fd3901/tests/testSupport/test-assembly/src/main/scala/org/tmt/csw/testassembly/TestAssemblyHandlers.scala#L253-L260
