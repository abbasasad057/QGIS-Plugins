# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SplitRoads
                                 A QGIS plugin
 This plugin splits selected roads on intersections.
                             -------------------
        begin                : 2018-04-19
        copyright            : (C) 2018 by TPLMaps
        email                : asad.abbas@tplmaps.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load SplitRoads class from file SplitRoads.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .Split_Roads import SplitRoads
    return SplitRoads(iface)
