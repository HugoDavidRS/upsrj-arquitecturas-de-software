<!--
============================================================
Politécnica de Santa Rosa

Profesor: Jesús Salvador López Ortega
Archivo: README.md
Descripción: Documento principal del proyecto. Contiene instrucciones de instalación, uso, estructura y entorno reproducible.
============================================================
-->

![upsrj](docs/img/upsrj.png)

# **Politécnica de Santa Rosa**

- **Carrera: ISW**
- **Materia: Arquitecturas de Software**
- **Instructor:** Jesús Salvador López Ortega ([LinkedIn](https://www.linkedin.com/in/jesus-salvador-lopez-ortega/) | [GitHub](https://github.com/chucholoport))

---

# **Índice**
- [**Politécnica de Santa Rosa**](#politécnica-de-santa-rosa)
- [**Índice**](#índice)
- [**Configuración del repositorio remoto en GitHub**](#configuración-del-repositorio-remoto-en-github)
- [**Instalación y configuración de entorno de trabajo**](#instalación-y-configuración-de-entorno-de-trabajo)
  - [Pasos en la terminal de Windows (CMD)](#pasos-en-la-terminal-de-windows-cmd)
  - [Pasos en la terminal de WSL2 (Ubuntu)](#pasos-en-la-terminal-de-wsl2-ubuntu)
  - [Instalación de Docker](#instalación-de-docker)
- [**Configuración del repositorio remoto en GitHub**](#configuración-del-repositorio-remoto-en-github-1)
  - [IDE de trabajo](#ide-de-trabajo)
  - [Pasos en la terminal de WSL2 (Ubuntu)](#pasos-en-la-terminal-de-wsl2-ubuntu-1)
  - [Ejecuta el contenedor en Visual Studio Code](#ejecuta-el-contenedor-en-visual-studio-code)
- [**Ejecución de proyectos y pruebas**](#ejecución-de-proyectos-y-pruebas)
- [**Contacto**](#contacto)

# **Configuración del repositorio remoto en GitHub**

> **Nota:** **Usa tu correo personal para crear tu cuenta de GitHub.** Recuerda que GitHub es tu portafolio personal como desarrollador de software, por lo que querrás conservarlo aún después de graduarte.

1. **Identifica el repositorio base del profesor**

    Con tu cuenta accede al perfil del profesor [Jesus Lopez](https://github.com/chucholoport) y busca el repositorio de tu materia en su [lista de repositorios](https://github.com/chucholoport?tab=repositories).

    ![git repos](docs/img/git_repositories.png)

2. **Crea un Fork del repositorio base del profesor**

    Selecciona el repositorio de tu materia y da click en `Fork` en la esquina superior derecha para crear un repositorio en tu perfil basado en los contenidos del original. Te aparecerá una ventana que te permitirá personalizar tu Fork, deja todo en default y da click en `Create Fork`.

    ![git fork](docs/img/git_fork.png)

🔙 [Volver al índice](#índice)

---

# **Instalación y configuración de entorno de trabajo**

## Pasos en la terminal de Windows (CMD)

1. **Configurar permisos para ejecutar scripts en PowerShell**

    Si tienes una configuración restringida para correr scripts desde Windows, corre este comando en una terminal de **PowerShell (PS1)**:

    ```powershell
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    ```

    > **Nota:** Si quieres cambiar la configuración para todos los usuarios, corre el siguiente comando en una terminal de **PowerShell (PS1) como administrador**: 

    ```powershell
    Set-ExecutionPolicy RemoteSigned -Scope LocalMachine -Force
    ```

    Puedes confirmar tu configuración con el siguiente comando:
    
    ```powershell
    Get-ExecutionPolicy
    ```

2. **Instalar Windows Subsystem for Linux (WSL)**
    ```batch
    wsl --install
    ```  

3. **Establecer WSL2 como default**
    ```batch
    wsl --set-default-version 2
    ```

🔙 [Volver al índice](#índice)

---

## Pasos en la terminal de WSL2 (Ubuntu)

1. **Configurar `python` como alias de `python3`**

   En algunas instalaciones de WSL, el comando `python` no está disponible por defecto, y solo existe `python3`.  
   Para evitar problemas de compatibilidad, instala el paquete **python-is-python3**:

   ```bash
   sudo apt update
   sudo apt install -y python-is-python3
   ```

   > **Nota:** Después de este paso, podrás ejecutar python y se usará automáticamente Python 3.

2. **Configurar `git` para usar tus credenciales**

    La distribución default de Ubuntu en WSL2 ya incluye una instalación de Git. Para confirmarlo puedes correr previamente el siguiente comando:

    ```bash
    git --version
    ```

    Necesitamos configurar tus credenciales de `git` para evitar que te pida el usuario y contraseña cada que entregas un commit. Para ello selecciona la opción que más te acomode:

   - **Configuración en GitHub con token personal**

       1. Configura tu nombre y correo:

            ```bash
            git config --global user.name "Tu Nombre"
            git config --global user.email "tu@email.com"
            ```
       2. Configura un token de autenticación
          - Ve a [https://github.com/settings/tokens](https://github.com/settings/tokens)
                  
          - Crea un nuevo token clásico
          
            ![git token](docs/img/git_token.png)

          - Selecciona todos los permisos y nombralo como `wsl-access`
          
            ![git token permissions](docs/img/git_token_permissions.png)
          
          - Copia el token

            ![alt text](docs/img/git_token_copy.png)

          > **Nota:** El token **solo se muestra una vez**, por lo que es recomendado que lo copies y guardes en algun archivo de texto en tu computadora.

          - Usa un credential helper para no tener que pegarlo cada vez
            
            ```bash
            git config --global credential.helper store
            ```
          - Cuando hagas git push por primera vez, Git pedirá usuario y contraseña
            - **Usuario:** tu usuario de GitHub
            - **Contraseña:** pega el token generado

   - **Instalar Git Credential Manager (GCM) dentro de WSL**

       Si ya tienes instalado y configurado `git` en Windows, puedes utilizar el `credential-manager` de Windows para configurarlo en WSL:

       ```bash
       git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe"
       ```

       > **Nota:** El parámetro de entrada del comando debe ser el directorio de tu instalación de **Git en Windows**.

🔙 [Volver al índice](#índice)

--- 

## Instalación de Docker

1. **Descarga Docker Desktop**

    Ve a [docker.com](https://www.docker.com/products/docker-desktop/) y descarga Docker Desktop para Windows.

2. **Instala Docker Desktop**

    Durante la instalación, activa la opción `Usar el motor basado en WSL2`. Docker detectará automáticamente tu distro WSL2 (Ubuntu).

    > **Nota:** Al final de la instalación deberás reiniciar tu computadora.

3. **Configura Docker para tu distro WSL**
   
    Abre `Docker Desktop → Settings → Resources → WSL Integration`. Activa tu distro (Ubuntu) para que Docker funcione dentro de ella.

    ![docker wsl integration](docs/img/docker_wsl_integration.png)

4. **Verifica desde WSL**
    
    Abre tu terminal WSL2 (Ubuntu) y ejecuta:
    
    ```bash
    docker --version
    docker run hello-world
    ```

    ![docker hello world](docs/img/docker_hello_world.png)

🔙 [Volver al índice](#índice)

--- 

# **Configuración del repositorio remoto en GitHub**

## IDE de trabajo
   
1. **Instala Visual Studio Code**

    Una vez que tengas tu entorno configurado, estás listo para descargar en tu computadora el código fuente, para ello vamos a utilizar `Visual Studio Code` como IDE de desarrollo con algunas extensiones para mejorar tu experiencia de navegación.

    1. Da click en el enlace de descarga de [Visual Studio Code](https://code.visualstudio.com/docs/?dv=win64user)
    2. Sigue el proceso de instalación con todas las configuraciones por default.

2. **Agrega las extensiones necesarias**
    
    Una vez tengas instalado el IDE, vamos a agregarle las siguientes extensiones:
    
    - **Git Graph:** Te permite visualizar el historial de tu repositorio de forma intuitiva.
    
    ![alt text](docs/img/extension_gitgraph.png)

    - **WSL:** Te permite conectar WSL a tu instalación de Windows para diferenciar los entornos de trabajo.
    
    ![wsl ext](docs/img/extension_wsl.png)

    - **Dev Containers:** Te permite administrar contenedores de Docker, es bastante util para facilitar el arranque del contenedor de trabajo de la materia.
    
    ![devcontainers ext](docs/img/extension_devcontainer.png)

    - **Python:** Te permite visualizar código de Python de una mejor manera, asi como funcionalidades de Debug y Ejecución
    
    ![python ext](docs/img/extension_python.png)

## Pasos en la terminal de WSL2 (Ubuntu)

1. **Creación del directorio de trabajo**

    - Abre una terminal de **WSL (Ubuntu)** y crea un directorio en donde descargues los repositorios de tus materias, después muévete al directorio creado.

    ```bash
    mkdir workspace # El comando "mkdir" crea directorios con el nombre de los parámetros de entrada (en este caso "workspace") 
    cd workspace # El comando "cd" cambia tu dirección actual al parámetro de entrada (en este caso "workspace")
    ```

    > **Nota:** Por estandarización es recomendado crear un directorio `workspace` en el root `~` de tu usuario, pero puedes crear el directorio de tu elección. 

2. **Clonación del repositorio remoto de GitHub**
    
    Ve a GitHub y obtén el `HTTPS` de descarga, puedes verlo dando click en `<> Code` desde tu repositorio.
    
    ![git https](docs/img/git_clone_https.png)

    Dentro del directorio de trabajo, ejecuta el comando de clonación de Git para que se cree una copia local del proyecto en tu computadora.

    ```bash
    git clone https://github.com/chucholoport/upsrj-aprendizaje-automatico.git # El comando "git" corre la aplicación de Git, la bandera "clone" le indica que debe clonar un repositorio remoto, y el HTTPS es el parámetro de entrada del comando
    ```

    ![git clone](docs/img/git_clone_local.png)

3. **Abre el repositorio en Visual Studio Code**

    Una vez tengas el repositorio clonado, es hora de compilar el contenedor para poder empezar a trabajar. Para ello muévete al directorio del repositorio clonado e **invoca Visual Studio Code desde WSL.**

    ```bash
    cd upsrj-aprendizaje-automatico # El comando "cd" cambia tu dirección actual al parámetro de entrada (en este caso "upsrj-aprendizaje-automatico")
    code . # El comando "code" abre Visual Studio Code y el parámetro de entrada "." le indica que debe ser en el directorio actual
    ```

    ![open code](docs/img/vscode_open.png)

## Ejecuta el contenedor en Visual Studio Code

Finalmente, al tener abierto el IDE, vamos a pedirle a Visual Studio Code que corra el contenedor del proyecto para que nos instale todas las dependencias y configuraciones necesarias. Para ello, vamos a dar click en el botón azul `><` de la parte inferior izquierda y seleccionar `Reopen in Container`.

![open container](docs/img/open_container.png)

🔙 [Volver al índice](#índice)

--- 

# **Ejecución de proyectos y pruebas**

1. Dentro del contenedor, presiona `Ctrl + Shift + B` o `Ctrl + B` (según tu configuración).

2. Selecciona la opción `Ejecutar proyecto` o bien `Ejecutar pruebas`.
   
    ![build commands](docs/img/vscode_build.png)

3. Verás el resultado en la terminal integrada.

    ![build project](docs/img/vscode_run.png)

    ![test project](docs/img/vscode_test.png)

🔙 [Volver al índice](#índice)

---

# **Contacto**

¿Dudas? Consulta los archivos de ayuda o pregunta a tu instructor.

**Autor:** Jesús Salvador López Ortega  
[LinkedIn](https://www.linkedin.com/in/jesus-salvador-lopez-ortega/) | [GitHub](https://github.com/chucholoport) | [Correo Institucional](mailto:jlopez@upsrj.edu.mx)

Actualizado: septiembre 2025

🔙 [Volver al índice](#índice)#   T e s t  
 