# unlu_sip

## Primeros Pasos

### LINUX

Nos debemos posicionar dentro de la carpeta del proyecto:

```python
sudo apt-get update && sudo apt-get upgrade

sudo apt install virtualenv

virtualenv --python=python3 seminario
```

Con los pasos anteriores hemos actualizado nuestro SO, instalado la librería de entorno virtuales y creado el mismo. Lo llamaremos "seminario" y para activarlo ejecutar:

```python
source seminario/bin/activate
```

Podemos instalar todas las librerias que necesitmos sin afectar nuestro SO. Para ello ejecutamos:

```python
pip3 install -r requirements.txt
```

Luego, para salir del mismo ejecutamos:

```python
deactivate seminario
```

### WINDOWS

Para el caso de la instalación de Pip debemos seguir los pasos que se indican en el video:
[Tutorial Windows](https://www.youtube.com/watch?v=t9BVg28_Slo&ab_channel=MichaelS)

Luego, para levantar el entorno virtual seguimos los mismos comandos.

## Verificando

A continuación haremos una serie de pasos que nos permitiran saber si hemos configurado todo de manera correcta:

Estando dentro de unlu_sip/unlu ejecutamos:

```python
export FLASK_APP=app.py (Linux)

set FLASK_APP=app.py (Windows)
```
Con ese comando nos quedará levantado el servidor de Flask y nos dará un enlace para ingresar.
Accedemos al mismo y debemos ver una página en blanco y minimalista con un "hello world!".
Si logramos visualizarlo, hemos configurado todo de manera correcta.