var clock = new THREE.Clock();

//RENDERER
var scene = new THREE.Scene();

// Load Camera Perspektive
var camera = new THREE.PerspectiveCamera( 35, window.innerWidth / window.innerHeight, 1, 3000 );
camera.position.set( 0, 0, 15 );

// Load a Renderer
var renderer = new THREE.WebGLRenderer({canvas: document.getElementById('default_canvas'), antialias: true});
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

// Disable Zoom
controls.enableZoom = false;

// Disable Rotation
controls.enableRotate = false;

// Disble Keyboard Control Movements
controls.enabled = false;

// Load Light
var ambientLight = new THREE.AmbientLight( 0xcccccc );
scene.add( ambientLight );


var directionalLight = new THREE.DirectionalLight( 0xffffff );
directionalLight.position.set( 0, 1, 1 ).normalize();
scene.add( directionalLight );


var loader = new THREE.GLTFLoader();
loader.load( '/static/FittingRoom/Models/Bashful.glb',
function ( gltf )
{
    var object = gltf.scene;

    var parts = object.children;

    for (var idx = 0; idx < parts.length; idx++)
        console.log(parts[idx])

    var body = parts[2].children[1];
    body.scale.y = 0.5;
    console.log(body);

    var mixer = new THREE.AnimationMixer(object);

    gltf.animations.forEach((clip) => { mixer.clipAction(clip).play() });

    gltf.scene.scale.set( 2, 2, 5 );
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
