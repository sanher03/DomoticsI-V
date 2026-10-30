# Descripción de los mensajes (sintaxis y formato)

Todos los intercambios de mensajes entre los actores se hacen por medio del broker mosquitto, de manera que las colas son de tipo publisher-subscriber. La comunicación, en la mayoría de los casos, es bidireccional, y según el caso en el que nos encontremos, se rezliza por un topic específico. Es tarea de cada uno de los actores ignorar aquellos mensajes que a pesar de ser publicados en el topic en el que están suscritos, no van dirigidos a ellos.

## Intercambio de mensajes entre controlador e interruptores

### Controlador -> Interruptor

**Consulta de estado:**

- consult: el controlador envía este mensaje al topic "redes/2313/O5/ID" con el objetivo de que el interruptor con el ID correspondiente al topic responda con su estado actual, ya que cada dispositivo se encuentra suscrito al topic correspondiente a su ID.

**Cambio de estado:**

- change SWITCHSTATE: una vez que el controlador comprueba que alguno de los mensajes que ha recibido desencadena alguna de las reglas, comprueba el estado de cambio al que debe cambiar el interruptor asociado a la regla, y envía un mensaje con el formato especificado al interruptor que debe recibir la acción. Este mensaje se publica en "redes/2313/O5/ID/set", donde el ID se refiere al del interruptor destino.

### Interruptor -> Controlador

**Consulta de estado:**

- value_query SWITCHSTATE: respuesta del interruptor a la consulta de su estado por parte del controlador. Se publica el mensaje en el topic en el que se recibió el mensaje de consulta, es decir "redes/2313/O5/ID", con ID asociado al propio interruptor.

**Cambio de estado:**

- value_change SWITCHSTATE CHANGESTATUS: respuesta del interruptor a la acción generada y enviada controlador. CHANGESTATUS será 'SUCCEDED' únicamente en el caso de que la acción haya sido llevada a cabo, (la probabilidad de fallo no haya interrumpido el cambio), y 'FAILED' en el caso contrario. En el mensaje se informa del estado en el que se encuentra el interruptor tras la acción. Se publica el mensaje en el topic en el que se recibió el mensaje de consulta, es decir "redes/2313/O5/ID/set", con ID asociado al propio interruptor.

## Intercambio de mensajes entre controlador y sensores

En este caso, la comunicación sigue siendo bidireccional, pero los actores están suscritos respectivamente a un solo topic, ya que la única acción que pueden recibir los sensores es la de consultar su estado.

### Controlador -> Sensor

**Consulta de estado:**

- consult: el controlador envía este mensaje al topic "redes/2313/O5/ID" con el objetivo de que el sensor con el ID correspondiente al topic responda con su estado actual, ya que cada dispositivo se encuentra suscrito al topic correspondiente a su ID.

### Sensor -> Controlador

**Consulta de estado:**

- value_query INTEGER: respuesta del sensor a la consulta de su estado por parte del controlador. Se publica el mensaje en el topic en el que se recibió el mensaje de consulta, es decir "redes/2313/O5/ID", con ID asociado al propio interruptor.

**Cambio de estado:**

- value INTEGER: envío periódico con el objetivo de notificar al controlador el cambio de valor del sensor a medida que pasa el tiempo, de manera que este pueda comprobar si desencadena alguna regla, y actuar en consecuencia. Se publica en el topic "redes/2313/O5/ID", con ID asociado al propio sensot.

## Intercambio de mensajes entre controlador y relojes

En este último caso la comunicación solo se hace en sentido reloj - controlador, para lo que usamos un único topic.

### Reloj -> Controlador

**Cambio de estado:**

- value TIME: nvío periódico con el objetivo de notificar al controlador el cambio de valor del reloj a medida que pasa el tiempo, de manera que este pueda comprobar si desencadena alguna regla, y actuar en consecuencia. Se publica en el topic "redes/2313/O5/ID", con ID asociado al propio reloj.



