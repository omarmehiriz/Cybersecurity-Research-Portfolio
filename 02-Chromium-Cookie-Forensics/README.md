# 🍪 Module 02: Chromium Session Integrity & AES-GCM Research Framework

Este módulo forma parte de una investigación avanzada sobre la superficie de ataque en navegadores basados en Chromium (Chrome, Edge, Brave). El proyecto documenta y simula un escenario de post-compromiso para evaluar cómo los artefactos de autenticación (cookies de sesión) pueden ser exfiltrados y analizados, a pesar de las capas de cifrado del sistema operativo.

## 🔬 Descripción del Proyecto
El objetivo de este laboratorio es entender el flujo de vida de una identidad digital en el endpoint. El framework implementa un sistema distribuido (C2) para la extracción forense de metadatos de sesión, permitiendo identificar vulnerabilidades en la persistencia de cuentas y proponer medidas de mitigación robustas.



## 🚀 Desafíos Técnicos y Soluciones de Ingeniería
Durante el desarrollo se superaron barreras críticas de seguridad implementadas en los navegadores modernos:

* **Hot-Cloning de Base de Datos:** Los navegadores bloquean el archivo `Cookies` mediante el motor SQLite durante su ejecución. Se implementó una lógica de replicación temporal para permitir la auditoría sin interrumpir el proceso del usuario.
* **Protocolo de Streaming NDJSON:** Para manejar volúmenes masivos de datos (más de 5,000 registros), se evolucionó de un envío monolítico a un sistema de *streaming* línea por línea a través de sockets TCP, evitando *timeouts* y desbordamientos de buffer.
* **Decryption Engine (AES-256-GCM):** Implementación de descifrado simétrico recuperando la clave maestra desde el archivo `Local State`, protegida originalmente por la API DPAPI de Windows.

## 🛡️ Análisis de Mitigación y Perspectiva Blue Team
Este proyecto no solo ilustra el vector de ataque, sino que sirve como base para el endurecimiento de sistemas. Un equipo de defensa (**Blue Team**) puede utilizar estos hallazgos para implementar las siguientes contramedidas:

### 1. Endurecimiento del Endpoint
* **App-Bound Encryption:** Verificación de la eficacia de las nuevas capas de protección de Chrome (v127+) que ligan el cifrado a la identidad del ejecutable.
* **Detección de Comportamiento:** Monitoreo de accesos inusuales a la carpeta `User Data` y llamadas sospechosas a `crypt32.dll` por procesos no firmados.

### 2. Contramedidas en el Lado del Servidor
Para que un robo de cookies sea ineficaz, se proponen las siguientes defensas:
* **Vinculación de Sesión (Session Binding):**
    * **IP Binding:** Validar que cada petición provenga de la IP original.
    * **Device Fingerprinting:** Vincular la sesión a atributos únicos del navegador (User-Agent, resolución, zona horaria).
    * **Token Binding (RFC 8471):** Vincular criptográficamente el token al canal TLS.
* **Gestión de Ciclo de Vida:**
    * **Refresh Tokens de un solo uso:** Si un atacante intenta reutilizar un token antiguo, el sistema debe invalidar todas las sesiones del usuario.
    * **Detección de "Impossible Travel":** Bloqueo de sesiones que aparecen en geolocalizaciones físicamente distantes en intervalos cortos.

### 3. Flags de Seguridad en Cookies
Auditoría de la implementación correcta de:
* `HttpOnly`: Prevenir exfiltración vía XSS.
* `SameSite=Strict`: Neutralizar vectores CSRF.
* `__Host- prefix`: Restringir la cookie exclusivamente al dominio de origen.



## 🛠️ Tecnologías Utilizadas
* **Lenguaje:** Python 3.x
* **Criptografía:** PyCryptodome (AES-GCM), Win32crypt (DPAPI).
* **Bases de Datos:** SQLite3 (Análisis forense).
* **Networking:** Sockets TCP/IP (Custom Protocol).

## ⚠️ Disclaimer Ético
Este software ha sido desarrollado estrictamente con fines educativos y de investigación académica para mejorar las posturas de seguridad defensiva. El autor no se hace responsable del uso indebido de esta herramienta. Su ejecución solo está permitida en entornos controlados bajo consentimiento.
