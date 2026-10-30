# Plataforma domótica IoT

Aplicación web Django para registrar dispositivos, crear reglas y consultar eventos. El controlador y tres dispositivos simulados se ejecutan automáticamente y se comunican mediante MQTT.

## Inicio rápido

### Requisitos

- Docker Desktop o Docker Engine con Docker Compose v2.
- Acceso a Internet durante la primera compilación para descargar las imágenes y dependencias.
- Para abrirla desde otro dispositivo: ambos equipos deben estar en la misma red local.

No hace falta instalar Python, Django, Node.js ni Mosquitto en el equipo anfitrión.

### Arrancar

Descarga o clona el repositorio, abre una terminal en su directorio raíz y ejecuta:

```bash
./scripts/start.sh
```

El script compila y arranca todos los servicios. Abre <http://localhost:8000> en el equipo anfitrión. La primera compilación puede tardar unos minutos.

También se puede arrancar directamente con Docker Compose:

```bash
docker compose up --build --detach
```

En Windows, ejecuta ese comando desde PowerShell en el directorio del repositorio.

Al iniciar una base de datos vacía, se crean automáticamente tres dispositivos de demostración y sus reglas:

| ID | Dispositivo | Comportamiento |
|---:|---|---|
| 101 | Interruptor | Recibe órdenes y confirma los cambios |
| 102 | Sensor | Publica valores entre 10 y 30 |
| 103 | Reloj | Publica la hora simulada |

El controlador los registra y aplica las reglas de ejemplo: el sensor enciende el interruptor por encima de 20 y lo apaga por debajo de 15; el reloj tiene una regla de demostración a las 09:00:10. Tras unos segundos, los eventos y cambios aparecen en la interfaz. Puedes añadir, editar o borrar dispositivos y reglas desde la web.

### Abrir desde un móvil, tableta u otro ordenador

El servidor web escucha en la red local. En el otro dispositivo, abre `http://IP-DEL-EQUIPO:8000`, sustituyendo la dirección por la IP local del ordenador que ejecuta Docker.

- Linux: consulta la IP con `hostname -I`.
- macOS: consulta la IP de la interfaz Wi-Fi con `ipconfig getifaddr en0`.
- Windows: ejecuta `ipconfig` y busca la dirección IPv4 de la conexión activa.

Por ejemplo: `http://192.168.1.25:8000`. Los dos equipos deben estar conectados a la misma Wi-Fi o LAN. Si no carga, permite conexiones entrantes al puerto TCP 8000 en el firewall del anfitrión y comprueba que la red no tenga aislamiento entre clientes.

Opcionalmente, cambia el puerto del anfitrión:

```bash
WEB_PORT=8080 ./scripts/start.sh
```

En ese caso usa `http://localhost:8080` o `http://IP-DEL-EQUIPO:8080`.

## Uso y operaciones habituales

La sección **Dispositivos** permite consultar sensores e interruptores, crear dispositivos, editarlos o borrarlos. En **Reglas** se configuran las condiciones y el interruptor que debe cambiar. **Eventos** muestra las consultas y las confirmaciones de cambio reportadas por los dispositivos.

Los cambios de las reglas pueden repetirse mientras una condición siga cumpliéndose. El interruptor evita publicar confirmaciones redundantes si ya está en el estado solicitado.

Ver los registros en tiempo real:

```bash
docker compose logs -f
```

Ver solo algunos servicios:

```bash
docker compose logs -f web controller sensor switch clock
```

Detener la aplicación sin borrar los dispositivos, reglas ni eventos:

```bash
./scripts/stop.sh
```

Volver a arrancarla conserva la base de datos y los cambios. **Para reiniciar y borrar los datos de demostración**, ejecuta `docker compose down --volumes` y luego `./scripts/start.sh`. La opción `--volumes` elimina permanentemente la base de datos de este despliegue.

## Estructura del proyecto

```text
.
├── docker-compose.yml          # Web, broker MQTT, controlador y dummies
├── Dockerfile                  # Imagen común de la aplicación
├── requirements.txt            # Dependencias Python
├── docs/                       # Documentación técnica y diagramas
│   ├── README.md
│   ├── communication.md
│   ├── requisitos.md
│   ├── esquema_persistencia.md
│   └── esquema_de_clases.png
├── scripts/
│   ├── start.sh                 # Arranque automatizado
│   └── stop.sh                  # Parada sin borrar datos
├── iot_devices/                # Cliente MQTT base, dispositivos y lanzadores
│   └── manual_tests/            # Pruebas interactivas heredadas
└── server_domotics/             # Aplicación Django
    ├── devices/                 # Gestión web de dispositivos
    ├── rules/                   # Gestión de reglas
    ├── domotics/                # Eventos, datos demo y migraciones
    ├── controller/              # Controlador y motor de reglas
    ├── server_domotics/         # Configuración del proyecto Django
    └── static/                  # Estilos, imágenes y Bootstrap local
```

## Arquitectura y configuración

Docker Compose crea una red privada para los servicios. El navegador solo necesita acceder a Django por el puerto 8000; el broker MQTT no se publica al exterior. Django, el controlador y los simuladores se conectan entre sí por el nombre interno `mqtt`.

El broker local permite conexiones anónimas y está pensado exclusivamente para demostraciones en una red privada. **No expongas este despliegue directamente a Internet ni reenvíes sus puertos desde el router.** Además, Django se ejecuta en modo de desarrollo. Para acceso fuera de la LAN, usa una VPN privada y prepara antes autenticación, HTTPS, credenciales y una configuración de producción.

Variables opcionales:

- `WEB_PORT`: puerto HTTP publicado en el anfitrión (por defecto `8000`).
- `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_SECRET_KEY`: configuración de Django para adaptar un despliegue controlado.
- `MQTT_HOST` y `MQTT_PORT`: dirección del broker que usan Django, el controlador y los simuladores (por defecto, el servicio local `mqtt:1883`).

La base de datos se conserva en un volumen Docker, independiente del código descargado. Bootstrap se incluye en la imagen para que la interfaz no dependa de un CDN durante su uso.

## Documentación adicional

La documentación técnica y los diagramas están agrupados en [docs/](./docs/README.md). 
