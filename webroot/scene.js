function main() {
    var renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    const fov = 75;
    const aspect = window.innerWidth / window.innerHeight;  // the canvas default
    const near = 0.1;
    const far = 5;
    const camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
    camera.position.z = 3;

    const scene = new THREE.Scene();

    {
        const color = 0xFFFFFF;
        const intensity = 1;
        const light = new THREE.DirectionalLight(color, intensity);
        light.position.set(0, -5, 2);
        scene.add(light);
    }
    var material = new THREE.MeshBasicMaterial();
    const geometry = new THREE.SphereGeometry(1, 32, 32);
    var loader = new THREE.TextureLoader();
    
    loader.load('earthday.jpg', function (texture) {
        

        material.map = texture;
        material.needsUpdate = true;
    });
    var cube = new THREE.Mesh(geometry, material);
    scene.add(cube);

    cube.rotation.z = Math.PI/180 * -23.5;
    function render(time) {
        time *= 0.001;  // convert time to seconds


        cube.rotateOnAxis( new THREE.Vector3(0, 1, 0).normalize(), 0.01  );  
        
        //cube.rotation.y = time;

        renderer.render(scene, camera);

        requestAnimationFrame(render);
    }
    requestAnimationFrame(render);

}

main();