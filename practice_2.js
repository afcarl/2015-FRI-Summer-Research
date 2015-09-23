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

// create a cube
function createCube(x, y, z, size) {
    var mesh = new Mesh3D();
    mesh.quad([x, y, z], [x, y+size, z],
                [x+size, y+size, z], [x+size, y, z]);
    mesh.quad([x, y, z], [x+size, y, z],
                [x+size, y, z+size], [x, y, z+size]);
    mesh.quad([x+size, y, z], [x+size, y+size, z],
                [x+size, y+size, z+size], [x+size, y, z+size]);
    mesh.quad([x, y, z], [x, y, z+size],
                [x, y+size, z+size], [x, y+size, z]);
    mesh.quad([x, y+size, z], [x, y+size, z+size],
                [x+size, y+size, z+size], [x+size, y+size, z]);
    mesh.quad([x, y, z+size], [x+size, y, z+size],
                [x+size, y+size, z+size], [x, y+size, z+size]);
    return mesh;
}

// create two cubes in one mesh
function createTwoCubes() {
    // create a cube using coordinates
    var mesh = new Mesh3D();
    mesh.quad([0, 0, 0], [0, 10, 0], [10, 10, 0], [10, 0, 0]);
    mesh.quad([0, 0, 0], [10, 0, 0], [10, 0, 10], [0, 0, 10]);
    mesh.quad([10, 0, 0], [10, 10, 0], [10, 10, 10], [10, 0, 10]);
    mesh.quad([0, 0, 0], [0, 0, 10], [0, 10, 10], [0, 10, 0]);
    mesh.quad([0, 10, 0], [0, 10, 10], [10, 10, 10], [10, 10, 0]);
    mesh.quad([0, 0, 10], [10, 0, 10], [10, 10, 10], [0, 10, 10]);
    // another cube
    mesh.quad([20, 20, 20], [20, 30, 20], [30, 30, 20], [30, 20, 20]);
    mesh.quad([20, 20, 20], [30, 20, 20], [30, 20, 30], [20, 20, 30]);
    mesh.quad([30, 20, 20], [30, 30, 20], [30, 30, 30], [30, 20, 30]);
    mesh.quad([20, 20, 20], [20, 20, 30], [20, 30, 30], [20, 30, 20]);
    mesh.quad([20, 30, 20], [20, 30, 30], [30, 30, 30], [30, 30, 20]);
    mesh.quad([20, 20, 30], [30, 20, 30], [30, 30, 30], [20, 30, 30]);
    // return both of the cubes in one mesh
    return mesh;
}

function shapeGeneratorEvaluate(params, callback){
    var mesh = createCube(0, 0, 0, 10);
    var cube = createCube(5, 5, 5, 10);
    // subtract cube from mesh
    mesh.subtract(cube, function(mesh) {
        var solid = Solid.make(mesh);
        callback(solid);
    });
}
