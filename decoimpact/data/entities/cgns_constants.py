# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""CGNS-specific constants.

This module defines standardized CGNS node type labels and dataset names used
in reading and writing CGNS files. Using these constants ensures consistency
and reduces the risk of typos in CGNS node type strings.
"""

# CGNS node type labels
FLOW_SOLUTION_T = "FlowSolution_t"
DATA_ARRAY_T = "DataArray_t"
GRID_COORDINATES_T = "GridCoordinates_t"
BASE_ITERATIVE_DATA_T = "BaseIterativeData_t"
ZONE_ITERATIVE_DATA_T = "ZoneIterativeData_t"
DESCRIPTOR_T = "Descriptor_t"

# CGNS dataset name for node data values
DATA = " data"
