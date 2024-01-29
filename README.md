# dragonfly_mct_import
## Description
This is a menu item for ORS Dragonfly for importing volumetric CT data produced by the Australian Synchrotron's MCT beamline reconstruction software pipeline.

## Installing
To install this menu item in Dragonfly, the .py file just needs to be placed in the Dragonfly pythonAllUsersExtensions/GenericMenuItems directory.

In our own Dockerfile for deploying Dragonfly in our Linux processing environment, we do this with the following line:

ADD MenuItemImportMctRecon_fabaf8b8b65611eebed60242ac150006.py /opt/dragonfly/Dragonfly2022.2/pythonAllUsersExtensions/GenericMenuItems/.
