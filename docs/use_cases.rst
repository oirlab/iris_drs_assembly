Use cases
=========

Start DRS
---------

Goal: Start DRS Assembly for readout writing, processing and automated real-time pipelines for post-processing.

Primary Actor: Astronomer, Support Astronomer, or Instrument Specialist

Preconditions:

Safety Notes:

-# Setup environmental variables and load configuration files for the pipelines
-# Check available drive space on readout and reduction disks
-# Check that readout and reduction disks are writable
-# Check socket communication (if on detector computer)
-# Setup directory structure on readout and reduction disks

Potential directory structure:
Readouts disk:

\code
/data1/date/readouts
/data1/date/raw
\endcode

Reduced disk:
\code
/data2/date/reduced
/data2/date/reduced/ifs
/data2/date/reduced/imager
\endcode


    - date is the UT date of the observation (i.e. 20170719)
-# Subscribe to telemetry and events.
-# Send status of DRS back to instrument sequencer
-# The DRS assembly is set to active idle status

Discussion: Perform pipeline test at the start of the pipeline to ensure that the pipeline is functioning correctly.

Observing Science on Detector Computers
---------------------------------------

Goal: Observing science on detector computers

Primary Actor: Astronomer, Support Astronomer, or Instrument Specialist

Preconditions:

Safety Notes:
The DetHCD running on the detector computers:

-# DetHCD receives a “start prepare” event from instrument sequencer (including subscribed telemetry about the instrument configuration, sampling, etc.) that an observation sequence will start.
-# The DetHCD executes the C library `iris_readout` once the readouts are received from the detector
-# Repeat until final raw science frame from the observing sequence is written.  This will be confirmed by the Imager/IFS Detector Assembly publishing the (endExposure) event (one for each detector that is exposing)
-# Once final frame header is read and organized into DB, DetHCD is set to idle until instrument sequencer sends another event of an observing sequence.

Observing Science on DRS Pipeline Computer
------------------------------------------

Goal: Observing science on DRS pipeline computer

Primary Actor: Astronomer, Support Astronomer, or Instrument Specialist

Preconditions:

Safety Notes:
The DRS Assembly running on the DRS computer:

-# Receive a “start prepare” observing event from instrument sequencer that an observing sequence is about to begin, the DRS assembly sets the polling service to active online status
    - The instrument sequencer will publish the observation setup, Observation ID, dither pattern, number of readouts, ramps, and whether the observation is science and sky through subscribed telemetry (e.g. obstype, obsname, dtotoff1, …)
-# Check for the raw science frames on the readout disk.
-# Once a file is found, read the header (via Python Astropy) information for first file
-# Upload raw science frame to the DMS (TBD)
-# Organize information based on received telemetry (e.g. obsname, obstype, datafile…) into a raw science database (DB; e.g. Python dictionary)
-# The DRS assembly will instruct the reduction pipelines to begin (see IMG-DRP and IFS-DRP, both implemented in `iris_pipeline`), if necessary files are found (i.e. if missing a sky frame, it will wait until sky is taken).
-# Check iteration number from header.
-# Repeat checking for raw science frames, organizing and running reduction pipelines until final frame from the observing sequence is written.  This will be confirmed by the Imager/IFS Detector Assembly publishing the (endExposure) event (one for each detector that is exposing)
-# Once final frame header is read and organized into DB, DRS assembly is set to idle until instrument sequencer sends another event of an observing sequence.

Writing an Individual Readout
-----------------------------

Goal: Generate raw science frame, write individual readouts

Primary Actor: DetHCD

Preconditions:

Safety Notes: Quality check and verbose if data is not saved to readout disk.

The `iris_readout` C library called from the `DetHCD`  will have two functions; 1) receiving and writing data (including receiving telemetry and creating headers) to a FITS file from the imager/IFS HCD and 2) sampling of the individual raw readouts (FITS file) to final generated raw science (FITS file).  These processes will run simultaneously.

Exposure sequence of N number of raw science frames with M number of readouts per raw science frame.
-# DetHCD receives the readout data from the detector
-# Once the DetHCD received the event from instrument sequencer it will immediately pull the necessary metadata from the subscribed telemetry and create a FITS header for each individual readout frame.
-# The DetHCD will write out individual readouts to FITS file with the generated header to the readout disk using the `iris_readout` C library:
   - The DetHCD will also notify the instrument sequencer whether the operation was successful by publishing writeReadout event.
   - For the first readout, the DetHCD will publish “start readout” observe event
-# The DetHCD will verify that the readout is written.
-# The DetHCD will continue the sequence until M number of readouts are received.

Run sampling Algorithm on Readouts
----------------------------------

Goal: Generate raw science frame, write individual readouts

Primary Actor: DetHCD and `iris_readout`

Preconditions:

Safety Notes: Quality check and verbose if data is not saved to readout disk.

