## Challenge MercadoLibre

Script que levanta los correos de gmail que tengan en su asunto o cuerpo la palabra "**devops**" y los almacena en una base de datos.

-----

### Requisitos

Tener instalado:

 - Docker-compose
 - Python3 y pip3
 - google-api-python-client
 - google-auth-httplib2
 - google-auth-oauthlib

### Funcionamiento

En el directorio raiz hay un archivo *docker-compose.yaml*  que crea el ambiente y descarga las imagenes necesarias para que pueda correr en cualquier equipo.

Levanta 3 contenedores, uno para la base de datos, otro para el adminer para poder ver los registros en las bases de datos y otro para correr python y todos los modulos necesarios.

Al ejecutar docker compose, se levantan los contenedores y se corre automaticamente el script **python/scrap-gmail.py**

### Como correrlo

Clonar el repositorio, guardar el archivo credentials.json dentro e instalar los modulos necesarios con pip3

    pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

Luego corremos este archivo para poder autorizar al script *scrap-gmail.py&#8203;* a usar nuestra cuenta de gmail.

Nos va a abrir una página web en donde nos va a pedir que hagamos login con nuestro usuario de google. Despues de eso nos avisa que ya podemos cerrar el navegador, la autorización ya va a estar lista.

Esto crea un archivo llamado token.pickle donde se guarda la autorización para no pedirla en las proximas corridas.

    python3 first-run-validation.py

Luego de esto ya estamos listos para correr docker y ver el log del contenedor python

    docker-compose up -d --build && docker logs -f python

### Info adicional

Para poder entrar al adminer la url es http://localhost:8080/ usuario y contraseña "root"