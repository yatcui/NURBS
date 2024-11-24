import bspline
import rhinoscriptsyntax as rs


def shift_control_point():
    # Select surface
    surface_id = rs.GetObject("Select surface", rs.filter.surface, preselect=True)
    if surface_id is None:
        print("No surface selected")
        return False
    U = rs.SurfaceDomain(surface_id, 0)
    V = rs.SurfaceDomain(surface_id, 1)
    if not U or not V:
        print("Invalid surface domain")
        return False
    p = rs.SurfaceDegree(surface_id, 0)
    q = rs.SurfaceDegree(surface_id, 1)
    knots = rs.SurfaceKnots(surface_id)
    print(p, q)
    print(U)
    print(V)

    distance = rs.GetReal("Shift surface point by")
    if not distance:
        print("No distance value entered")
        return False
    print("Distance: ", distance)

    # Prompt the user to select a control point
    rs.EnableObjectGrips(surface_id, True)  # Turn on control points
    selected_point_grip = rs.GetObjectGrip("Select a control point") 
    if not selected_point_grip:
        print("No control point selected.") 
        return False
    # Get the coordinates of the selected control point 
    selected_point = rs.ObjectGripLocation(selected_point_grip[0], selected_point_grip[1]) 
    print("Selected control point: ", selected_point)

    # Get points on the surface closest to selected control point
    params = rs.SurfaceClosestPoint(surface_id, selected_point)  # u, v
    if not params:
        print("No closest point on surface found")
        return False
    print("u, v of closest point on surface: ", params)
    closest_point = rs.EvaluateSurface(surface_id, params[0], params[1])  # 3D coordinates
    if not closest_point:
        print("Evaluation of closest point failed")
        return False
    print("Coordinates of closest point: ", closest_point)
    rs.AddPoint(closest_point)  # Show point

    norm_shift_vector = rs.VectorUnitize(rs.VectorCreate(closest_point, selected_point))
    if not norm_shift_vector:
        print("Could not build shift vector")
        return False
    print("Shift vector", norm_shift_vector)

    # Get 2D index of control point
    control_points = rs.SurfacePoints(surface_id)
    if not control_points:
        print("Control point net could not be retrieved")
        return False
    u_count = rs.SurfacePointCount(surface_id)[0]
    v_count = rs.SurfacePointCount(surface_id)[1]
    index_2d = (-1, -1) 
    for i in range(u_count): 
        for j in range(v_count): 
            cp = control_points[i * v_count + j] 
            if rs.Distance(selected_point, cp) < 1e-6: 
                # Small tolerance to account for floating point precision 
                index_2d = (i, j) 
                break 
        if index_2d != (-1, -1): 
            break 
    if index_2d == (-1, -1):
        print("Control point not found in control point net")
        return False
    print("Index of selected control point:", index_2d)

    # B-Spline basis function for control point and u, v for closest point on surface
    # 1st and last knots must be duplicated for basis calculation (NURBS book convention)
    U = [knots[0][0]] + knots[0] + [knots[0][-1]]
    V = [knots[1][0]] + knots[1] + [knots[1][-1]]
    bu = bspline.bspline_basis(p, U, index_2d[0], params[0])
    bv = bspline.bspline_basis(q, V, index_2d[1], params[1])
    buv = bu * bv
    print(f"N_{index_2d[0]},{index_2d[1]}({params[0]}, {params[1]}) = {buv:.6f}")

    translation = norm_shift_vector * distance / buv
    new_location = rs.PointAdd(selected_point, translation)
    print("Translation:", translation)
    rs.ObjectGripLocation(selected_point_grip[0], selected_point_grip[1], new_location)
    
    # Turn off control points for surface. Must take place *after* moving the control point
    # grip to its new location.
    rs.EnableObjectGrips(surface_id, False)

    return True


if __name__ == "__main__":
    if shift_control_point():
        print("Control point shift successful")
    else:
        print("Control point shift failed")