-# The sampling job will use each readout and begin to perform the sampling algorithm (e.g., UTR, MDS, CDS; based on what is selected from the instrument sequencer by the Astronomer), performing the following operations:
    - Reference pixel subtraction, linearization, bad pixel flagging
    - Up-the-ramp (UTR)/Multiple Correlated Double Sampling (MCDS) computed for each ramp
    - Ramps added/averages
-# Once the sampling algorithm is complete, the headers from all the readouts are combined into one header and a final header is created for the Science Frame
-# The final image and header is written to a FITS file (raw science frame) on the readout disk.
-# The DetHCD will verify that the raw science frame is written.
-# DetHCD tells the instrument sequencer that the final raw science frame FITS file has been written and to start next exposure by publishing “end dataset write” observe event.

\ section drsAsm_usecases_createrawscience Build a raw science frame offline

Goal: User starts sampling of readouts to construct raw science frame

Primary Actor: Astronomer

Preconditions: User needs to download the readouts from the readout storage disk

Safety Notes:

User running `iris_pipeline` on their own machine, `iris_pipeline` also includes Python wrappers to the same `iris_readout` C library which is integrated in `DetHCD`:

-# User selects the individual readouts, via GUI or editing configuration files, to run the sampling algorithm
-# The sampling job will open each of the readouts and then perform the sampling algorithm on them, performing the following operations:
   - Reference pixel subtraction, linearization, bad pixel flagging
   - Up-the-ramp (UTR)/Multiple Correlated Double Sampling (MCDS) computed for each ramp
   - Ramps added/averages
-# Once the sampling algorithm is complete, the headers from all the readouts are combined into one header and a final header is created
-# The final image and header is written to a FITS file (raw science frame) on the users disk
-# The information from the raw science frame is stored in a raw science DB

Note: This step can be skipped if the user does not wish to change the default sampling selected during their observations for the generation of the raw science frames.

Reduction of imager data
------------------------

Goal: Start reduction of imager data

Primary Actor: Astronomer, Support Astronomer, or Instrument Specialist

Preconditions:

Safety Notes:

-# The DRS assembly instructs the imager reduction pipeline (included in `iris_pipeline`) to run once the required number of frames (science, calib and sky) are found in the raw science DB
    - Sky and calibration files will be identified by nearest Julian date within the DB
    - If a sky and calibration files are missing, the DMS will be searched for a relevant calibration file based on the nearest Julian date (TBD)
    - Sky frames are identified from the observing sequence from the instrument sequencer from telemetry of the obsname and obstype.
-# Science and calibration files are read (via Python Astropy) into the IMG-DRP from the readout disk
-# The IMG-DRP will run on the science and calibration files, making use of the following algorithms:
    - Sky/Dark subtraction
    - Correction of detector artifacts
    - Correction of cosmic rays
    - Flat fielding
-# The reduced image and header is written to a FITS file on the reduction disk with the file name format that includes the ObjectID.
-# The reduced image is uploaded to the DMS (TBD)

/section drsAsm_usecases_reduce_spec Reduction of IFS slicer data (IFS-DRP)

Goal: Start reduction of IFS slicer data

Primary Actor: Astronomer, Support Astronomer, or Instrument Specialist

Preconditions:

Safety Notes:


-# The DRS assembly sends command to spawn the IFS slicer reduction process (IFS-DRP, based on `iris_pipeline`) once the required number of frames (science, calib and sky) are found in the raw science frame DB
    - Sky and calibration files will be identified by nearest Julian date within the DB
    - If a sky and calibration files are missing, the DMS will be searched for a relevant calibration file based on the nearest Julian date (TBD)
    - Sky frames are identified from the observing sequence from the IRIS sequencer
-# Raw science frames and calibration frames are read (via pyfits) into the real-time IFS slicer reduction process from the readout disk
-# The real-time IFS slicer reduction will run on the science and calibration files, making use of the following algorithms:
    - Sky/Dark subtraction
    - Correction of detector artifacts
    - Correction of cosmic rays
    - Flat fielding
    - Spectral extraction
    - Wavelength solution
    - Cube assembly (x, y, wavelength)
-# The reduced data cube and header is written to a FITS file on the reduction disk
-# The reduced data cube is uploaded to the DMS (TBD)

Reduction of IFS lenslet data
-----------------------------

Goal: Start reduction of IFS lenslet data

Primary Actor: Astronomer, Support Astronomer, or Instrument Specialist

Preconditions:

Safety Notes:


-# The DRS Assembly spawns the IFS lenslet reduction process (IFS-DRP) once the required number of frames (science, calib and sky) are found in the raw science frame DB
    - Sky and calibration files will be identified by nearest Julian date within the DB
    - If a sky and calibrations file are missing, the DMS will be searched for a relevant calibration file based on the nearest Julian date (TBD)
    - Sky frames are identified from the observing sequence from the IRIS sequencer
-# Science and calibration files are read (via Python Astropy) into the real-time IFS lenslet reduction process from the readout disk
-# The real-time IFS lenslet reduction will run on the raw science frames and calibration frames, making use of the following algorithms:
    - Sky/Dark subtraction
    - Correction of detector artifacts
    - Correction of cosmic rays
    - Spectral extraction
    - Wavelength solution
    - Cube assembly (x, y, wavelength)
