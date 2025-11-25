// main.js

// --- CONFIGURACIÓN DE LA ESCENA Y CÁMARA ---
const scene = new THREE.Scene();

// CÁMARA (FOV, Aspecto, Cerca, Lejos)
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

// RENDERER
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Fondo de la escena (Gris claro)
scene.background = new THREE.Color(0xf0f0f0); 

// --- ILUMINACIÓN ---
// Luz ambiental suave para evitar sombras completamente oscuras
const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
scene.add(ambientLight);

// Luz direccional (como un sol) para dar volumen
const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
directionalLight.position.set(5, 10, 7.5); // Posicionada para iluminar desde arriba/frente
scene.add(directionalLight);

// --- CONTROLES DE ÓRBITA (Para mover el modelo con el ratón) ---
// Vincula los controles a la cámara y al elemento DOM del renderizador
const controls = new THREE.OrbitControls(camera, renderer.domElement);


// --- CARGADOR DE OBJ ---
const objLoader = new THREE.OBJLoader();
const objPath = './Real.obj';

objLoader.load(
    objPath,
    // Función cuando el modelo se carga
    function (object) {
        
        // --- 1. Manejo de Materiales ---
        object.traverse(function (child) {
            if (child.isMesh) {
                // Aplica un material por defecto si el OBJ no tiene MTL o si el material no es válido
                if (!child.material || child.material.isMeshBasicMaterial) {
                    child.material = new THREE.MeshPhongMaterial({
                        color: 0xaaaaaa, // Color gris por defecto
                        side: THREE.DoubleSide,
                        shininess: 30 // Para un poco de brillo
                    });
                }
            }
        });

        // --- 2. Centrado y Posicionamiento Automático ---
        const box = new THREE.Box3().setFromObject(object);
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());

        // Mover el objeto para que su centro esté en el origen (0, 0, 0)
        object.position.sub(center);

        // Calcular la distancia necesaria de la cámara para que el objeto quepa en la vista
        const maxDim = Math.max(size.x, size.y, size.z);
        const fov = camera.fov * (Math.PI / 180);
        let cameraDistance = Math.abs(maxDim / 2 / Math.tan(fov / 2));
        cameraDistance *= 1.5; // Añadir un margen

        camera.position.z = cameraDistance;
        camera.lookAt(scene.position); 
        
        // Establecer el punto de foco de los OrbitControls en el centro del objeto
        controls.target.copy(scene.position); 
        controls.update();
        
        // --- 3. Añadir a la escena ---
        scene.add(object);

        console.log("Modelo Real.obj cargado y configurado exitosamente.");
    },
    // Función de progreso (opcional)
    function (xhr) {
        // Muestra el progreso de la carga en la consola
        console.log((xhr.loaded / xhr.total * 100).toFixed(2) + '% cargado');
    },
    // Función de error
    function (error) {
        console.error('Error al cargar el archivo OBJ:', error);
    }
);

// --- ANIMACIÓN Y RENDER ---
function animate() {
    // Solicita al navegador que prepare el siguiente frame
    requestAnimationFrame(animate);

    // Actualiza los controles de órbita para aplicar la interacción del mouse
    controls.update(); 

    // Renderiza la escena
    renderer.render(scene, camera);
}
animate();

// --- RESPONSIVIDAD (Ajustar al redimensionar la ventana) ---
window.addEventListener('resize', () => {
    // Actualiza el aspecto de la cámara
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    
    // Ajusta el tamaño del renderizador
    renderer.setSize(window.innerWidth, window.innerHeight);
});
