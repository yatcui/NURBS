Import["497.igs"]

spoiler = Import["golf5_kotfluegel_vorn.igs"]

surfaces = Import["golf5_kotfluegel_vorn.igs","SplineRegion"];

surfaces[[1]]

surf = Graphics3D[surfaces[[1]]]

cpts = surfaces[[1]][[1]];

Show[Graphics3D[{PointSize[Medium], Red, Map[Point, cpts], Gray, 
   Line[cpts], Line[Transpose[cpts]]}], surf]