-# The reduced data cube and header is written to a FITS file on the reduction disk
-# The reduced data cube is uploaded to the DMS (TBD)

Display IFS/imager data
-----------------------

Goal: Display raw and reduced IFS/imager data in the quicklook visualization tool

Primary Actor:

Preconditions:

Safety Notes:
Two quicklook visualization tools will be open for displaying the reduced IFS data and reduced imager data.
For calibration, engineering and readouts:
Two quicklook visualization tools will be open for displaying the raw IFS data and raw imager data.


-# DRS visualization tool checks the raw and reduced directories for new images (IFS/imager)
-# Once a new frame is found, the DRS Assembly spawns the quicklook visualization tool to display the frame on screen, if the quicklook visualization tool is not running for either the IFS or imager data.
    - If the quicklook visualization tool is already running with an IFS frame, the currently running quicklook tool will load the new image.
    - If the quicklook visualization tool is closed for any reason, the tool will reload when the new frame is found.
-# Continue checking for new IFS/imager frames, replace previous frame with new frame.


Offline manual processing
-------------------------

Goal: User reduces raw science frames on their own machine

Primary Actor:

Preconditions: User needs to download the raw science frames from the readout storage disk or the DMS, or run the sampling algorithm on readouts to create a raw science frame (see section 4.1.6).

Safety Notes:

`iris_pipeline` includes Python wrappers of the `iris_readout` C library to implement sampling algorithm that transform raw readouts to raw science frames. Therefore the same tool can be used whether the user wants to start from raw readouts or directly from raw science frames.

-# User selects the individual raw science frames (either from imager or IFS), via GUI or edits data reduction files (a pipeline configuration text file in .ini format, see `stpipe` and an association JSON file, see the <a href="https://jwst-docs.stsci.edu/display/JDAT/Understanding+Associations">JWST documentation</a>), to run the data pipeline on.
-# `iris_pipeline`, based on `stpipe`, will read the header keywords (e.g. obsname and obstype), and from the FITS files and decide which data pipeline (i.e. final image (see Table 2), final IFS lenslet or final IFS slicer (see Table 3)) will run and which algorithms will be available to use.
    - If using the GUI, the user will be able to select which steps to run in the full pipeline
    - If using a configuration file, each section will represent a different algorithm and the user may add or remove those steps.
-# The user will click on a button to execute the pipeline or run the `strun` script that starts the execution of the pipeline.
-# The data pipelines will execute
    - If an error occurs, `iris_pipeline` will return the error message back to the user
    - Otherwise, the `iris_pipeline` will show an execution log and a completion message at the end

Quicklook visualization
-----------------------

Goal: Display images and data cubes from imager/IFS (science/calibrations)

Primary Actor: Astronomer, Support Astronomer, or Instrument Specialist

Preconditions:

Safety Notes:
The quicklook visualization tool is a utility for displaying raw and reduced images from the IRIS imager and IFS.
General features:
- Displays 2D and 3D images (data cubes).
- Plotting, slicing the data arrays in multiple ways (2D and 3D images)
    - Displays slices of data cubes
    - Plot horizontal, vertical and diagonal cuts across the image
    - Display a surface plot and display a contour plot
    - Note: This includes collapsing (e.g. take a mean, median and sum) the data in these dimensions,
- Take median, mean, sum of the data (either in slices or as a whole), Gaussian and boxcar smoothing of the data (either in channels, slices or as a whole).  Note: A slice is a selection of one or more channels from a data cube.
- Adjust brightness (stretch), contrast, image stretch schemes (e.g. linear, log, power law), invert the stretch
- Pan; recenter; zoom in and zoom out
- Compute statistics on regions of pixels or spaxels (e.g., sum, error, area, surface brightness, mean, median, minimum, maximum, variance, standard deviation)
- Centroid on the peak of a source
- Overplot multiple images and spectra with specified regions.
- Displays imager images in mosaic mode (i.e. all 4 chips, if available)

Visualization: Centering IFS/Imager
-----------------------------------

Goal: Center the object on the detector (IFS/Imager)

Primary Actor: Astronomer

Preconditions: quicklook has displayed a reduced IFS/imager frame

Safety Notes: Need something to say a move is bad (i.e. bogus coordinates)

-# A user will click on the x and y pixel position in the reduced frame (IFS or imager) where they want to center the telescope using their mouse.
    - The user will have the option to auto centroid based on the position that they clicked or use the original position.
    - The user will also have an option to tweak the position slightly (i.e. using the arrow keys on the computer).
-# Once the user is satisfied with the pixel position that they selected, they will have an option to send the coordinates to the TCS (via instrument sequencer?)
-# The telescope will point to the new position.

Interface Implications: Need an ICD for the TCS or instrument sequencer to pass the coordinates.  Will also need to have a precise mapping from the instrument coordinates to the telescope coordinates.
