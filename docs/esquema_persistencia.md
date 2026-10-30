# Esquema de datos usado en la persistencia

Al haber elegido la opción de django, la persistencia la realizamos mediante SQLite, de manera que hemos definido una serie de modelos que almacenar la información necesaria para el correcto funcionamiento del proyecto. El fichero SQLite que usamos es "db.sqlite3", y al ser una base de datos de rápido acceso y fácil manejo, no es necesario persistir como tal los datos en ningún momento. Las acciones que se realizan sobre el fichero quedan guardadas, y cuando se vuelva a acceder a la base de datos, esta estará actualizada y mostrará el resultado de las acciones realizadas con anterioridad.

A continuación proporcinamos un breve esquema del formato y la información que almacenamos en nuestra base de datos.

Nuestra base de datos cuenta con tres modelos, es decir, tres tablas que almacenan cada una información asociada a un objeto diferente, que será explicada a continuación.

### Device Model: 
Almacena la información de los dispositivos registrados en el sistema.
- **device_id**: Un campo entero que representa el identificador único de un dispositivo.

- **name**: Un campo de texto que almacena el nombre del dispositivo, con una longitud máxima de 200 caracteres.

- **tipo**: Un campo de texto que representa el tipo de dispositivo, con una longitud máxima de 20 caracteres. Se proporciona un conjunto limitado de opciones para este campo, definido en DEVICE_TYPE. El usuario puede seleccionar entre 'Sensor', 'Switch' y 'Clock'.

- __str__(): Un método especial que devuelve una representación en cadena del objeto. En este caso, devuelve el nombre del dispositivo.

### Rule Model: 
Almacena la información de las reglas registradas en el sistema.
- **name**: Un campo de texto que almacena el nombre de la regla, con una longitud máxima de 200 caracteres.

- **device1**: Una clave externa que establece una relación muchos a uno con la clase Device. Cada regla está asociada con un dispositivo, y si se elimina un dispositivo, todas las reglas asociadas a él también se eliminan.

- **comparator**: Un campo de texto que representa el tipo de comparador para la regla, con una longitud máxima de 20 caracteres. Las opciones disponibles están definidas en COMPARATOR_TYPE. El usuario puede seleccionar entre 'More_than', 'Less_than' y 'Equals'.

- **value**: Un campo de texto que almacena el valor asociado con la regla, con una longitud máxima de 200 caracteres.

- **device2**: Una clave externa que establece una relación muchos a uno con la clase Device. Representa el dispositivo que se cambiará según la regla.

- **turn_on**: Un campo booleano que indica si el dispositivo asociado debe encenderse o apagarse según la regla.

### Event Model: 
Almacena información de los eventos internos generados por el sistema.
- **device**: Una clave externa que establece una relación muchos a uno con la clase Device. Cada evento está asociado con un dispositivo.

- **state**: Un campo de texto que representa el estado del evento, con una longitud máxima de 200 caracteres. Las opciones disponibles están definidas en STATE. El sistema asocia 'Query', si el evento es una consulta, y 'Change' si el evento es generado por un cambio.

- **value**: Un campo de texto que almacena el valor asociado con el evento, con una longitud máxima de 200 caracteres.

- **read**: Un campo booleano que indica si el evento ya se ha leído o no. Está por defecto a False.

- **status**: Un campo de texto que representa el estado de la acción evento, con una longitud máxima de 200 caracteres. Las opciones disponibles están definidas en STATUS. El sistema asocia 'SUCCEDED', si la acción del evento se ha llevado a cabo, y 'FAILED' en caso contrario. Los eventos de consulta tienen este campo a 'SUCCEDED' por defecto.


