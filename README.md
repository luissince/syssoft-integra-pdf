# Generador de PDF con FastAPI y Python

<!-- ![IMAGES DE GO LANG](images/ladder.svg) -->
<img src="templates/images/syssoftintegra.png" alt="Imagen SysSoft Integra" width="200" />



## Iniciar

Este proyecto utiliza FastAPI, wkhtmltopdf, pdfkit y SQLAlchemy para generar archivos PDF. A continuación, se proporciona información sobre cómo configurar y ejecutar la aplicación.

Algunos recursos para iniciar con este proyecto puedes ver en:

- [Python](https://www.python.org/) Es un lenguaje de alto nivel de programación interpretado cuya filosofía hace hincapié en la legibilidad de su código, se utiliza para desarrollar aplicaciones de todo tipo.

- [FastAPI](https://fastapi.tiangolo.com/) Es un marco web moderno para crear API RESTful en Python. Se lanzó por primera vez en 2018 y desde entonces ha ganado rápidamente popularidad entre los desarrolladores debido a su facilidad de uso, velocidad y solidez.

- [wkhtmltopdf](https://wkhtmltopdf.org/) Son herramientas de línea de comandos de código abierto (LGPLv3) para representar HTML en PDF y varios formatos de imagen utilizando el motor de renderizado Qt WebKit. Estos funcionan completamente "sin cabeza" y no requieren visualización ni servicio de visualización.

- [PDFKit](https://pypi.org/project/pdfkit/) Envoltorio Python 2 y 3 para la utilidad wkhtmltopdf para convertir HTML a PDF usando Webkit. 

- [SQLAlchemy](https://code.visualstudio.com/) Es el kit de herramientas Python SQL y el mapeador relacional de objetos que brinda a los desarrolladores de aplicaciones todo el poder y la flexibilidad de SQL.

- [Visual Studio](https://code.visualstudio.com/) Editor de código para todos tipos de lenguaje de programación.

- [Git](https://git-scm.com/) Software de control de versiones.

- [Git Hub](https://github.com/) Plataforma de alojamiento de proyecto de todo ámbito.

## Instalación

Siga los pasos para iniciar el desarrollo:

### 1.  Clona el proyecto o agrague el ssh al repositorio para contribuir en nuevos cambios [Git Hub - Generador de PDF](https://github.com/luissince/syssoft-integra-pdf)

#### 1.1. Agregue por ssh para la integración

Generar tu clave ssh para poder contribuir al proyecto.

```bash
ssh-keygen -t rsa -b 4096 -C "tu email"
```

Configuración global del nombre.

```bash
git config --global user.name "John Doe"
```

Configuración global del email.

```bash
git config --global user.email johndoe@example.com
```

Crea una carpeta.

```bash
mkdir syssoft-integra-pdf
```

Moverse a la carpeta.

```bash
cd syssoft-integra-pdf
```

Comando para inicia git.

```bash
git init
```

Comando que agrega la referencia de la rama.

```bash
git remote add origin git@github.com:luissince/syssoft-integra-pdf.git
```

Comando que descarga los archivos al working directory.

```bash
git fetch origin master
```

Comando que une los cambios al staging area.

```bash
git merge origin/master
```

#### 1.2 Clonar al proyecto

Al clonar un proyecto no necesitas crear ninguna carpeta.

```bash
git clone https://github.com/luissince/syssoft-integra-pdf.git
```

### 2. Instale python desde la págin oficial

```bash
https://www.python.org/downloads/
```

### 3. Instale wkhtmltopdf desde la págin oficial

```bash
https://wkhtmltopdf.org/
```

### 4. Instale las dependencias

```bash
pip install -r requirements.txt
```

### 5. Configuración de Variables de Entorno

A continuación, se presenta la configuración de las variables de entorno utilizadas en el front-end:

```bash
APP_URL_FILES="http://localhost"

PATH_WKHTMLTOPDF=""

DB_HOST="localhost"
DB_USER="root"
DB_PASSWORD="root"
DB_DATABASE="prueba"
DB_PORT=3306
```

### 6. Ejecute el siguiente comando para ejecutar en modo desarrollo

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 7. Ejecute el siguiente comando para ejecutar en modo producción

```bash
uvicorn main:app --host 0.0.0.0 --port 80
```

### 8. Ejecute el siguiente comando para generar el archivo requirements.txt para capturar las dependencias del proyecto

```bash
pip freeze > requirements.txt
```

### 9. Configuración para Ejecutar GitHub Actions para el CI/CD:

Para ejecutar los workflows de GitHub Actions, asegúrate de que tu usuario tenga los privilegios de ejecución necesarios. A continuación, te proporcionamos algunos pasos para empezar:


#### 9.1. Crea un grupo de Docker:

```bash
sudo groupadd docker
```

#### 9.2. Agrega tu Usuario al Grupo de Docker:

```bash
sudo usermod -aG docker $USER
```

#### 9.3. Aplica los Cambios en el Grupo de Docker:

```bash
newgrp docker
```

#### 9.4. Verifica que tu Usuario esté en el Grupo de Docker:

```bash
groups
```
Asegúrate de que "docker" esté en la lista de grupos.

#### 9.5. Configuración y Uso del Runner:

Para iniciar la creación del runner, ve a Settings del proyecto, luego a Actions, Runners, y selecciona "New self-hosted runner".

Si deseas ejecutar en segundo plano, utiliza los siguientes comandos de configuración:

```bash
sudo ./svc.sh status
sudo ./svc.sh install
sudo ./svc.sh start
sudo ./svc.sh stop
sudo ./svc.sh uninstall
```

Estos comandos te permiten controlar el runner según sea necesario.

### 10. Punto importante la hacer git push

Cuando realices un git push origin master y desees evitar que se ejecute el flujo de trabajo de GitHub Actions, puedes incorporar [skip ci] o [ci skip] en el mensaje del commit. Esta adición indicará a GitHub Actions que omita la ejecución de los trabajos para ese commit específico.

Por ejemplo, al realizar un commit, puedes utilizar el siguiente comando para incluir [skip ci] en el mensaje del commit:

```bash
git commit -m "Tu mensaje del commit [skip ci]"
```

### 11. Punto importante al hacer al hacer commit

Si deseas mantener mensajes de commit distintos para desarrollo, prueba y producción, pero sin tener que hacer un commit en la rama de desarrollo antes de probar en la rama de prueba, puedes utilizar la opción --no-ff (no fast-forward) al realizar la fusión en cada rama. Esto te permitirá realizar un commit específico en la rama de prueba (y posteriormente en la rama de producción) incluso si no hubo cambios adicionales en desarrollo.

1. En la rama desarrollo

```bash
git checkout desarrollo
git pull origin desarrollo
# Realiza tus cambios y realiza el commit
git add .
git commit -m "Mensaje de desarrollo"
```

2. Cambia a la rama de prueba

```bash
git checkout test
git pull origin test
# Fusiona los cambios de desarrollo con un commit específico
git merge --no-ff desarrollo -m "Mensaje de prueba"
```

El uso de --no-ff asegurará que se cree un nuevo commit, incluso si no hubo cambios adicionales en desarrollo.