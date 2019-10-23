function main() {
    var renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    const fov = 75;
    const aspect = window.innerWidth / window.innerHeight;  // the canvas default
    const near = 0.1;
    const far = 500;
    const camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
    camera.position.z = 60;
    camera.position.y = 0;

    const scene = new THREE.Scene();

    {
        const color = 0xFFF0E9;
        const intensity = 3;
        const light = new THREE.DirectionalLight(color, intensity);
        light.position.set(10, 0, 4);
        scene.add(light);
    }
    var material = new THREE.MeshPhongMaterial({shininess: 0});
 
    const geometry = new THREE.SphereGeometry(10, 32, 32);
    
    var loader = new THREE.TextureLoader();
    
    loader.load('earthday.jpg', function (texture) {
        

        material.map = texture;

        material.needsUpdate = true;
    });
    var cube = new THREE.Mesh(geometry, material);
    scene.add(cube);

    const sat_geometry = new THREE.BoxGeometry(1, 1, 1);
    var sat_material = new THREE.MeshPhongMaterial({shininess: 0, color: 0xFFF0E9});
    var sat = new THREE.Mesh(sat_geometry, sat_material);

    scene.add(sat);

    

    cube.rotation.z = Math.PI/180 * -23.5;
    function render(time) {
        time *= 0.001;  // convert time to seconds

        if (!jQuery.isEmptyObject(ws_data)) {

        
        cube.rotateOnAxis( new THREE.Vector3(0, 1, 0).normalize(), 0.007  );  
        sat.position.x = ws_data[0].position[0]
        sat.position.y = ws_data[0].position[1]
        sat.position.z = ws_data[0].position[2]
        sat.rotation.x = time;
        sat.rotation.y = time;
        sat.rotation.z = time;
        //cube.rotation.y = time;

        renderer.render(scene, camera);
        }
        requestAnimationFrame(render);
    }
    requestAnimationFrame(render);

}

main(); 

