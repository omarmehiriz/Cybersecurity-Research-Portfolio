# Cybersecurity-Research-Portfolio

Bienvenido a mi repositorio de investigación en ciberseguridad. Este proyecto documenta el análisis de vectores de ataque y mecanismos de defensa en entornos modernos, centrándose en la exfiltración de artefactos de identidad y la persistencia de amenazas en sistemas basados en Windows.

##  Estructura del Proyecto

El framework está dividido en módulos progresivos que cubren desde la comunicación C2 básica hasta la ingeniería inversa de cifrado de navegadores:

* **[Module 01: C2 Payload Analysis](./01_C2_Payload_Analysis)**: Implementación de canales de comunicación persistentes y ejecución remota de comandos.
* **[Module 02: Chromium Cookie Forensics](./02_Chromium_Cookie_Forensics)**: Investigación sobre el descifrado de AES-GCM, bypass de bloqueos de bases de datos y secuestro de sesiones (Session Hijacking).
* **[Module 03: Credential Extraction Audit](./03_Credential_Extraction_Audit)**: Estudio de mecanismos de supervivencia del agente en el sistema y técnicas de ofuscación para bypass de soluciones AV/EDR.

---

##  Stack Tecnológico
* **Lenguaje Principal:** Python 3.x
* **Criptografía:** AES-GCM, DPAPI (Win32 API), RSA.
* **Networking:** Custom Sockets TCP/IP, NDJSON Streaming.
* **Forense:** SQLite3 Database Analysis, Chromium Local State Parsing.

---

##  Objetivos de la Investigación
El objetivo principal de este repositorio es proporcionar una visión de **360 grados** sobre la seguridad de los datos de usuario:

1.  **Perspectiva Ofensiva (Red Team):** Entender cómo los *infostealers* modernos logran bypassar las protecciones del sistema operativo para extraer secretos.
2.  **Perspectiva Defensiva (Blue Team):** Identificar indicadores de compromiso (IoCs) y proponer configuraciones robustas (Hardenning) para mitigar el impacto de un endpoint comprometido.

### Hallazgos Clave
* **Identidad Digital:** La autenticación basada únicamente en cookies es vulnerable si no se acompaña de una vinculación de sesión (Session Binding).
* **Limitaciones del Cifrado Local:** El cifrado en reposo (at-rest) de los navegadores es efectivo contra accesos físicos, pero puede ser superado por procesos maliciosos que corren bajo el mismo contexto de usuario.

---

##  Propuesta de Mitigación Estratégica
Para neutralizar los vectores de ataque presentados en estos módulos, se recomienda la implementación de:

* **Vinculación Criptográfica:** Implementación de RFC 8471 (Token Binding) para ligar tokens al canal TLS.
* **Contextual Auth:** Uso de IP-Binding y Device Fingerprinting para detectar discrepancias en el uso de tokens exfiltrados.
* **Hardenning del Navegador:** Configuración estricta de flags `HttpOnly`, `SameSite` y la adopción de **App-Bound Encryption** (disponible en versiones recientes de Chrome).

---

## ⚠️ Disclaimer Ético
Este repositorio ha sido creado exclusivamente con fines educativos y como parte de una investigación académica 
- **No** se promueve el uso de estas herramientas para actividades ilícitas.
- El autor **no** se hace responsable del uso indebido del código aquí expuesto.
- Toda prueba se ha realizado en entornos controlados y aislados.

---
**Desarrollado por Omar Mehiriz** *Estudiante de Ciberseguridad | Investigador de Amenazas*
