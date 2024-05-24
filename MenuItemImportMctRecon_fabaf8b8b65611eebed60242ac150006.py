"""
An importer for volumetric CT data reconstructed with the Australian Synchrotron's MCT beamline reconstruction pipeline.

:author: Gary Ruben
:contact: 
:email: rubeng@ansto.gov.au
:organization: Australian Synchrotron
:address: 800 Blackburn Rd, Clayton VIC 3168, Australia
:copyright: 
:date: Jan 18 2024 15:39
:dragonflyVersion: 2022.2.0.12227
:UUID: fabaf8b8b65611eebed60242ac150006
"""

__version__ = '1.0.0'

import sys
from pathlib import Path

import numpy as np
import h5py

from PyQt5.QtWidgets import QFileDialog, QMessageBox
from ORSServiceClass.menuItems.userDefinedMenuItem import UserDefinedMenuItem
from ORSServiceClass.actionAndMenu.menu import Menu
from ORSServiceClass.decorators.infrastructure import interfaceMethod
from ORSModel import createChannelFromNumpyArray
# from ORSModel.ors import DimensionUnit


def load_file(filepath: str, h5_path: str) -> None:
    """Load a data volume from an hdf5 file into a Dragonfly channel

    Parameters
    ----------
    filepath : str
        pathlib.Path-compatible path to an hdf5 file
    h5_path : str
        Path in hdf5 file to the data volume (case sensitive), e.g. /data
    """
    
    # The Dragonfly method createChannelFromNumpyArray accepts only these Numpy data types:
    # np.int8, np.uint8, np.int16, np.uint16, np.int32, np.uint32 and np.float32

    with h5py.File(filepath, 'r') as f:
        data = f[h5_path]

        # load into memory
        data = data[:]

        # Retrieve voxel side lengths; these are in metres, which matches Dragonfly's units
        try:
            x_spacing, y_spacing, z_spacing = f[h5_path].attrs['Spacing']
        except KeyError:
            x_spacing, y_spacing, z_spacing = (1, 1, 1)

    channel = createChannelFromNumpyArray(data)
    channel.setTitle(Path(filepath).stem)

    channel.setXSpacing(x_spacing)
    channel.setYSpacing(y_spacing)
    channel.setZSpacing(z_spacing)

    channel.publish()


def h5_path_exists(filepath: str, h5_path: str) -> bool:
    """Checks whether the h5_path exists in an hdf5 file without loading any contents

    Parameters
    ----------
    filepath : str
        pathlib.Path-compatible path to an hdf5 file
    h5_path : str
        Path in hdf5 file to the data volume (case sensitive), e.g. /data

    Returns
    -------
    bool
        True iff the path exists
    """
    with h5py.File(filepath, 'r') as f:
        return h5_path in f


def error_dialog(title: str, text: str) -> None:
    """Qt Informational Error dialog with a single OK button

    Parameters
    ----------
    title : str
        Window title
    text : str
        Window text
    """
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)

    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setStandardButtons(QMessageBox.Ok)

    retval = msg.exec()


class MenuItemImportMctRecon_fabaf8b8b65611eebed60242ac150006(UserDefinedMenuItem):
    """Auto-generated class defining a top-level Dragonfly menu
    """

    @classmethod
    def getTopLevelName(cls):
        """
        Defines the top level menu name where the menu item will appear.
        """
        return 'MCT'


    @classmethod
    def getMenuItem(cls):
        """
        :return: Menu item
        """
        aMenuItem = Menu(title='Import MCT Recon...',
                         id_='MenuItemImportMctRecon_fabaf8b8b65611eebed60242ac150006',
                         section='',
                         action='MenuItemImportMctRecon_fabaf8b8b65611eebed60242ac150006.menuItemEntryPoint()')
        return aMenuItem


    @classmethod
    def menuItemEntryPoint(cls):
        """
        Will be executed when the menu item is selected.
        """
        filepath, _filter = QFileDialog.getOpenFileName(
            caption="Please select an hdf5 recon file",
            directory="/data/mct",
            filter="hdf5 (*.h5 *.hdf5)",
        )

        if filepath is not None:
            # MCT recon files contain the reconstructed volume data in a couple of locations
            # Try to read from each in turn
            if h5_path_exists(filepath, h5_path := "/data"):
                load_file(filepath, h5_path)
            elif h5_path_exists(filepath, h5_path := "/MCT/DATA"):
                load_file(filepath, h5_path)
            else:
                error_dialog("Load Error", "No hdf5 path /data or /MCT/DATA found")
