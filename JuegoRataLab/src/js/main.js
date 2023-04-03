
// Creación variables
var scene = null,
    camera = null,
    renderer = null,
    controls = null,
    modelLoad= null,
    modelObject=null,
    modelMaterial=null,
    diamante=null,
    lightAmbiente=null,
    stats=null,
    sound3d = null,
    win = false,
    romper = false;
    
var objetoJaula=null,
    objetoLab=null,
    meshJaula=null;

var playerBody=null,
    JaulaBody=null;
    
var myPlayer=null, 
    input={left:0,right:0,up:0,down:0}, 
    rotSpeed = 0.05, 
    speed = 0.5,
    myCollectibles=[],
    collectible=null,
    points=0,
    n=180; 

const world = new CANNON.World({
    //gravity:0
});

const timeStep = 1/60;

// Inicializar la scene
function startScene() {
    initScene();
    crearMundo();
}

function initScene() {
    // Scene, Camera, Renderer 
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xC6F8FC);
    camera = new THREE.PerspectiveCamera(
        75,                                       
        window.innerWidth / window.innerHeight,   
        0.1,                                      
        1000);                                    

    renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('app') });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);
     
    const container = document.getElementById('container');
    stats = new Stats();
    container.appendChild(stats.domElement);
    
    camera.position.set(-1.01, 0, -6);
    
    createPlayer();
    crearLuz();
    initSound3D();
}

function crearMundo(){
    var rutaModelo='./src/modelos/LabRat/';
    var rutaMTL='Laberinto2.mtl';
    var rutaOBJ='Laberinto2.obj';
    loadLaberinto_MTL(rutaModelo, rutaMTL, rutaOBJ); //carga el modelo y lo pone en escena como objetoLab

    var rutaModelo='./src/modelos/jaula/';
    var rutaMTL='JaulaModel.mtl';
    var rutaOBJ='JaulaModel.obj';
    loadJaula_MTL(rutaModelo, rutaMTL, rutaOBJ); //carga el modelo y lo pone en escena como objetoJaula

    modelObject = new THREE.ConeGeometry();
    modelMaterial = new THREE.MeshBasicMaterial({color:0x81FFF7});
    diamante = new THREE.Mesh(modelObject,modelMaterial);
    
    diamante.rotateX(Math.PI);
    diamante.position.x = -27;
    diamante.position.y = camera.position.y;
    diamante.position.z = -9;

    diamante.scale.set(2.5,2.5,2.5);

    scene.add(diamante);
}

function crearLuz(){
    const light = new THREE.HemisphereLight( 0xffffbb, 0x080820, 3);
    light.position.set(10,-50,0);
    scene.add( light );

    const lightPoint = new THREE.PointLight( 0xFFFFFF, 3, 50 );
    lightPoint.position.set(-27, camera.position.y, -9);
    scene.add(lightPoint);
}

function initSound3D() {
    sound3d = new Sound(["./src/audio/Shiny.mp3"],70,scene,{
        debug:false,
        position: {x:-27,y:camera.position.y,z:-9},
        volume: 0.3,
        loop:true
    });
}

function CrearCollectibles(){

   initCollectible(-60, -82);
   initCollectible(-22, 31);
   initCollectible(82, 105);
   initCollectible(108, 80);
   initCollectible(108, -59);
   initCollectible(55, 47);
}

function initCollectible (pos1, pos2){
    console.log("Crear elementos");
    const geometry = new THREE.BoxGeometry( 4, 4, 4 );
	const textureLoader2 = new THREE.TextureLoader();
	const texture = textureLoader2.load('./src/img/texturaQueso.jpg');
	materialCubo= new THREE.MeshStandardMaterial({map:texture})
    collectible = new THREE.Mesh( geometry, materialCubo);

    collectible.name = "modelToPick"+Math.floor(Math.random()*60);
    collectible.position.y =0;
    collectible.position.x = pos1;
    collectible.position.z = pos2;

    myCollectibles.push(collectible,diamante); //Pone todos los collectibles dentro del arreglo

    scene.add( collectible );
    scene.add(diamante);
}

