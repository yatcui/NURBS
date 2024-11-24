"""
NOTE:

- Reference to RhinoCommmon.dll is added by default

- You can specify your script requirements like:

    # r: <package-specifier> [, <package-specifier>]
    # requirements: <package-specifier> [, <package-specifier>]

    For example this line will ask the runtime to install
    the listed packages before running the script:

    # requirements: pytoml, keras

    You can install specific versions of a package
    using pip-like package specifiers:

    # r: pytoml==0.10.2, keras>=2.6.0

- Use env directive to add an environment path to sys.path automatically
    # env: /path/to/your/site-packages/
"""
#! python3

import rhinoscriptsyntax as rs
import scriptcontext as sc

import System
import System.Collections.Generic
import Rhino


surface_id = rs.GetObject("Select surface", rs.filter.surface, preselect=True)
if surface_id is None:
    print("No surface selected")
else:
    
    U = rs.SurfaceDomain(surface_id, 0)
    V = rs.SurfaceDomain(surface_id, 1)
    if U is None or V is None:
        print("Invalid surface domain")
    else:
        print(f"Range in U: {U}")
        print(f"Range in V: {V}")
        print(f"Degree in U = {rs.SurfaceDegree(surface_id, 0)}")
        print(f"Degree in V = {rs.SurfaceDegree(surface_id, 1)}")
        print(f"CP count in U = {rs.SurfacePointCount(surface_id)[0]}")
        print(f"CP count in V = {rs.SurfacePointCount(surface_id)[1]}")
#        points = rs.SurfacePoints(surface_id)
#        for p in points:
#            print(p)
