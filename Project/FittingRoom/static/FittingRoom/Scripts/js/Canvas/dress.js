var foot = document.getElementById("foot").value;
var inches = document.getElementById("inches").value;

var clock = new THREE.Clock();

//RENDERER
var scene = new THREE.Scene();

// Load Camera Perspektive
var camera = new THREE.PerspectiveCamera( 35, window.innerWidth / window.innerHeight, 1, 3000 );
camera.position.set( 0, 0, 15 );

// Load a Renderer
var renderer = new THREE.WebGLRenderer({canvas: document.getElementById('model_canvas'), antialias: true});
renderer.setClearColor( 0xffffff );
renderer.setPixelRatio( window.devicePixelRatio );
renderer.setSize((window.innerWidth / 2), (window.innerHeight / 2) );

// Used to resize the canvas and model
window.addEventListener( 'resize',
function()
{
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize((window.innerWidth / 2), (window.innerHeight / 2));
}, false );

document.body.appendChild(renderer.domElement);

// Load the Orbitcontroller
var controls = new THREE.OrbitControls( camera, renderer.domElement );

var controlSwitch = false;

controls.enableZoom = controlSwitch;
controls.enableRotate = controlSwitch;
controls.enabled = controlSwitch;   // Enable Keyboard controls

// Load Light
var ambientLight = new THREE.AmbientLight( 0xcccccc );
scene.add( ambientLight );


var directionalLight = new THREE.DirectionalLight( 0xffffff );
directionalLight.position.set( 0, 1, 1 ).normalize();
scene.add( directionalLight );


// Load Dress
var texture = new THREE.TextureLoader();
var material = new THREE.MeshBasicMaterial( {
    map: texture.load('/static/FittingRoom/Dresses/dress_01.png'), transparent: true});
var geometry = new THREE.PlaneGeometry(7, 7*.75);
var mesh = new THREE.Mesh(geometry, material);
mesh.position.set(-0.5, -0.5, 1);

var loader = new THREE.GLTFLoader();
loader.load( '/static/FittingRoom/Models/greeting.glb',
function ( gltf )
{
    var object = gltf.scene;

    var mixer = new THREE.AnimationMixer(object);

    gltf.animations.forEach((clip) => { mixer.clipAction(clip).play() });

    if (foot <= 0 && inches <= 0)
        gltf.scene.scale.set( 2, 2, 2 );
    else
    {
        var y_axis = (foot * 0.4) + (inches * 0.033333333);

        if (y_axis < 2.44)
            gltf.scene.scale.set( 2, y_axis, 2 );
        else
        {
            var max_height = 2.43;
            gltf.scene.scale.set(2, max_height, 2);
        }
    }

    gltf.scene.position.x = 0;
    gltf.scene.position.y = -3;
    gltf.scene.position.z = 0;

    function animate()
    {
        requestAnimationFrame( animate );
        var delta3 = clock.getDelta();

        if ( mixer ) mixer.update( delta3 );
        renderer.render( scene, camera );
    }
    animate();

    scene.add( gltf.scene );
});

function render()
{
    renderer.render(scene, camera);
    requestAnimationFrame(render);
}

render();
