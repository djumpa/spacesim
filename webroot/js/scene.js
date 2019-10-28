import {GLTFLoader} from './GLTFLoader.js';
import {OrbitControls} from './OrbitControls.js'
import { NoBlending } from './three.module.js';

var camera, scene, renderer;
var planets = [];

var sat, sun, line, line_earth;
var container;


const MAX_LINE_ELEMENTS = 10;

init();
render();

function init()
{
    container = document.createElement('div');
    document.body.appendChild(container);

    window.addEventListener('resize', onWindowResize, false);

    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 10000, 5e11);
    camera.position.set(0,0,2e11);
    camera.lookAt(new THREE.Vector3(0,0,0));

    scene = new THREE.Scene();

    renderer = new THREE.WebGLRenderer({ antialias:true });
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(window.innerWidth, window.innerHeight);
    container.appendChild(renderer.domElement);

    var controls = new OrbitControls (camera, renderer.domElement);
    controls.update();

    var path = 'res/background/';
    var urls = [path + 'purplenebula_lf.jpg',path + 'purplenebula_rt.jpg',
                path + 'purplenebula_dn.jpg',path + 'purplenebula_up.jpg',
                path + 'purplenebula_ft.jpg',path + 'purplenebula_bk.jpg']

    var background = new THREE.CubeTextureLoader().load(urls);
    background.format = THREE.RGBFormat;
    scene.background = background;


    sun = new THREE.PointLight( 0xffffff, 30, 5e13, 2);
    var geometry = new THREE.SphereGeometry(695510000,32,32);
    var material = new THREE.MeshBasicMaterial({color:0xffffff});
    var path = 'res/sun.jpg';
    material = loadElement(path,material);
    sun.add(new THREE.Mesh(geometry, material));
    
    scene.add( sun );



    geometry = new THREE.SphereGeometry(6371000,32,32);
    planets.push(generatePlanet(365.25, [0, 0, Math.PI/180 * -23.5] , [1.5e11, 0, 0] , sun, geometry, 'phong', 'res/earthday.jpg'));
    scene.add(planets[planets.length - 1].mesh);

    geometry = new THREE.SphereGeometry(1737100,32,32);
    planets.push(generatePlanet(365.25, [0, 0, Math.PI/180 * -23.5] , [1.5e11+384399000, 0, 0] , planets[0].mesh, geometry, 'phong', 'res/moon.jpg'))
    scene.add(planets[planets.length - 1].mesh);

    geometry = new THREE.BoxGeometry(1, 1, 1);
    material = new THREE.MeshPhongMaterial({shininess: 0, color: 0xFFF0E9});
    sat = new THREE.Mesh(geometry, material);
    scene.add(sat);

    geometry = new THREE.Geometry();
    line = new THREE.Line(geometry, new THREE.LineBasicMaterial({ color: 0x00ff00 }));
    for (let index = 0; index < MAX_LINE_ELEMENTS; index++) { 
        line.geometry.vertices.push(new THREE.Vector3(0, 0, 0));   
    }
    scene.add(line)

    geometry = new THREE.Geometry();
    line_earth = new THREE.Line(geometry, new THREE.LineBasicMaterial({ color: 0xff0000 }));
    for (let index = 0; index < MAX_LINE_ELEMENTS; index++) { 
        line_earth.geometry.vertices.push(new THREE.Vector3(0, 0, 0));   
    }
    scene.add(line_earth)
}

function loadElement(path, material)
{
    var loader = new THREE.TextureLoader();
    loader.load(path, function (texture) {
        material.map = texture;
        material.needsUpdate = true;
    });
    return material;
}

/**
 * generates the javascript object containing the parameters of given planet
 */
function generatePlanet(orbitingRate, rotationRate, distance, orbitingCenter, geometry, materialType, texturePath)
{
    var material = getMaterial(materialType, texturePath); 
    var mesh = new THREE.Mesh(geometry,material);

    mesh.position.x = orbitingCenter.position.x + distance[0];
    mesh.position.y = orbitingCenter.position.y + distance[1];
    mesh.position.z = orbitingCenter.position.z + distance[2];

    mesh.rotation.x = rotationRate[0];
    mesh.rotation.y = rotationRate[1];
    mesh.rotation.z = rotationRate[2];



    return {
        orbitingRate: orbitingRate,
        rotationRate: rotationRate,
        distance: distance,
        orbitingCenter: orbitingCenter,
        mesh: mesh,

        update : function(time)
        {
            // Future update of position and orientation should be done here.
        }
    };
}

function getMaterial(type, texturePath)
{
    var material;

    switch(type)
    {
        case 'basic':
            material = new THREE.MeshBasicMaterial(); break;
        case 'lambert':    
            material = new THREE.MeshLambertMaterial({shininess:0}); break;
        case 'phong':
            material = new THREE.MeshPhongMaterial({shininess:0}); break;
        case 'standart':
            material = new THREE.MeshStandardMaterial(); break;       
        default:
            material = new THREE.MeshBasicMaterial({shininess:0}); break;   
    };

    if(texturePath != null)
    {
        var loader = new THREE.TextureLoader();
        loader.load(texturePath, function (texture) {
            material.map = texture;
            material.needsUpdate = true;
        });
    }

    return material;
}

function onWindowResize()
{
    camera.aspect = window.innerWidth/window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth,window.innerHeight);
}


function render(time) {
    
    time *= 0.001;  // convert time to seconds
    
    /*
    Call to update the orientatino and position of planets

    for(var i = 0; i < planets.length; i++)
        planets[i].update(time);
    */
   if (!jQuery.isEmptyObject(ws_data)) {

    //sun.mesh.position.set(ws_data[0].position[0], ws_data[0].position[2], ws_data[0].position[1]); 

    planets[0].mesh.rotateOnAxis( new THREE.Vector3(0, 1, 0).normalize(), 0.007  );  
    planets[0].mesh.position.set(ws_data[1].position[0], ws_data[1].position[2], ws_data[1].position[1]);  

    planets[1].mesh.position.set(ws_data[2].position[0], ws_data[2].position[2], ws_data[2].position[1]);
    planets[1].mesh.rotation.y =  0.1 * time;

    
    for (let index = 0; index < ws_data[2].pos_hist.length; index++) {
         
        line.geometry.vertices[index] = new THREE.Vector3(ws_data[2].pos_hist[index][0], ws_data[2].pos_hist[index][2], ws_data[2].pos_hist[index][1]); 
        line.geometry.verticesNeedUpdate  = true; 
        

        line_earth.geometry.vertices[index] = new THREE.Vector3(ws_data[1].pos_hist[index][0], ws_data[1].pos_hist[index][2], ws_data[1].pos_hist[index][1]);
        line_earth.geometry.verticesNeedUpdate  = true; 
        
    }
    //console.log(line.geometry.vertices)  
        
    
  

   
    sat.position.x = ws_data[3].position[0];
    sat.position.y = ws_data[3].position[2];
    sat.position.z = ws_data[3].position[1];
    sat.rotation.x = time;
    sat.rotation.y = time;
    sat.rotation.z = time;


    //camera.position.set(ws_data[1].position[0], ws_data[1].position[2], (ws_data[1].position[1]+19710000));
    
    renderer.render(scene, camera);
   }
    requestAnimationFrame(render);
}
