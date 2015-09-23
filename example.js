var Conversions = Core.Conversions;
var Debug = Core.Debug;
var Path2D = Core.Path2D;
var Point2D = Core.Point2D;
var Point3D = Core.Point3D;
var Matrix2D = Core.Matrix2D;
var Matrix3D = Core.Matrix3D;
var Mesh3D = Core.Mesh3D;
var Plugin = Core.Plugin;
var Tess = Core.Tess;
var Sketch2D = Core.Sketch2D;
var Solid = Core.Solid;
var Vector2D = Core.Vector2D;
var Vector3D = Core.Vector3D;

params = [
  {
    "id": "radius",
    "displayName": "Radius",
    "type": "length",
    "rangeMin": 1,
    "rangeMax": 50,
    "default": 20
  }
];

function process(params) {

  var r = params['radius'];
  var angle = 2*Math.PI / 3;
  var h = Math.sqrt(2) * r;

  var sides = [];
  for (var i = 0; i < 3; i++) {
      var x = r * Math.cos(i * angle);
      var y = r * Math.sin(i * angle);
      sides.push([x, y, 0]);
  }
  var peak = [0, 0, h];

  var mesh = new Mesh3D();
  mesh.triangle(sides[0], sides[2], sides[1]);
  mesh.triangle(sides[0], sides[1], peak);
  mesh.triangle(sides[1], sides[2], peak);
  mesh.triangle(sides[2], sides[0], peak);

  return Solid.make(mesh);
}
