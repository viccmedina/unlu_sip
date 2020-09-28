# unlu_sip

## Primeros Pasos

### LINUX

Nos debemos posicionar dentro de la carpeta del proyecto:

```bash
sudo apt-get update && sudo apt-get upgrade

sudo apt install virtualenv

virtualenv --python=python3 seminario
```

Con los pasos anteriores hemos actualizado nuestro SO, instalado la librería de entorno virtuales y creado el mismo. Lo llamaremos "seminario" y para activarlo ejecutar:

```bash
source seminario/bin/activate
```

Podemos instalar todas las librerias que necesitmos sin afectar nuestro SO. Para ello ejecutamos:

```bash
pip3 install -r requirements/requirements.txt
```

Luego, para salir del mismo ejecutamos:

```bash
deactivate seminario
```

### WINDOWS

Para el caso de la instalación de Pip debemos seguir los pasos que se indican en el video:
[Tutorial Windows](https://www.youtube.com/watch?v=t9BVg28_Slo&ab_channel=MichaelS)

Luego, para levantar el entorno virtual seguimos los mismos comandos.

## Verificando

A continuación haremos una serie de pasos que nos permitiran saber si hemos configurado todo de manera correcta:

Estando dentro de unlu_sip/unlu ejecutamos:

```bash
export FLASK_APP=app.py (Linux)
export FLASK_ENV=development (Linux)

set FLASK_APP=app.py (Windows)
set export FLASK_ENV=development (Widnows)
```
Con ese comando nos quedará levantado el servidor de Flask y nos dará un enlace para ingresar.
Accedemos al mismo y debemos ver una página en blanco y minimalista con un "hello world!".
Si logramos visualizarlo, hemos configurado todo de manera correcta.

La segunda línea nos permite configurar el entorno en modo de desarrollo. De esta manera vamos a tener
una mayor visualización de Logs y así, vamos a debbugear con mayor fecilidad.


## Settings Local

:warning: **Las settings local nos van a permitir levantar el sistema**: use it well!

Debemos generar un archivo llamado `settings_local.py` dentro del directorio `unlu_sip/distribuidora`.
Este archivo **NO DEBE SER COMMITEADO** al repositorio ya que su objetivo es establecer configuración local del sistema.
Es decir, dentro de `settings_local.py` debemos tener las siguientes constantes:


```python
# Este path pertenece a mi configuración local, en el mismo se almacenará el archivo de la DB.
DB_PATH = '/home/victoria/unlu_sip/data.sqlite'
# Palabra secreta utilizada para cuestiones de seguridad.
DB_SECRET_KEY = 'mysecretkey'
```

En el caso de que falle, tener en cuenta que en el archivo `unlu_sip/distribuidora/__init__.py` se emplean las constantes definidas anteriormente.
Tener en cuenta que la línea 

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
```
Conforma el path. Es necesario contar con cuatro barras.


## Migraciones

Flask, como muchos otros frameworks trabaja con el sistema de migraciones para llevar el seguimiento de los cambios en la DB. Es decir, 
mantiene un registro de todos los ALTERs que se hayan realizado.

En una primera instancia se recomienda ejecutar nuevamente la instalación de los requerimientos.

Luego, situados en la raíz del repositorio `unlu_sip/`, ejecutar esta serie de pasos:

```bash
touch data.sqlite (Linux)
echo. > data.sqlite (Windows)


flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

Si todo salió bien, contaremos con un mensaje en la consola sobre el éxito de nuestros pasos.
En caso contrario, se recomienda eliminar la carpeta `migrations` que fue creada en el paso 1.

:warning: **Las migraciones NO se commitean**: use it well!


## Markdown
Si queremos visualizar archivos de Markdown (.md) debemos tener instalado el paquete `grip`

Si no estamos seguros de que tenemos instaldo el paquete mencionado, simplemente volvemos a instalar los requerimientos:

```bash
pip3 install -r requirements/requirements.txt
```

Luego, en la consola ejecutamos el comando:

```bash
grip
```