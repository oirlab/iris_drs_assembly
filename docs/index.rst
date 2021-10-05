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

Telemetry handling
------------------

`iris_pipeline` requires that all the metadata necessary for processing will be available in the headers of the raw science frame FITS files, therefore, the DRS Assembly will also need to gather the necessary Telemetry and add it to the FITS files.
Once we have a clearer picture on how Telemetry will be handled we can improve the design of this functionality. For example if there will be a way to access Telemetry from Python or C easily, we could have the first step of the processing pipeline collect the relevant telemetry and add it to the metadata. In this case the DRS Assembly wouldn't need to accomplish this task at all.

Use cases
---------

Description of the DRS Assembly use cases:

.. toctree::
   :maxdepth: 2

   use_cases



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
