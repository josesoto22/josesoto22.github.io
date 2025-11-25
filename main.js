// --- CONFIGURACIÓN DE LA ESCENA ---
const scene = new THREE.Scene();
// CÁMARA (FOV, Aspecto, Cerca, Lejos)
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true }); // Con suavizado de bordes
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Fondo de la escena
scene.background = new THREE.Color(0xf0f0f0); // Gris claro

// Iluminación
const ambientLight = new THREE.AmbientLight(0xffffff, 0.7); // Luz ambiental suave
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
directionalLight.position.set(5, 10, 7.5); // Luz principal
scene.add(directionalLight);

// --- CARGADOR DE OBJ ---
const objLoader = new THREE.OBJLoader();
const objPath = './Real.obj';

objLoader.load(
    objPath,
    // Función cuando el modelo se carga
    function (object) {
        
        // 1. Aplicar un material por defecto
        object.traverse(function (child) {
            if (child.isMesh) {
                // El archivo OBJ pide 'Real.mtl'. 
                // Si no lo tienes, el modelo no tendrá material. 
                // Aplicamos un material simple para que sea visible.
                if (!child.material || child.material.isMeshBasicMaterial) {
                    child.material = new THREE.MeshPhongMaterial({
                        color: 0xaaaaaa, // Gris por defecto
                        side: THREE.DoubleSide
                    });
                }
            }
        });

        // 2. Centrar y dimensionar el objeto para que quepa en la vista
        const box = new THREE.Box3().setFromObject(object);
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());

        // Mover el objeto para centrarlo en (0, 0, 0)
        object.position.sub(center);

        // Calcular la distancia de la cámara
        const maxDim = Math.max(size.x, size.y, size.z);
        const fov = camera.fov * (Math.PI / 180);
        let cameraDistance = Math.abs(maxDim / 2 / Math.tan(fov / 2));
        cameraDistance *= 1.5; // Añadir un margen

        camera.position.z = cameraDistance;
        camera.lookAt(scene.position); 
        
        // 3. Añadir a la escena
        scene.add(object);

        // Hacemos el objeto accesible para la función de animación
        window.loadedObject = object;

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

// --- ANIMACIÓN Y RENDER ---
function animate() {
    requestAnimationFrame(animate);

    // Rotación simple para visualizar el objeto (comenta esta sección si no la quieres)
    if (window.loadedObject) {
        window.loadedObject.rotation.y += 0.005;
    }

    renderer.render(scene, camera);
}
animate();

// --- RESPONSIVIDAD (Ajustar al redimensionar la ventana) ---
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});