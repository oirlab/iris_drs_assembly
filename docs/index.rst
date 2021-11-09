IRIS-TMT Data Reduction System Assembly
=======================================

The IRIS Data Reduction System (DRS) Assembly is a software component to be deployed at
the Thirty Meter Telescope observatory to manage the real-time reduction of IRIS data.
The role of the Assembly is to receive commands, gather telemetry, configure and launch
the data reduction pipeline implemented as a separate package: `iris_pipeline <https://github.com/oirlab/iris_pipeline>`_.

Architecture
------------

.. figure:: _static/architecture.png
    :width: 700
    :alt: Flowchart of the architecture of the DRS Assembly at the TMT Observatory

    Architecture of the deployment of the DRS Assembly and the rest of the IRIS instrument at the TMT Observatory

See the figure above for a chart of the system architecture, the DRS Assembly is a Python service which is always in execution on the Pipeline computer at the TMT Observatory and is in charge of subscribing to the events stream of the Common Software (CSW).
Once it receives the command of starting acquisition it signals to the Python processing pipeline to start to monitor the disk for raw science frames coming from the Readout disk.

The `iris_pipeline` Python process, once properly configured with the right parameters for the current observing mode, will process the input raw science frames into reduced science frames, it will also connect to the TMT Data Management System (DMS) to get the necessary calibration files. It will also have a local cache for the most commonly used calibration files.

`iris_pipeline` will include all the processing modules necessary to assemble the imager and the spectrograph pipelines.

Once the pipelines have completed execution, they will write the output FITS files to the Reduced disk. At this point the DRS Assembly can publish the event of "execution completed".

DRS Assembly Design
-------------------

TMT has released a Python interface to the Observatory middleware CSW, named PyCSW and published `on Github <https://github.com/tmtsoftware/csw-python>`_.
`PyCSW` is based on Python async co-routines to handle asynchronous commands and execute background processes.

We implemented a proof-of-concept DRS Assembly in Python relying on PyCSW in the `oirlab/iris_drs_assembly repository on Github <https://github.com/oirlab/iris_drs_assembly>`_, it is currently capable of accepting a command from a Scala component via CSW and then execute in a long-running co-routine a simple `iris_pipeline` pipeline for reducing an input raw science frame to a reduced frame. It currently doesn't handle telemetry or any configuration of the pipeline.

Next let's focus on the major capabilities we need to add to the DRS Assembly:

Telemetry handling
^^^^^^^^^^^^^^^^^^

`iris_pipeline` requires that all the metadata necessary for processing will be available in the headers of the raw science frame FITS files, therefore, the DRS Assembly will also need to gather the necessary Telemetry and add it to the FITS files.
Once we have a clearer picture on how Telemetry will be handled we can improve the design of this functionality. For example if there will be a way to access Telemetry from Python or C easily, we could have the first step of the processing pipeline collect the relevant telemetry and add it to the metadata. In this case the DRS Assembly wouldn't need to accomplish this task at all.

Another option is to have the Detector HCD receive telemetry and directly add the minimal required keywords to the raw science frames before they are read by the data reduction pipeline.

The current list of telemetry required by IRIS for all necessary purposes (i.e. online reduction, postprocessing) is documented in the `oirlab/iris_metadata repository on Github <https://github.com/oirlab/iris_metadata/>`_

Command handling
^^^^^^^^^^^^^^^^

Currently we have only planned to receive the command "Start acquisition" and send a notification once the processing is complete.
As soon as the design of the Observatory software is more mature, we will also consider if other commands are useful either for monitoring execution or for other purposes.

Pipeline configuration
^^^^^^^^^^^^^^^^^^^^^^

IRIS data will need to be reduced using different pipelines and for each pipeline different configuration options based on the instrument configuration, the purpose of the observation, the actual target, the weather conditions and more.

All of this logic needs to be implemented in the DRS Assembly. We also need extensive testing that ensures that all possible combinations of the options are properly handled by the software.

Pipeline execution
^^^^^^^^^^^^^^^^^^

In the proof-of-concept implementation, the DRS Assembly just imports `iris_pipeline` and executes the pipeline in a co-routine triggered by reception of a command. This is the simplest implementation and better allows exceptions in the code to flow through and be handled in the Assembly.

We will need to run benchmarks and make sure the Python Global Interpreter Lock is not slowing down the execution of multiple pipelines in parallel. If that is the case, we most probably transition all the computational kernels to `numba` so that in addition of gaining performance from compilation to machine code, we can also force release of the GIL.

Resiliency
^^^^^^^^^^

For online reduction, the pipeline needs to be resilient to errors, we will need to implement explicit handling for all the most common issues, like slow network, unavailable disk, out-of-memory. Moreover we need to make sure that a crash in the pipeline doesn't cause the whole DRS Assembly to crash.

This could also force us to re-design the software to be more decoupled. We will first keep the software simple and favor functionality and then plan for a refactoring to increase resiliency.

Use cases
---------

Description of the DRS Assembly use cases:

.. toctree::
   :maxdepth: 2

   use_cases

Data rates
----------

.. toctree::
   :maxdepth: 2

   data_rates


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
