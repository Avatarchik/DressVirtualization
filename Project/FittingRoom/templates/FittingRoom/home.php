<?php
    session_start();
?>

<!DOCTYPE HTML>
<html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="stylesheet" href="/static/FittingRoom/CSS/main.css" />
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" />

        {% if title %}
            <title>Perfect-Fit - {{ title }}</title>
        {% else %}
            <title>Perfect-Fit - Dress Visualization</title>
        {% endif %}
    </head>

    <body>
        <script src = "https://cdnjs.cloudflare.com/ajax/libs/three.js/109/three.js"></script>
        <script src = "https://cdnjs.cloudflare.com/ajax/libs/three.js/109/three.min.js"></script>

        <script type="text/javascript" src = "/static/FittingRoom/Scripts/js/Three/OrbitControls.js"></script>
        <script type="text/javascript" src = "/static/FittingRoom/Scripts/js/Three/GLTFLoader.js"></script>

        <!-- Header -->
        <header id="header">
            <nav class="left">
                <a href="#menu">
                    <span>
                        <div>
                            <div style = "width: 25px; height:4px; background-color: #25a2c3; margin: 5px; margin-top: 25%;"></div>
                            <div style = "width: 25px; height:4px; background-color: #25a2c3; margin: 5px;"></div>
                            <div style = "width: 25px; height:4px; background-color: #25a2c3; margin: 5px;"></div>
                        </div>
                    </span>
                </a>
            </nav>
            <a href="{% url 'FittingRoom-Home' %}"><img style = "width: 100; height:100%;" src = "/static/FittingRoom/Images/logo.png"></a>
            <a href="{% url 'FittingRoom-Contact' %}"></a>
            <nav class="right">
                <a href="{% url 'User-Profile' %}" class = "button alt">{{ user.username }}</a>
                <a href="{% url 'User-Logout' %}" class = "button alt">Logout</a>
            </nav>
        </header>

        <!-- Menu -->
        <nav id="menu">
            <h1>Menu</h1>
            <ul class="links">
                <li><a href="/">Home</a></li>
                <li><a href="{% url 'FittingRoom-Contact' %}">Contact</a></li>
            </ul>
            <ul class="actions vertical">
                <li><a href="{% url 'User-Profile' %}" class = "button fit">{{ user.username }}</a></li>
                <li><a href="{% url 'User-Logout' %}" class = "button fit">Logout</a></li>
            </ul>
        </nav>

        <div class="center">
            <form class="center" method="post">
                {% csrf_token %}
                <script type="text/javascript">
                    function changeHeight()
                    {
                        var foot = document.getElementById("foot").value;
                        var inches = document.getElementById("inches").value;

                        var clock = new THREE.Clock();

                        //RENDERER
                        var scene = new THREE.Scene();

                        // Load Camera Perspektive
                        var camera = new THREE.PerspectiveCamera( 35, window.innerWidth / window.innerHeight, 1, 3000 );
                        camera.position.set( 0, -3, 15 );

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

                        // Disable Keyboard Control Movements
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
                    }
                </script>

                <canvas id = "default_canvas" class = "center"></canvas>
                <script type="text/javascript" src = "/static/FittingRoom/Scripts/js/Canvas/home.js"></script>
                <h4>Enter your Height information</h4>
                <table>
                    <tr>
                        <td><label for="Foot">Foot:</label></td>
                        <td><input name = "Foot" type="text" id = "foot" style = "text-align: center;"></td>
                        <td><label for="Inches">Inches:</label></td>
                        <td><input name = "Inches" type="text" id = "inches" style = "text-align: center;"></td>
                    </tr>
                </table>
                <button type="button" onclick = "changeHeight()" class = "button alt">Update Model</button>
            </form>
        </div>

        <div id = "dress_library" style = "text-align: center;">
            <button type="button" name="button">Dresses</button>
            <script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
            <script type="text/javascript">
                $(function() {
                    $('button').click(function() {
                        $.ajax({
                            url: '{% url "FittingRoom-Dress-Library" %}',
                            type: 'POST',
                            success: function() {
                                var success = "No Errors encountered.";
                                console.log(success);
                            },
                            error: function() {
                                var fail = "Unknown error(s) encountered.";
                                console.log(fail);
                            }
                        })
                    });
                });
            </script>
        </div>

        <div id = "images">
            <!--<input type="button" value = "Load Dresses" onclick = "callForImages()"/>-->
            <script>
                var imageContainer = document.getElementById("images");

                function callForImages()
                {
                    var httpRequest = (window.XMLHttpRequest) ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
                    httpRequest.onload = function() {
                        var dataStr = JSON.stringify(httpRequest.responseText);
                        var result = JSON.parse(dataStr);
                        loadImages(result);
                    }
                    try
                    {
                        httpRequest.open("GET", "/static/FittingRoom/Scripts/php/getImages.php", true);
                        httpRequest.send(null);
                    }
                    catch(e)
                    {
                        console.log("Error");
                    }
                }

                function loadImages(images)
                {
                    for (var idx = 0; idx < images.length; idx++)
                    {
                        var newImage = document.createElement("img");
                        newImage.setAttribute("src", images[idx]);
                        imageContainer.appendChild(newImage);
                    }
                }
            </script>
        </div>

        <!-- Scripts -->
        <script src="/static/FittingRoom/Scripts/js/jquery.min.js"></script>
        <script src="/static/FittingRoom/Scripts/js/jquery.scrolly.min.js"></script>
        <script src="/static/FittingRoom/Scripts/js/skel.min.js"></script>
        <script src="/static/FittingRoom/Scripts/js/util.js"></script>
        <script src="/static/FittingRoom/Scripts/js/main.js"></script>
    </body>
</html>
