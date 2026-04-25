# C2 Simulation & Telemetry Analysis

Este módulo recrea un entorno de Mando y Control (C2) profesional diseñado como laboratorio de investigación. El objetivo es estudiar el comportamiento de agentes remotos, la telemetría que generan en la red y los artefactos forenses que dejan en el host tras una intrusión.

Componentes del Proyecto
 **`agent.py` (Endpoint Payload):** Simula un agente de acceso remoto. Incluye una técnica de distracción mediante un "Lure Document" (PDF real de la UAH) que se abre al ejecutarse el script para ocultar la actividad maliciosa en segundo plano. Contiene módulos de captura de pantalla y webcam para simular la exfiltración de datos.
 **`c2_server.py` (Analyst Interface):** Consola de mando que actúa como el servidor de escucha. Permite al analista monitorizar conexiones entrantes, enviar comandos de auditoría y recibir evidencias exfiltradas de forma organizada.

Análisis de Defensa (SOC/Blue Team Perspective)
El valor principal de este laboratorio es la identificación de **Indicadores de Compromiso (IoCs)** críticos para un entorno de monitorización real:

1. Telemetría y Análisis de Red
 **Técnicas de Tunneling:** Identificación de tráfico hacia servicios de túnel TCP (como **ngrok** o similares) para evadir firewalls perimetrales.
 **Puertos no estándar:** Detección de conexiones persistentes a través de puertos inusuales (ej. 4444) que no corresponden a protocolos corporativos estándar.
 **Anomalías en Exfiltración:** Monitorización de picos de tráfico saliente (Outbound) durante la transferencia de archivos de imagen o capturas de pantalla.

 2. Comportamiento del Host (Endpoint)
 **Parent-Child Link (Procesos):** Detección de una de las técnicas más comunes de phishing: una aplicación legítima (ej. `Acrobat.exe`, `Chrome.exe`) lanzando procesos de sistema como `powershell.exe` o `python.exe`.
 **Ejecución de Comandos:** Rastreo de comandos de reconocimiento (`whoami`, `hostname`, `net user`) ejecutados desde el payload.
 **Artefactos Forenses:** Localización de archivos huérfanos (`snap.png`, `foto.jpg`) creados en directorios temporales de usuario sin intervención humana explícita.

Medidas de Mitigación Recomendadas
 **Reglas ASR (Attack Surface Reduction):** Configuración de políticas para bloquear la creación de procesos hijos por parte de aplicaciones de lectura de documentos o navegadores.
 **DNS/Proxy Filtering:** Bloqueo preventivo de dominios asociados a servicios de túneles públicos conocidos.
 **Auditoría de Eventos:** Activación y monitorización de los Logs de PowerShell (**Event ID 4104**) para inspeccionar bloques de código ejecutados en memoria.
 **EDR Policy:** Alertar sobre la carga de librerías de captura de imagen/vídeo (`OpenCV`, `PyAutoGUI`) por parte de procesos no autorizados.

---
**Nota Técnica:** El código contenido en este directorio ha sido securizado para su exhibición pública. Se han sustituido los endpoints reales por placeholders (`REDACTED_ENDPOINT`) y se ha restringido la ejecución de comandos arbitrarios por motivos éticos y de seguridad.
