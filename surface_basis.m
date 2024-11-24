(* ::Package:: *)

(*
1. Define the degree and knot vectors for both u and v directions.
2. Use BSplineBasis to calculate the basis functions in each direction.
3. Combine these basis functions to get the basis function for the surface.
*)

(* Define the degrees for u and v directions *)
degreeU = 7;
degreeV = 5;

(* Define the knot vectors for u and v directions *)
knotsU = {0.,0.,0.,0.,0.,0.,0.,0.,1.,1.,1.,1.,1.,1.,1.,1.};
knotsV = {0.,0.,0.,0.,0.,0.,1.,1.,1.,1.,1.,1.};

(* 
Parameter values u and v for point on surface
-432.11540229364914, 263.0404685883425, 92.87925745418916`
Can be found in Rhino3D with "EvaluateUVPt".
*)
u = 0.43;
v = 0.19;

(* Calculate the basis functions for u and v *)
basisU = Table[BSplineBasis[{degreeU, knotsU}, i, u], {i, 0, Length[knotsU] - degreeU - 2}]
basisV = Table[BSplineBasis[{degreeV, knotsV}, j, v], {j, 0, Length[knotsV] - degreeV - 2}]

(* The rational B-spline basis function is the product of the basis functions in each direction *)
basisFunctionValue = Outer[Times, basisU, basisV]

(* Output the basis functions *)
basisFunctionValue[[4]][[2]]
basisU[[4]]
basisV[[2]]
basisU[[4]] * basisV[[2]]
(* Note: Indexing the List starts at 1, but input for basis function starts at zero. *)
BSplineBasis[{degreeU, knotsU}, 3, u] * BSplineBasis[{degreeV, knotsV}, 1, v]





(* ::Input:: *)
(**)
