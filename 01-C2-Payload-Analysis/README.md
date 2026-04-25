# C2 Simulation & Telemetry Analysis

Este módulo recrea un entorno de Mando y Control (C2) profesional diseñado como laboratorio de investigación. El objetivo es estudiar el comportamiento de agentes remotos, la telemetría que generan en la red y los artefactos forenses que dejan en el host tras una intrusión.

## Componentes del Proyecto
* **agent.py (Endpoint Payload):** Simula un agente de acceso remoto. Incluye una técnica de distracción mediante un "Lure Document" (PDF real de la UAH) que se abre al ejecutarse el script para ocultar la actividad maliciosa en segundo plano. Contiene módulos de captura de pantalla y webcam para simular la exfiltración de datos.
* **c2_server.py (Analyst Interface):** Consola de mando que actúa como el servidor de escucha. Permite al analista monitorizar conexiones entrantes, enviar comandos de auditoría y recibir evidencias exfiltradas de forma organizada.

## Análisis de Defensa (SOC / Blue Team Perspective)

El valor principal de este laboratorio reside en la identificación y comprensión de los
Indicadores de Compromiso (IoCs) generados durante una intrusión simulada. A continuación
se documentan las técnicas de detección y mitigación aplicables en un entorno empresarial real.

---

### 1. Telemetría y Análisis de Red (NDR / SIEM)

**Detección de Túneles TCP**  
Los agentes remotos frecuentemente utilizan servicios de tunneling público (ngrok, serveo,
localhost.run) para evadir firewalls perimetrales enrutando el tráfico C2 a través de HTTPS
legítimo. La defensa más eficaz es el bloqueo preventivo a nivel DNS/Proxy de los dominios
asociados a estos servicios, ya que su uso en endpoints corporativos es prácticamente
inexistente en condiciones normales.

**Puertos No Estándar**  
Implementar reglas de alerta en el SIEM ante conexiones salientes persistentes hacia puertos
inusuales (4444, 5555, 1337, 8080 en contextos no autorizados). Complementar con un baseline
de tráfico por endpoint para detectar desviaciones estadísticas.

**Anomalías de Exfiltración (DLP)**  
Monitorizar picos de tráfico outbound desde endpoints con perfil de bajo consumo de red.
La transferencia de capturas de pantalla o imágenes genera patrones de tráfico reconocibles:
ráfagas periódicas de tamaño constante hacia una IP externa no categorizada.

---

### 2. Comportamiento del Host (EDR / Sysmon)

**Parent-Child Process Anomalies**  
Una de las señales más fiables de compromiso es la cadena de procesos anómala.
Ejemplos de alta prioridad:

| Proceso Padre | Proceso Hijo | Severidad |
|---|---|---|
| `AcroRd32.exe` | `python.exe` | 🔴 Crítica |
| `chrome.exe` | `powershell.exe` | 🔴 Crítica |
| `winword.exe` | `cmd.exe` | 🔴 Crítica |

Ninguna de estas relaciones debería ocurrir en condiciones normales. Configurar reglas
de detección en el EDR con severidad crítica.

**Ejecución de Comandos de Reconocimiento**  
Detectar la ejecución en secuencia rápida de los siguientes comandos desde un proceso
no interactivo:

```bash
whoami && hostname && net user && ipconfig && systeminfo
```

Este patrón es característico de la fase de reconocimiento post-explotación (Discovery - T1082).

**Carga de Librerías Sospechosas**  
Alertar sobre la carga de módulos de captura de imagen o vídeo (`OpenCV`, `PyAutoGUI`,
`Pillow`) por parte de procesos que no sean aplicaciones multimedia autorizadas.

**Artefactos Forenses en Disco**  
Vigilar la creación de archivos de imagen (`*.png`, `*.jpg`) en directorios temporales
(`%Temp%`, `%AppData%`, `%LocalAppData%`) sin interacción explícita del usuario,
especialmente si son eliminados inmediatamente tras su creación.

---

### 3. Medidas de Hardening y Mitigación

**Attack Surface Reduction (ASR)**  
Activar las reglas ASR de Microsoft Defender para bloquear la creación de procesos hijo
por parte de aplicaciones de lectura de documentos y navegadores. Esta medida neutraliza
la mayoría de los vectores de phishing por documento.

**Control de Ejecución (AppLocker / WDAC)**  
Restringir la ejecución de intérpretes portables (Python, Node.js) y scripts no firmados
desde directorios de escritura del usuario. Un endpoint corporativo no debería poder
ejecutar `python.exe` desde `%AppData%`.

**DNS y Proxy Filtering**  
Mantener una lista de bloqueo actualizada de dominios asociados a servicios de túnel
público. Complementar con inspección TLS en el proxy para detectar tráfico C2 encapsulado
en HTTPS.

**PowerShell Script Block Logging**  
Activar Event ID 4104 y enviar los eventos al SIEM. Permite inspeccionar el código
ejecutado en memoria incluso cuando el script ha sido eliminado del disco.

**Principio de Mínimo Privilegio**  
Un usuario estándar no debería tener permisos para instalar librerías, ejecutar
intérpretes arbitrarios ni realizar conexiones salientes no autorizadas.

---

### 4. Respuesta ante Incidentes (IR)

En caso de detección de un agente activo, el procedimiento recomendado es:

1. **Contención** → Aislar el endpoint de la red sin apagarlo para preservar artefactos en memoria.
2. **Adquisición forense** → Capturar imagen de RAM (Volatility) y disco antes de cualquier acción correctiva.
3. **Análisis de IoCs** → Extraer IPs, dominios, hashes y rutas de artefactos para incorporarlos a las reglas del SIEM.
4. **Erradicación** → Identificar el vector de entrada inicial antes de restaurar el sistema.

---

  **Nota Ética:** Este laboratorio ha sido desarrollado con fines estrictamente educativos en un entorno controlado y aislado. El análisis de estas técnicas tiene como único objetivo la comprensión de los vectores de ataque para mejorar las capacidades defensivas en entornos SOC reales.

 **Nota Técnica:** El código contenido en este directorio ha sido securizado para su exhibición pública. Se han sustituido los endpoints reales por placeholders (`REDACTED_ENDPOINT`) y se ha restringido la ejecución de comandos arbitrarios por motivos éticos y de seguridad.
