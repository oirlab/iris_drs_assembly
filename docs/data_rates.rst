Data rates and storage
######################

One of the goals of TMT observatorys DMS is to archive raw data from all TMT instruments for data storage and delivery to astronomical users. The DMS is currently only being designed to store raw science quality files. Our team is currently exploring the technical and scientific merits for storing all individual reads from the imaging and spectrograph detectors, to improve the quality of the reduction in both real-time and during post-processing. Indeed, there are several missions that have greatly benefited with saving all individual detector reads (e.g, NASA Spitzer) that have generated additional science results that would not have been possible without this capability.
Raw science-quality near-infrared astronomical frames are typically produced in the following:

- Reads are read from the detector into memory (readouts)
- Intermediate reduction is performed for all reads for a user defined exposure time
	- Reference pixel subtraction, linearization, deinterlacing, bad pixel flagging
	- Up-the-ramp (UTR)/Multiple Correlated Double Sampling (MCDS) computed for each ramp
	- Ramps added/averages
- A final file with combined readouts are written to disk as a FITS file (raw science frame)

In this typical readout method, the intermediate reduction is run before the science-quality raw FITS file is created. Our team has been exploring the possibility and advantages of saving every individual read to allow for greater flexibility and performance improvements in the reduction process. For example, if the seeing degrades for a select number of individual reads, those reads can be removed in post-processing to improve the overall S/N of the raw science frame. This will require that metadata from the AO system, TCS, and other supporting systems would need to be recorded in real-time. The astronomical user then has the flexibility of optimizing their reductions during post-processing using the needed telemetry associated with each readout. This is especially true (and likely) if there are newer sampling schemes or masking techniques not considered yet by the instrument team, then the astronomical user can greatly benefit from storing all individual reads.

Maximal Data rates
------------------

The following table explores the maximum data rates possible with the imager and spectrograph setup. The maximum data rates calculated assumes the following configuration: a pixel clocking rate of 400 MHz with 64 readout channels gives a minimum read time of 0.72 seconds; Correlated Double Sampling (CDS) clock time of 2.16 seconds per exposure; 4k×k detector will have 64 MB per exposure; and the observing run will be 16 hours per night (science with calibrations); and assuming 91 total observing nights per year. This method is with (unrealistically) taking raw frames continuously in CDS with the minimum integration time (including 1 reset) and ignoring overhead between frames (on average 1/2 read time and could be as much as 1 read time). Table 5, column 2 shows the maximum data rates is all individual readouts are saved. Each of these calculations ignore real world overheads, such as resets, pausing exposures during target acquisition, and telescope dithering. Since each individual read are in integers, these files will be written with 16 bits/pixel.
The total data rates per detector and 5 detectors, including raw and readout frames, is listed in Table 8, columns 3 and 4. Currently, the planned implementation of data storage is that raw science (FITS) frames are stored on the DMS. Individual readouts will be stored on the IRIS stand-alone readout disk, and our team is investigating future archiving and long-term solutions. To store <3 months of individual readouts taken at the maximum data rates would require <280 TB storage.

<table ><tr ><td   >Raw Science Frames</td><td   >Readout Frames</td><td   >Total Per Detector</td><td   >Total Per 5 Detectors</td></tr><tr >
<td   >29.6 MB/s <br /> 104 GB/hr <br /> 1666 files/hr <br /> 1.64 TB/night <br /> 26,666 files/night <br /> 149 TB/yr <br /> 2,426,600 files/yr</td><td   >44 MB/s <br /> 156 GB/hr <br /> 5000 files/hr <br /> 2.44 TB/night <br /> 80,000 files/night <br /> 222 TB/yr <br /> 7,280,000 files/yr</td><td   >73.6 MB/s <br /> 260 GB/hr <br /> 6666 files/hr <br /> 4.08 TB/night <br /> 106,666 files/night <br /> 371 TB/yr <br /> 9,706,600 files/yr</td><td   >368 MB/s <br /> 1.27 TB/hr <br /> 33,330 files/hr <br /> 20.4 TB/night <br /> 533,330 files/night <br /> 1.81 PB/yr <br /> 48,533,000 files/yr</td></tr></table>

Table 8: Maximum IRIS data rates with continuous data taking configuration. The total per detector is calculated by summing the raw frames and the readouts.

Real World Reduced Data Rates
-----------------------------

The DRS reduced data product rates were computed using the IFS slicer (45x90) at R=4000 (800 spectral elements) and imager (4096x4096).
Assumptions:

- The reduced frames contain 3 extensions (science, noise and flags).
   - Single floats (32 bits) are used for the science and noise frames
   - Unsigned integers are used for the flags (8 bits).
- Each raw IFS frame has data cube created
- Each raw imager frame is sky-subtracted
- Assumptions:
- Dither overhead: 60 seconds
- Frame overhead: 5 secs

