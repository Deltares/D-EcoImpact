# Visualization of input and output data

There are multiple ways that the data used and produced can be visualized. Here the use of Panoply to explore the data construct, Quickplot for 2D horizontal and 3D vertical visualization and QGIS for spatial relevant visualization are discussed.


## Panoply

Panoply is a NetCDF viewer developed by NASA GISS. Panoply can be downloaded [here](https://www.giss.nasa.gov/tools/panoply/).

Panoply is useful for exploring the content of NetCDF files. It allows the user to see which variables are present in the file, over which dimensions these variables contain values (e.g. x, y, z, time) and what metadata is supplied with each variable. Especially when you have gotten a NetCDF file that you are not familiar with on which data it contains it can be useful to open it first with Panoply.

![Panoply](/assets/images/3_netcdf.png "The FM-VZM_0000_map.nc opened in Panoply. The variable “mesh2d_sa1” (Salinity) has been selected for viewing. On the right hand-side the metadata attached to this variable is visible, among which the first line showing that this variable has values allocated to 3 dimensions (time, mesh2d_nFaces and mesh2d_nLayers).")

## Quickplot
Quickplot is a Deltares visualization tool used amongst others for Delft3D 4 and Delft3D-FM models. Intern Deltares the latest version of Quickplot can be gathered here:

(n:\Deltabox\Bulletin\jagers\Delft-QUICKPLOT MCRv82 (2013b)\64bit\)

Quickplot is also co-delivered with the installation of one of the Delft3D suites. 

Quickplot allows the visualization of UGRID NetCDF files, both in the horizontal, over time and in the vertical (for 3D models). 

![Quickplot](/assets/images/3_quickplot.png "The FM-VZM_0000_map.nc opened in Quickplot. The variable “Salinity” (mesh2d_sa1) has been selected for viewing. On the left hand side the selection of time period (Time Step=150) and the toplayer is shown (K=22). On the right hand-side the values attached to this variable are visible.")

## QGIS
QuantumGIS (QGIS) is open source free ware GIS software. The latest version of QGIS can be downloaded [here](https://www.qgis.org/en/site/forusers/download.html)

QGIS can handle 2D Mesh data directly. When it comes to 3D mesh data a Deltares plugin developed by Jan Mooiman (QGIS_Qmesh) can perform the visualisation. Also visualization through time is made easy with the QGIS_Qmesh plugin. Intern Deltares the latest version of this plugin can be gathered here:
n:\Deltabox\Bulletin\mooiman\programs\
or externally compiled [here](https://github.com/Deltares/qgis_umesh).

When Mesh data is loaded directly in QGIS the spatial relevance can be easily displayed using the plugin QuickMapServices > OSM layer.

![QGIS](/assets/images/3_qgis.png "The FM-VZM_0000_map.nc opened in QGIS through the “Add mdal layer” function. The variable “Bed level” (mesh2d_flowelem_bl) has been selected for viewing. As background for spatial relevance the OSM layer of QuickMapServices is used. The test file is a part of the Volkerak-Zoom Lake model in the Netherlands.")


![QMESH](/assets/images/3_qgis_qmesh.png "The FM-VZM_0000_map.nc opened in QGIS through the QGIS_Qmesh plugin. The variable “Salinity” (mesh2d_sa1)  has been selected for viewing and the top layer (Layer=22) is shown on a specific time step. As background for spatial relevance the OSM layer of QuickMapServices is used. The test file is a part of the Volkerak-Zoom Lake model in the Netherlands.")




