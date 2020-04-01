var prevDress = [], prevMid = [];

function sampleDropdownBtn()
{
    document.getElementById("SampleDressDropDown").classList.toggle("show");
}

function importDropdownBtn()
{
    document.getElementById("ImportedDressDropDown").classList.toggle("show");
}

const PATH_TO_MODEL = "/static/FittingRoom/Models/";
const PATH_TO_DRESS = "/static/FittingRoom/Dresses/";
var dressOn = false;

const FOOT_TO_INCHES = 12;
const EACH_INCHES = 0.031746032;
const DRESS_INCREMENT = 0.104761905;
const DRESS_POSITION_INCREMENT = 0.0375;
const DRESS_POS_AT_ZERO_INCHES = -3.0125;
const MAX_HEIGHT_IN_INCHES = 75;
const MIN_HEIGHT_IN_INCHES = 36;
const WAIST_INCREMENT = 0.08;
const MAX_WAIST_SIZE = 37;
const MIN_WAIST_SIZE = 20;
const WAIST_WIDTH_INCREMENT = 0.208;
const DRESS_WIDTH_AT_ONE_INCH = 1.84;
const DRESS_WIDTH_INCREMENT = 0.14;
const DRESS_MID_POSITION_PIVOT = 474;
const MIDPOINT_INCREMENT = 0.003333333;
const MID_STARTING_POINT = -0.2;

function displayStatus(heightFoot, heightInInches, waistInches)
{
    if (dressOn) console.log("Wearing Dress: True");
    else console.log("Wearing Dress: False")

    console.log("Height Foot: ", heightFoot);
    console.log("Height Inches: ", heightInInches);
    console.log("Waist Inches: ", waistInches);
}

function fixDressPosition(heightInInches)
{
    if (heightInInches < 1) return DRESS_POS_AT_ZERO_INCHES;
    else return fixDressPosition(heightInInches - 1) + DRESS_POSITION_INCREMENT;
}

function adjustDressWidth(userWaist)
{
    if (userWaist == 0) return 0;
    else if (userWaist == 1) return DRESS_WIDTH_AT_ONE_INCH;
    else return adjustDressWidth(userWaist - 1) + DRESS_WIDTH_INCREMENT;
}

function adjustDressXAxis(midpoint, startingPoint)
{
    var diff = Math.abs(DRESS_MID_POSITION_PIVOT - midpoint);
    var pos = 0;

    if (DRESS_MID_POSITION_PIVOT > midpoint)
    {
        pos = startingPoint + (diff * MIDPOINT_INCREMENT);
        // console.log("Equation: ", startingPoint, " + (", diff, " * ", MIDPOINT_INCREMENT, ") = ", pos);
    }
    else
    {
        pos = startingPoint - (diff * MIDPOINT_INCREMENT);
        // console.log("Equation: ", startingPoint, " - (", diff, " * ", MIDPOINT_INCREMENT, ") = ", pos);
    }

    return pos;
}

