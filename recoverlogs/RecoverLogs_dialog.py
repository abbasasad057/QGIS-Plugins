# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RecoverLogsDialog
                                 A QGIS plugin
 This plugin displays logs of specified features
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2018-05-21
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt5 import uic
from PyQt5 import QtWidgets

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'RecoverLogs_dialog_base.ui'))


class RecoverLogsDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(RecoverLogsDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)


FORM_CLASS1, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ConfigDialog.ui'))


class ConfigDialog(QtWidgets.QDialog, FORM_CLASS1):
    def __init__(self, parent=None):
        """Constructor."""
        super(ConfigDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)


FORM_CLASS2, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'results.ui'))


class ResultsDialog(QtWidgets.QDialog, FORM_CLASS2):
    def __init__(self, parent=None):
        """Constructor."""
        super(ResultsDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)


FORM_CLASS3, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'details.ui'))


class DetailsDialog(QtWidgets.QDialog, FORM_CLASS3):
    def __init__(self, parent=None):
        """Constructor."""
        super(DetailsDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)


FORM_CLASS4, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'details1.ui'))


class DetailsDialog1(QtWidgets.QDialog, FORM_CLASS4):
    def __init__(self, parent=None):
        """Constructor."""
        super(DetailsDialog1, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)


FORM_CLASS5, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'results1.ui'))


class ResultsDialog1(QtWidgets.QDialog, FORM_CLASS5):
    def __init__(self, parent=None):
        """Constructor."""
        super(ResultsDialog1, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)


# FORM_CLASS6, _ = uic.loadUiType(os.path.join(
#     os.path.dirname(__file__), 'results1Filt.ui'))
#
#
# class ResultsDialog1Filt(QtWidgets.QDialog, FORM_CLASS6):
#     def __init__(self, parent=None):
#         """Constructor."""
#         super(ResultsDialog1Filt, self).__init__(parent)
#         # Set up the user interface from Designer.
#         # After setupUI you can access any designer object by doing
#         # self.<objectname>, and you can use autoconnect slots - see
#         # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
#         # #widgets-and-dialogs-with-auto-connect
#         self.setupUi(self)
#
#
# FORM_CLASS7, _ = uic.loadUiType(os.path.join(
#     os.path.dirname(__file__), 'resultsFilt.ui'))
#
#
# class ResultsDialogFilt(QtWidgets.QDialog, FORM_CLASS7):
#     def __init__(self, parent=None):
#         """Constructor."""
#         super(ResultsDialogFilt, self).__init__(parent)
#         # Set up the user interface from Designer.
#         # After setupUI you can access any designer object by doing
#         # self.<objectname>, and you can use autoconnect slots - see
#         # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
#         # #widgets-and-dialogs-with-auto-connect
#         self.setupUi(self)