function CollisionAnimate(){
    var originPoint = myPlayer.position.clone();

    for (var vertexIndex = 0; vertexIndex < myPlayer.geometry.vertices.length; vertexIndex++){
    var localVertex = myPlayer.geometry.vertices[vertexIndex].clone();
    var globalVertex = localVertex.applyMatrix4( myPlayer.matrix );
    var directionVector = globalVertex.sub( myPlayer.position );

    var ray = new THREE.Raycaster( originPoint, directionVector.clone().normalize() );
    var collisionResults = ray.intersectObjects( myCollectibles );
        if (collisionResults.length > 0 && collisionResults[0].distance < directionVector.length()){
            console.log("take element: "+collisionResults[0].object.name);
            points++;
            collisionResults[0].object.visible = false;
            document.getElementById("points").innerHTML = points;
            if(points<7){ //Condicion para que no se coma el diamante
                var pointSound = document.getElementById("sonidoPuntos");
                pointSound.volume=0.4;
                pointSound.play();
            }

            if(points == 6){
                //ROMPE LA JAULA
                document.getElementById("jaulaAbre").play();
                romper=true; //Por alguna razon, quita la jaula tambien
                             //Creemos que es porque la jaula esta vinculada con las bounding boxes
                RemoveJaula();
            }
            if (points>=7 ){
                //WIN
                win = true;
                document.getElementById("WinPanel").style.display="block";
                document.getElementById("songBack").pause();
                document.getElementById("WinMusic").play();
                sound3d = null;
            }
        }
    }
}

function CollisionJaula(){ //Al final no usamos CANNON.js :P

    if(romper==false){
    firstBB = new THREE.Box3().setFromObject(myPlayer);
    secondBB = new THREE.Box3().setFromObject(meshJaula);

    var collisionJal = firstBB.intersectsBox(secondBB); //Bounding Boxes detectan colision Jaula-Jugador

    if(collisionJal == true){
        console.log("PROHIBIDO");
        if(myPlayer.position.z <7 && myPlayer.position.z > -26){ 
            if(myPlayer.position.x<-39){
                //Si player.z esta entre <=3 y >=-21, la 3ra condicion para diferenciarlo del otro lado de jaula
                myPlayer.position.x = myPlayer.position.x - 1;
            }else{
                myPlayer.position.x = myPlayer.position.x + 1;
            }
        }
        
        if(myPlayer.position.x > -39 && myPlayer.position.x < -15){ 
            if(myPlayer.position.z <-26){
                //Si player.x >=-39 y <=-15, la tercera condicion para dif. del otro lado de la jaula
                myPlayer.position.z = myPlayer.position.z - 1;
            }else{
            myPlayer.position.z = myPlayer.position.z + 1;
            }
        }

        //SOLO PARA ESTA CONDENADA ESQUINA SPEEDRUN STRATEGY %100 SUCCESS RATE TRY IT BEFORE THEY PATCH IT
        //dev note: we couldn't patch it
        if(myPlayer.position.x <=-39 && myPlayer.position.z<=-26){
            console.log(":(");
            myPlayer.position.z = myPlayer.position.z + 1;
            myPlayer.position.x = myPlayer.position.x + 1;
        }
    }
    }
}

function RemoveJaula(){
    scene.remove(modelLoad);
    scene.remove(meshJaula);
}

function animate() {
    requestAnimationFrame(animate);
    world.step(timeStep);
    stats.update();
    diamante.rotation.y += 0.02;
    //myCollectibles.rotation.y += 0.02; no lo descomenten porque hace boom
    sound3d.play(); //sonido 3d
    sound3d.update(camera);
    movementPlayer();
    camera.position.copy(myPlayer.position);
    CollisionAnimate();
    CollisionJaula();
    renderer.render(scene, camera);
 
}

function loadLaberinto_MTL(generalPath, pathMTL, pathOBJ){
    var mtlLoader = new THREE.MTLLoader();
    mtlLoader.setTexturePath(generalPath);
    mtlLoader.setPath(generalPath);
    mtlLoader.load(pathMTL, function (materials) {

        materials.preload();

        var objLoader = new THREE.OBJLoader();
        objLoader.setMaterials(materials);
        objLoader.setPath(generalPath);
        objLoader.load(pathOBJ, function (objetoLab) {

            modelLoad = objetoLab;
            scene.add(objetoLab);
            objetoLab.scale.set(0.2, 0.1, 0.2);
            objetoLab.position.y = -60;
            objetoLab.position.x = 0;
            objetoLab.position.z = 0;
        });
    });
}                       //Tenemos que cargar los dos objetos en funciones separadas para poder llamarlas
                        //en escena independientemente y poder darles colisiones individuales