function changeHeight(currentDress, midpoint)
{
    var userFoot = document.getElementById("foot").value;
    var userInches = document.getElementById("inches").value;
    var userWaist = document.getElementById("waist").value;
    var heightInInches = parseInt(userFoot * FOOT_TO_INCHES)
        + parseInt(userInches);

    // displayStatus(userFoot, userInches, userWaist);

    // Used to enable/disble OrbitControls
    var controlSwitch = false;

    var clock = new THREE.Clock();
    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera( 35,
        window.innerWidth / window.innerHeight, 1, 3000 );
    var renderer = new THREE.WebGLRenderer(
        {canvas: document.getElementById('default_canvas'), antialias: true});
    var ambientLight = new THREE.AmbientLight( 0xcccccc );
    var directionalLight = new THREE.DirectionalLight( 0xffffff );

    camera.position.set( 0, -3, 15 );
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

    var controls = new THREE.OrbitControls( camera, renderer.domElement );

    controls.enableZoom = controlSwitch;
    controls.enableRotate = controlSwitch;
    controls.enabled = controlSwitch;

    directionalLight.position.set( 0, 1, 1 ).normalize();
    scene.add( ambientLight );
    scene.add( directionalLight );

    if (dressOn)
    {
        // This is to hold the value of the previous dress
        if (prevDress.length == 0)
            prevDress[0] = currentDress;
        else
        {
            if (currentDress != undefined)
                prevDress[0] = currentDress;
        }

        if (prevMid.length == 0)
            prevMid[0] = midpoint;
        else
        {
            if (midpoint != undefined)
                prevMid[0] = midpoint;
        }

        // console.log("prevMid[0]: ", prevMid[0]);

        var dress = prevDress[0];
        var texture = new THREE.TextureLoader();
        var material = new THREE.MeshBasicMaterial( {
            map: texture.load(dress), transparent: true});

        var dressLength = 0, dressWidth = 0;

        if (heightInInches > MAX_HEIGHT_IN_INCHES)
            dressLength = parseInt(MAX_HEIGHT_IN_INCHES) * DRESS_INCREMENT;
        else if (heightInInches < MIN_HEIGHT_IN_INCHES)
            dressLength = parseInt(MIN_HEIGHT_IN_INCHES) * DRESS_INCREMENT;
        else
            dressLength = parseInt(heightInInches) * DRESS_INCREMENT;

        if (userWaist > MAX_WAIST_SIZE)
            dressWidth = adjustDressWidth(MAX_WAIST_SIZE);
        else if (userWaist < MIN_WAIST_SIZE)
            dressWidth = adjustDressWidth(MIN_WAIST_SIZE);
        else
            dressWidth = adjustDressWidth(userWaist);

        var geometry = new THREE.PlaneGeometry(dressWidth, (dressLength)*.765);

        // console.log("parseInt(heightInInches)", parseInt(heightInInches));
        // console.log("DRESS_INCREMENT", DRESS_INCREMENT);
        // console.log("Dress Length: ", dressLength);
        // console.log("Dress Width: ", dressWidth);
        var mesh = new THREE.Mesh(geometry, material);

        var yPos = 0;
        var xPos = adjustDressXAxis(prevMid[0], MID_STARTING_POINT);

        if (heightInInches > MAX_HEIGHT_IN_INCHES)
            yPos = fixDressPosition(MAX_HEIGHT_IN_INCHES);
        else
            yPos = fixDressPosition(heightInInches);

        mesh.position.set(xPos, yPos, 1.1);
        // console.log("xPos: ", xPos);
        // console.log("yPos: ", yPos);
    }

    var model = ((!dressOn)? PATH_TO_MODEL.concat("Bashful.glb")
        : PATH_TO_MODEL.concat("Idle_State_bodyless.glb") );
    var loader = new THREE.GLTFLoader();
    loader.load( model,
    function ( gltf )
    {
        var object = gltf.scene;
        var mixer = new THREE.AnimationMixer(object);

        gltf.animations.forEach((clip) => { mixer.clipAction(clip).play() });

        var height = 0, defaultValue = 2;
        var waist = 0;

        if (userFoot == "" || userInches == ""
            || userFoot == undefined || userInches == undefined
            || userWaist == undefined || userWaist == "")
            {
                alertEmptyBox(userFoot, userInches, userWaist);
                height = defaultValue;
            }
        else
        {
            var maxHeight = 2.3809524, minHeight = 1.142857152;
            var maxWaistSize = 3, minWaistSize = 1.6;

            if (heightInInches > MAX_HEIGHT_IN_INCHES)
                height = maxHeight;
            else if (heightInInches < MIN_HEIGHT_IN_INCHES)
                height = minHeight;
            else
                height = (heightInInches * EACH_INCHES);

            if (userWaist > MAX_WAIST_SIZE)
                waist = maxWaistSize;
            else if (userWaist < MIN_WAIST_SIZE)
                waist = minWaistSize;
            else
                waist = (userWaist * WAIST_INCREMENT);

            // console.log("userFoot: ", userFoot);
            // console.log("FOOT_TO_INCHES: ", FOOT_TO_INCHES);
            // console.log("heightInInches: ", heightInInches);
            // console.log("Height Formula: ", heightInInches, " * ", EACH_INCHES);
            // console.log("Height: ", height);
            // console.log("Waist Size: ", waist);
        }

        gltf.scene.scale.set( waist, height, waist );
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
        if (dressOn) scene.add( mesh );
    });

    function render()
    {
        renderer.render(scene, camera);
        requestAnimationFrame(render);
    }
    render();
}

function alertEmptyBox(userFoot, userInches, userWaist)
{
    var userEnterFoot = ((userFoot == "" || userFoot == undefined)? false : true );
    var userEnterInches = ((userInches == "" || userInches == undefined)? false : true );
    var userEnterWaist = ((userWaist == "" || userWaist == undefined)? false : true );

    if (!userEnterWaist)
        alert("Please enter your waist size in inches")
    if (!userEnterFoot)
        alert("Please enter your height in feet");
    if (!userEnterInches)
        alert("Please enter your height in inches");
}

function findIDValue(dress, keysList, arrLength)
{
    var currentDress = undefined;
    var idx = 0;
    var foundDress = false;

    while (!foundDress && idx < arrLength)
    {
        if (dress.getAttribute('id') == keysList[idx])
        {
            currentDress = document.getElementById(keysList[idx]).value;
            foundDress = true;
        }
        else
            idx++;
    }

    return currentDress;
}

function dressMidpoint(value, keysList, valuesList, arrLength)
{
    var midpoint = 0, idx = 0;
    var foundMatchId = false;

    while (!foundMatchId && idx < arrLength)
    {
        if (value.getAttribute('id') == keysList[idx])
        {
            midpoint = valuesList[idx];
            foundMatchId = true;
        }
        else
            idx++;
    }

    return midpoint;
}

function wearSampleDress(value)
{
    dressOn = true;

    var sDressList = {{ js_sample_dresses_data | safe }};
    var sKeys = Object.keys(sDressList);
    var arrLength = sKeys.length;
    var currentDress = findIDValue(value, sKeys, arrLength);

    var sDressMidpointList = {{ js_sample_dresses_midpoint_data | safe }};
    var sMidpointKeys = Object.keys(sDressMidpointList);
    var sMidpointValues = Object.values(sDressMidpointList);
    var midpointArrLength = sMidpointKeys.length;
    var midpoint = dressMidpoint(value, sMidpointKeys, sMidpointValues, midpointArrLength);

    // console.log("Dress: ", currentDress);
    changeHeight(currentDress, midpoint);
}

function wearUploadedDress(value)
{
    dressOn = true;

    var uDressList = {{ js_uploaded_dresses_data | safe }};
    var uKeys = Object.keys(uDressList);
    var currentDress = undefined;
    var arrLength = uKeys.length;
    var currentDress = findIDValue(value, uKeys, arrLength);

    var uDressMidpointList = {{ js_uploaded_dresses_midpoint_data | safe }};
    var uMidpointKeys = Object.keys(uDressMidpointList);
    var uMidpointValues = Object.values(uDressMidpointList);
    var midpointArrLength = uMidpointKeys.length;
    var midpoint = dressMidpoint(value, uMidpointKeys, uMidpointValues, midpointArrLength);

    // console.log("Dress: ", currentDress);
    changeHeight(currentDress, midpoint);
}
