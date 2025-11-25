// --- CONFIGURACIÓN DE LA ESCENA Y CÁMARA ---
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

scene.background = new THREE.Color(0xf0f0f0); 

// Iluminación
const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
directionalLight.position.set(5, 10, 7.5);
scene.add(directionalLight);

// --- 🎯 NUEVO: CONTROLES DE ÓRBITA ---
const controls = new THREE.OrbitControls(camera, renderer.domElement);
// Opcional: configurar límites de zoom o movimiento
// controls.enableDamping = true; // Para un movimiento más suave (requiere .update() en el loop)
// controls.dampingFactor = 0.05;

// --- CARGADOR DE OBJ ---
const objLoader = new THREE.OBJLoader();
const objPath = './Real.obj';

objLoader.load(
    objPath,
    // Función cuando el modelo se carga
    function (object) {
        
        // Aplicar material por defecto si no hay MTL
        object.traverse(function (child) {
            if (child.isMesh) {
                if (!child.material || child.material.isMeshBasicMaterial) {
                    child.material = new THREE.MeshPhongMaterial({
                        color: 0xaaaaaa, 
                        side: THREE.DoubleSide
                    });
                }
            }
        });

        // Centrar y dimensionar el objeto
        const box = new THREE.Box3().setFromObject(object);
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());

        object.position.sub(center);

        const maxDim = Math.max(size.x, size.y, size.z);
        const fov = camera.fov * (Math.PI / 180);
        let cameraDistance = Math.abs(maxDim / 2 / Math.tan(fov / 2));
        cameraDistance *= 1.5; 

        camera.position.z = cameraDistance;
        camera.lookAt(scene.position); 
        
        // 🎯 IMPORTANTE: Hacer que los controles miren al centro del objeto
        controls.target.copy(center); // Establece el punto de foco de los controles
        controls.update();
        
        scene.add(object);

        console.log("Modelo Real.obj cargado exitosamente.");
    },
    // Función de progreso (opcional)
    function (xhr) {
        console.log((xhr.loaded / xhr.total * 100) + '% cargado');
    },
    // Función de error
    function (error) {
        console.error('Error al cargar el archivo OBJ:', error);
    }
);

// --- ANIMACIÓN Y RENDER (MODIFICADA) ---
function animate() {
    requestAnimationFrame(animate);

    // 🎯 NUEVO: Actualiza los controles en cada cuadro
    // controls.update(); // SOLO si usas controls.enableDamping = true;
    controls.update(); // Actualiza siempre para cualquier cambio en la entrada del usuario

    // NO necesitamos la rotación automática si el usuario va a moverlo
    // if (window.loadedObject) {
    //     window.loadedObject.rotation.y += 0.005; 
    // }

    renderer.render(scene, camera);
}
animate();

// --- RESPONSIVIDAD ---
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});
