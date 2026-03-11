# Reversing on Windows – The Logon Quest

Autor: SyXe'05  
Categoría: Reversing / Windows Internals

## PDF original

Reversing_on_Windows_The_Logon_Quest_por_SyXe'05.pdf

---

## Introducción

Este documento estudia el proceso de **logon en Windows** desde la perspectiva de la ingeniería inversa.

El objetivo es comprender cómo el sistema operativo maneja el proceso de autenticación del usuario y qué componentes intervienen durante el inicio de sesión.

El análisis de estos mecanismos resulta especialmente interesante para:

- Investigación en seguridad
- Comprensión de los internals de Windows
- Análisis de malware
- Desarrollo de herramientas de debugging y reversing

---

## Componentes implicados en el logon de Windows

Durante el proceso de autenticación intervienen varios componentes clave del sistema:

- **Winlogon.exe**
- **LSASS (Local Security Authority Subsystem Service)**
- **GINA (Graphical Identification and Authentication)** en versiones antiguas de Windows
- **Credential Providers** en versiones modernas

Cada uno de estos módulos cumple una función específica dentro del proceso de autenticación.

---

## Winlogon

**Winlogon.exe** es el proceso responsable de gestionar el inicio de sesión interactivo.

Entre sus funciones se incluyen:

- Mostrar la pantalla de logon
- Gestionar el bloqueo de sesión
- Lanzar el shell del usuario tras autenticación correcta

El análisis de Winlogon permite comprender cómo se inicia la sesión del usuario dentro del sistema.

---

## LSASS

El proceso **LSASS** se encarga de validar las credenciales introducidas por el usuario.

Entre sus responsabilidades principales:

- Validación de contraseñas
- Aplicación de políticas de seguridad
- Gestión de tokens de seguridad

Este proceso es crítico para el funcionamiento del sistema y suele ser objetivo de análisis en investigaciones de seguridad.

---

## Análisis mediante reversing

El reversing de estos componentes puede realizarse mediante:

- Análisis de llamadas a la API
- Debugging de procesos del sistema
- Estudio del flujo de autenticación

Durante el análisis se pueden identificar:

- Funciones responsables de validar credenciales
- Creación de tokens de seguridad
- Inicialización de la sesión del usuario

---

## Consideraciones de seguridad

Debido a su papel central en el sistema, los componentes relacionados con el logon suelen estar protegidos mediante mecanismos de seguridad adicionales.

Entre ellos:

- Protección de procesos críticos
- Restricciones de acceso a memoria
- Validación de integridad del sistema

Esto dificulta el análisis directo de estos componentes.

---

## Conclusión

El estudio del proceso de **logon en Windows** permite comprender mejor cómo funciona el sistema operativo a nivel interno.

El análisis de componentes como **Winlogon** y **LSASS** proporciona información valiosa sobre el modelo de seguridad de Windows y sobre cómo se gestionan las sesiones de usuario.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