Real world case 1: Dither pattern of 300 second IFS observations; CDS Imager observations as many frames as possible. This also assumes 16 hours observing with 12 hours on sky, 4 hours for calibration and 91 nights a year (1/4 year).
Note: We do not combine frames for final stacks in this calculation. We also do not include calibrations (i.e. arcs, flats, master darks, master flats).
Discussion: We need to explore how the data rates will change with different observing modes (i.e. mosaicking, multiple objects, single objects, etc).

<table ><tr ><td   >Products</td><td   >Individual Frame</td><td   >Hourly Data Rate</td><td   >Nightly Data Rate</td><td   >Yearly Data Rate</td></tr><tr ><td   >Reduced Imager</td><td   >151.0 MB (1 det) <br /> 604.0 MB (4 det)</td><td   > 62.4 GB/hr (1 det) <br /> 250.0 GB/hr (4 det)</td><td   >0.75 TB/night (1 det) <br />   3.00 TB/night (4 det)</td><td   > 68.1 TB/year (1 det) <br /> 272.6 TB/year (4 det)</td></tr><tr ><td   >Reduced IFS</td><td   >58.3 MB</td><td   >641.3 MB/hr</td><td   >11.0 GB/night</td><td   >1.0 TB/year</td></tr></table>Table 9: Real world IRIS data rates from reduced products.

In addition, IRIS will have a 120 modes for the IFS (slicer and lenslet), which will require a rectification matrix for each one.  Including 3 extensions in each file, will require 5.6 GB/year.
In general, these are the frame sizes:

- Imager = 4 detectors x 151.0 MB = 604.0 MB Note: This is an image with 3 extensions (float science, float noise, int flag)
- IFS = 73.7 MB Note: This is a maximum size for a spectrum with 3 extensions (float science, float noise, int flag)

Calibration Data Rates from the DMS
-----------------------------------

The calibration data rates from the DMS, operating under the assuming if the calibration frames are downloaded from the DMS in order to produce the real-time reduction.  The rates include the cases in which the rectification matrices (for the IFS lenslet observations) are downloaded from the DMS, and stored locally.  The rates have a 1st run and Nth run which represent frames that are needed initially but then can be reused throughout the night (i.e. master darks, bad pixel maps).  We also assume the modes are unique (i.e. no reuse of calibration frames for filter and scale).

<table ><tr ><td  colspan="3" >Instrument</td><td   >1st;Observation</td><td   >Nth;Observation</td></tr><tr ><td  colspan="3" ></td><td   >[MB]</td><td   >[MB]</td></tr><tr ><td   rowspan="3">IFS</td><td   rowspan="2">Lenslet</td><td   >Rectmat</td><td   >1441.1</td><td   >1273.3</td></tr><tr ><td   >No rectmat</td><td   >392.5</td><td   >224.7</td></tr><tr ><td  colspan="2" >Slicer</td><td   >543.5</td><td   >224.7</td></tr><tr ><td  colspan="3" >Imager</td><td   >1275.2</td><td   >604.0</td></tr></table>Table 10: Calibration data rates from the DMS

Lenslet calibration data rates from the DMS include the following; arc lamp, bad pixel map, master dark, sky spectra, rectification matrix (rectmat).  Data rates include with and without downloading the rectmat from the DMS.
Slicer calibration data rates from the DMS include the following; arc lamp, bad pixel map, master dark, flat field, sky spectra.
Imager calibration data rates from the DMS include the following; bad pixel map, master dark, sky images.
The maximal data rate from the DMS for calibration frames in a given night, assuming 8 unique modes of imaging and spectroscopy, would be 7619.5 MB/night w/o rectmats and 10354.3 MB/night with rectmats. The calibration fame sizes are listed in Table 11.


- Frame Size [MB]
- Arc lamp 151.0
- Bad pixel map 16.8
- Master dark 151.0
- Sky spectra 73.7
- Sky image 151.0
- Rectification matrix (maximum) 1048.6
- Flat (IFS slicer only) 151.0

Table 11: Calibration frame sizes for a single detector

The memory usage of the individual algorithms can be found in Table 12 for the imager and Table 13 for the IFS.  It is assumed that the frames are completely loaded in memory, and does not account for optimal methods of reading in subarrays of data as well as utilizing running sum techniques.

