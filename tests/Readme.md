# Colab Tests Runner 
Este script corre tests para revisión de código y funciona de forma general para cualquier colab. 

### Ubicación de los Tests
Para esto, en primer lugar se deben subir los tests en la carpeta ```../tests``` y los archivos deberán quedar distribuidos de la siguiente forma:
```
colab_lms
  |-- tests
       |-- G1
           |-- P1
                |-- 1
                    |-- input.txt
                    |-- output.txt
                |-- 2
                    |-- input.txt
                    |-- output.txt
                |-- 3
                    |-- input.txt
                    |-- output.txt
           |-- P2
               ...
           |-- Pn
           ...
       |-- Gn
```

### Modificación en el Colab
Luego de subidos los tests, debes poner la siguiente línea en el colab en donde necesitas correr los tests:
```
import urllib.request
exec(urllib.request.urlopen(link_al_script).read())
```
Este script, reconoce la pregunta dentro del colab sí y solo sí esta se encuentra dentro de los tags asignados, para así poder identificar correctamente a qué código corresponde cada pregunta y poder correr los tests de forma efectiva. Los tags se ponen en la celdas de código de la siguiente forma:
```
# <P1>

El código a ejecutar va aquí

# </P1>
```
Inmediatamente después, deberás crear otra celda y poner lo siguiente:
```
run_tests('G1', 'P1')
```
Esta es la función que reconoce la tarea y el número de la pregunta y corre los tests asociados a esta. Es de vital importancia que los argumentos que se le entregan a esta función coincidan con los nombres de las carpetas en donde están almacenados los tests. En este caso, ```G1``` correspondería a la Guía 1 y ```P1``` a la Pregunta 1; en la figura de arriba se puede ver cómo deberían quedar distribuidos los tests para esta ruta.

### Tests
Como te habrás dado cuenta, los tests para cierto colab se encuentran en la ruta ```../tests/codigo_evaluacion/pregunta```, y, dentro de esta carpeta, cada tests estará dentro de una carpeta, cuyo nombre será el número del test. **La numeración comienza desde el 1 en adelante** y, de forma obligatoria, **los nombres de las capetas deben ser solo números**.

Dentro de la carpeta de cada test, **deberán existir como mínimo 2 archivos: ```input.txt``` y ```output.txt```**, los cuales serán, valga la redundancia, el input que se le entregará al código del estudiante y el output esperado luego de ejecutarlo. 

#### Tests Públicos y Secretos
Para diferenciar los tests de los públicos y los secretos, de forma **obligatoria** cada **input** deberá tener un código al inicio que los diferencie, de la siguiente forma:
```
#P
3
5
```
```
#S
3
5
```
En donde ```#P``` significa que el test será ```Público``` y ```#S``` será ```Secreto```. En el caso de los tests secretos, el output esperado se encriptará con ```Hash MD5```, para que el estudiante no pueda ver el resultado.

Cuando el tests es secreto, se espera que el output de ```output.txt``` también esté encriptado con ```Hash MD5```, por ejemplo:
```
fc490ca45c00b1249bbe3554a4fdf6fb
```
Para esto, tendrás disponible un script con una función que podrá encriptar tu output de la forma en la que te mencionamos.

#### encode_secret_tests.py
Para correr este escript, deberás utilizar el siguiente comando:
```
python encode_secret_tests -p path_al_archivo_output.txt
```
(en mac funciona con ```python3```)


### Ejecución por Parte del Estudiante
Para que el run tests funcione en el colab correctamente, el estudiante deberá ejecutar la celda que contiene su código primero en el colab y, posterior a eso, correr los tests.

En caso de existir algún problema con la actualización de los tests en caso de cambio de códugo del estudiante, se sugiere reiniciar el kernel del colab.


