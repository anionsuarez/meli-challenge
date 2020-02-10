## Challenge MercadoLibre

Script que levanta los correos de gmail que tengan en su asunto o cuerpo la palabra "**devops**" y los almacena en una base de datos.

-----

### Requisitos

Tener instalado:

 - Docker-compose
 - Python3
 - virtualenv

### Funcionamiento

En el directorio raiz hay un archivo *docker-compose.yaml*  que crea el ambiente y descarga las imagenes necesarias para que pueda correr en cualquier equipo.

Levanta 3 contenedores, uno para la base de datos, otro para el adminer para poder ver los registros en las bases de datos y otro para correr python y todos los modulos necesarios.

Al ejecutar docker compose, se levantan los contenedores y se corre automaticamente el script **python/scrap-gmail.py**

### Como correrlo

Clonar el repositorio, guardar el archivo credentials.json dentro y despues levantamos el entorno virtual de python:

    source challenge-env/bin/activate

Luego corremos este archivo para poder autorizar al script *scrap-gmail.py&#8203;* a usar nuestra cuenta de gmail. Esto crea un archivo llamado token.pickle donde se guarda la autorización para no pedirla en las proximas corridas.

    python3 first-run-validation.py

Luego de esto ya estamos listos para correr docker:

    docker-compose up -d --build

Una vez finalizado, par poder ver el log de la corrida del container, ejecutamos:

    docker ps -a | grep -i python | awk '{print $NF}' | xargs docker logs -f

### Info adicional

Para poder entrar al adminer la url es http://localhost:8080/ usuario y contraseña "root"