function loadJaula_MTL(generalPath, pathMTL, pathOBJ){ 
    var mtlLoader = new THREE.MTLLoader();
    mtlLoader.setTexturePath(generalPath);
    mtlLoader.setPath(generalPath);
    mtlLoader.load(pathMTL, function (materials) {

        materials.preload();

        var objLoader = new THREE.OBJLoader();
        objLoader.setMaterials(materials);
        objLoader.setPath(generalPath);
        objLoader.load(pathOBJ, function (objetoJaula) {

            modelLoad = objetoJaula;

            scene.add(objetoJaula);
            objetoJaula.scale.set(0.06, 0.06, 0.06);
            objetoJaula.position.x = -25;
            objetoJaula.position.y = -5;
            objetoJaula.position.z = 15;

        });
    });

    var geometry = new THREE.BoxGeometry(12.5,12.5,12.5);
    var material= new THREE.MeshBasicMaterial({color:0x00ff00, wireframe:false, visible:false});
    meshJaula= new THREE.Mesh(geometry,material);

    meshJaula.position.set(-27,0,-9);
    scene.add(meshJaula);
}

function StartJuego(){
    animate();
    alert("El juego va a comenzar"+"\nAndres Correa - Valentina Cuellar");
    document.getElementById("menuPanel").style.display="none";
    var musicBG = document.getElementById("songBack");
    musicBG.volume=0.18;
    musicBG.play();
    contadorTiempo();
    CrearCollectibles();
}

function contadorTiempo(){
  var l= document.getElementById("tiempo");

  window.setInterval(function(){
      l.innerHTML=n;
      if(n>0){
          n--;
      }
      else if (n == 0 && win == false) {
          document.getElementById("LostPanel").style.display="block";
          document.getElementById("songBack").pause();
          document.getElementById("LoseMusic").play();
          sound3d = null;
      }
  },1000)
}

function createPlayer(){
    var geometry = new THREE.BoxGeometry(1,1,1);
    var material= new THREE.MeshBasicMaterial({color:0x00ff00, visible:false});
    myPlayer= new THREE.Mesh(geometry,material);
    myPlayer.position.set(camera.position.x,camera.position.y,camera.position.z); //MESH JUGADOR

    // playerBody = new CANNON.Body({ //BODY JUGADOR
    //     shape: new CANNON.Box(new CANNON.Vec3(1.5,1.5,1.5)),
    //     //type: CANNON.Body.KINEMATIC
    //     position: new CANNON.Vec3(0,0,0)
    // });
    // world.addBody(playerBody);
    scene.add(myPlayer);
}

function movementPlayer(){
    if(input.right == 1){ // Camara Rota
        camera.rotation.y -= rotSpeed;
        myPlayer.rotation.y -= rotSpeed;
    }else if(input.left == 1){ // Camara Rota
        camera.rotation.y += rotSpeed;
        myPlayer.rotation.y += rotSpeed;
    }else if(input.up == 1){ // Camara Avanza
        camera.position.z -= Math.cos(camera.rotation.y) * speed;
        camera.position.x -= Math.sin(camera.rotation.y) * speed;
        myPlayer.position.z -= Math.cos(camera.rotation.y) * speed;
        myPlayer.position.x -= Math.sin(camera.rotation.y) * speed;
    }else if(input.down == 1){ // Camara Avanza
        camera.position.z += Math.cos(camera.rotation.y) * speed;
        camera.position.x += Math.sin(camera.rotation.y) * speed;
        myPlayer.position.z += Math.cos(camera.rotation.y) * speed;
        myPlayer.position.x += Math.sin(camera.rotation.y) * speed;
    }
    
}

window.addEventListener('keydown',function(e){ 
    switch(e.keyCode){
     case 68: //derecha
     input.right=1;
     console.log("derecha");
     break;
     case 65: //izquierda
     input.left=1;
     console.log("izquierda");
     break;
     case 87: //arriba
     console.log("arriba");
     input.up=1;
     break;
     case 83:
     input.down =1;
     console.log("abajo");
     break;
     case 67: //Al presionar C obtiene las coordenadas de player
     console.log("posicion X: "+ myPlayer.position.x+" Z: "+myPlayer.position.z);
     case 27:
     this.location.reload();
    }

});
window.addEventListener('keyup',function (e) { //Suelta la tecla
    switch (e.keyCode) {
        case 68: // Derecha
            input.right = 0;
        break;
        case 65: // Izquierda
            input.left = 0;
        break;
        case 87: // Arriba
            input.up = 0;
        break;
        case 83: // Abajo
            input.down = 0;
        break;
    }
});

