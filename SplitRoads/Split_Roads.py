# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SplitRoads
                                 A QGIS plugin
 This plugin splits selected roads on intersections.
                              -------------------
        begin                : 2018-04-19
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
import tempfile
import uuid
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QAction
# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .Split_Roads_dialog import SplitRoadsDialog
import os.path
import processing
from qgis.utils import *
from qgis.core import *
import numpy as np
from osgeo import ogr


class SplitRoads:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        self.dlg = SplitRoadsDialog()
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'SplitRoads_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'Road Splitting Plugin')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'SplitRoads')
        self.toolbar.setObjectName(u'SplitRoads')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('SplitRoads', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference


        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def split(self):
        lyr = self.iface.activeLayer()
        # print(lyr.primaryKeyAttributes())
        pkIdx = lyr.primaryKeyAttributes()[0]
        # print("PK:"+str(pkIdx))
        new_layer = lyr.materialize(QgsFeatureRequest().setFilterFids(lyr.selectedFeatureIds()))

        alg = 'grass7:v.clean'
        extent = new_layer.extent()
        xmin = extent.xMinimum()
        xmax = extent.xMaximum()
        ymin = extent.yMinimum()
        ymax = extent.yMaximum()
        temppath = tempfile.gettempdir()
        uId = str(uuid.uuid4()).replace("-", "")
        tempPath = temppath.replace("\\", "/")+"/output{0}.shp".format(uId)

        params = {"input": QgsProcessingFeatureSourceDefinition(new_layer.name(), True), "type": [1], "tool": [0],
                  "-b": False, 'threshold': '', "-c": False, "output": tempPath,
                  'error': 'memory:errorFile.shp', "GRASS_REGION_PARAMETER": "%f,%f,%f,%f" % (xmin, xmax, ymin, ymax),
                  "GRASS_SNAP_TOLERANCE_PARAMETER": 5, "GRASS_MIN_AREA_PARAMETER": 0.0001,
                  "GRASS_OUTPUT_TYPE_PARAMETER": 0}

        splitResults = processing.run(alg, params)
        # print(splitResults['output'])
        splitLyr = QgsVectorLayer(splitResults['output'], "Cleaned", "ogr")
        # QgsProject.instance().addMapLayer(splitLyr)
        featsSplit = [feature for feature in splitLyr.getFeatures()]
        # print(len(featsSplit))
        idFld = np.asarray([s.attributes()[pkIdx+1] for s in featsSplit])
        # print(idFld)
        unqFldId = list(set(idFld))
        nonUnqFlds = []
        for idx, fldIdVal in enumerate(unqFldId):
            repCount = len(idFld[np.where(idFld == fldIdVal)])
            if repCount > 1:
                nonUnqFlds.append(fldIdVal)
        # print([f.name() for f in lyr.fields()])
        newFeats = []
        # splitFlds = [fld for fld in splitLyr.fields()]
        # print(splitFlds[1:])
        # print([f.name() for f in lyr.fields()])
        for splitFeat in featsSplit:
            # print(nonUnqFlds)
            if splitFeat.attributes()[pkIdx+1] in nonUnqFlds:
                # print("Loop:" + str(splitFeat.attributes()[pkIdx]))
                # print(pkIdx)
                # print("DefaultVal:", lyr.dataProvider().defaultValueClause(pkIdx))
                splitFeat.setAttribute(pkIdx+1, lyr.dataProvider().defaultValueClause(pkIdx))
                # print(lyr.dataProvider().defaultValueClause(pkIdx))
                newFeat = QgsFeature()
                # print(splitFeat.geometry().asPolyline())
                g=splitFeat.geometry().convertToType(QgsWkbTypes().LineGeometry)
                # print(splitFeat.geometry())
                # print(g.wkbType())
                # print()
                # print(splitFeat.geometry().wkbType())
                newFeat.setGeometry(g)
                newFeat.setFields(lyr.fields())
                srch_fld_idx = splitLyr.fields().lookupField('Searchable')
                x= splitFeat.setAttribute(srch_fld_idx,bool(splitFeat.attributes()[1:][int(srch_fld_idx)]))
                # print(x)
                newFeat.setAttributes(splitFeat.attributes()[1:])
                # print(newFeat.attributes())
                newFeats.append(newFeat)
        # print(newFeats)
        # print([f.name() for f in newFeats[0].fields()])
        deleteIds = []
        for newId in set(nonUnqFlds):
            exprRslt = QgsExpression("\"id\" = {}".format(newId))
            deleteFeat = lyr.dataProvider().getFeatures(QgsFeatureRequest(exprRslt))
            deleteIds.append([f.id() for f in deleteFeat][0])

        lyr.startEditing()
        # print(len(newFeats))
        # print(QgsFeatureSink.Flag(2))
        # print(QgsFeatureSink.FastInsert)
        # print(newFeats[0].attributes())
        # print(newFeats)
        lyr.dataProvider().addFeatures(newFeats)
        lyr.deleteFeatures(deleteIds)
        # print(bl, feats)
        # print(addFeatBool)
        # QgsProject.instance().removeMapLayer(new_layer)
    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        # self.dlg.pushButton.clicked.connect(lambda: (self.split()))
        icon_path = ':/plugins/SplitRoads/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Roads Splitting Plugin'),
            callback=self.split,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'Road Splitting Plugin'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        self.dlg.show()

        # Run the dialog event loop
        result = self.dlg.exec_()