<table ><tr ><td   >DRS post processing </td><td   ># Frames </td><td   >Memory </td><td   >Function</td></tr><tr ><td   >Generate master dark<br /> Dark subtraction;<br />Remove detector artifacts<br /> Flat Fielding*<br /> Spectral extraction<br /> Wavelength calibration<br /> Cube assembly;<br />Scaled sky-subtraction<br /> Residual ADC<br /> Telluric correction<br /> Flux calibration <br />Mosaic/Combine SCI </td><td   >~10<br />2<br />2<br />2<br />1<br />2<br />2<br />2<br />2<br />2<br />2<br />&gt;2</td><td   >1.51 GB<br />302 MB<br />302 MB<br />302 MB<br />178.5 &ndash; 1122.3 MB<br /> 147.4 MB<br />147.4 MB<br />147.4 MB<br />147.4 MB<br />147.4 MB<br />147.4 MB<br />Nframes x 73.7 MB</td><td   >Median combine<br />Subtraction<br />Bad pixel and CR removal<br />DIV by normalized flat field<br />Advanced spectral extraction<br /> Least square minimization<br /> Cube assembly<br />;OH and continuum scaling<br />Atm. Dispersion Correction<br />Telluric feature removal<br />Flux calibration;<br />Dither shifts</td></tr></table>

Table 12: Memory used by specific DRS algorithm for the IFS

<table ><tr ><td   >DRS post processing </td><td   ># Frames</td><td   >Memory </td><td   >Function</td></tr><tr ><td   >Generate master dark<br /> Dark subtraction <br />Remove detector artifacts <br />Flat Fielding <br />Scaled sky-subtraction <br />Field distortion correction <br />Flux calibration <br />Mosaic/Combine SCI </td><td   >~10<br />2<br />2<br />2<br />2<br />1<br />2<br />&gt;2</td><td   >1.51 GB (6.04 GB) <br />302 MB (1.21 GB) <br />302 MB (1.21 GB) <br />302 MB (1.21 GB) <br />302 MB (1.21 GB) <br />151 MB (604 MB) <br />302 MB (1.21 GB)<br />Nframes x 151 MB(Nframes x 604 MB)</td><td   >Median combine<br />Subtraction<br />;Bad pixel and CR removal<br />DIV by normalized flat field<br /> Scale factor from sky<br /> FRS Field distortion correction <br />Flux calibration;<br />Dither shifts </td></tr></table>

Table 13: Memory used by specific DRS algorithm for the Imager per detector

2x for redundancy
Readout Computer 2 x 0.5 PB/night
Pipeline Computer 2 x 4 TB/night

Computing Hardware Required
---------------------------

During the phases of design and construction of IRIS the DRS will require computers during for development and testing. Listed below are the computers required for each phase.  A brief summary is listed in Table 14.

- Phase, Computer(s)
- FDP, Readout Computer Pipeline Computer Simulated DMS Computer
- FAB, Readout Computer Pipeline Computer
- INT, Readout Computer Pipeline Computer

Table 14: The computers required during each of the phases for development of the IRIS DRS.  Note: Final design phase (FDP), Fabrication: (FAB), and Integration (INT).

Readout computer
The purpose of the readout computer is to store all of the IRIS readouts from all 5 detectors (IFS and imager). This computer needs 0.5 Petabyte of storage to store the readouts for up to 3 months.  We require 2x the storage for redundancy (or 1 Petabyte).  This computer will interface between the IRIS detectors, the DRS pipeline computer and the DMS. This computer needs to be relatively fast and with sufficient memory to handle the bandwidth from the other services requesting the data.

Pipeline computer
The purpose of the pipeline computer is to process the all of the IRIS IFS and imager raw science frames quickly such that an observer will be able to evaluate and analysis it in real-time. This computer needs to be very fast and have multiple cores (i.e. Intel Xeon 2.2GHz with 22 cores) to meet the requirement of producing a reduced science image within 30 seconds and reduced IFS data cube within 60 seconds ([REQ-2-IRIS-1630]) of the data being taken. In addition, this computer needs a large amount of memory (1TB), particularly for parallel processing all of the detectors.  Finally, a small amount of storage (10 TB) is necessary to store the reduced data products for up to 3 days after observation. We require 2x the storage for redundancy (or 20 TB).

Simulated DMS computer
During FDP we will need to simulate the communications between the pipeline computers the DMS and other services that the DRS will subscribe to for telemetry (e.g. TCS, AOESW, NFIRAOS, M1CS, and NSCU).  We plan on simulating this communications with a third computer which is specced as a readout disk computer.

Development phases:

FDP: The pipeline and readout computers can be scaled down versions (less memory and storage) than that required during INT in order to develop the infrastructure of the DRS and readout processor.   However, we will require a third computer (DMS/metadata computer) to simulate the connections between the IRIS detectors, the readout disk, DMS and subscribed telemetry (e.g. TCS, NFIRAOS, AOESW, NSCU, M1CS).

FAB: We require 1 of the 4 INT readout computers and storage space to store the engineering data from the lab from the IRIS detectors.

INT: We will require the final readout and pipeline computer during this phase. Since computers will get better over time, we will purchase these computers right before INT.  The readout computer will have the full 1 PB storage and the pipeline computer will have the 22+ required cores.
