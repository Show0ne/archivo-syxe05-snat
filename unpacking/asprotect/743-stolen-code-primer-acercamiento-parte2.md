# 743 — Primer acercamiento al Stolen Code (Parte 2)

| Campo | Valor |
|------|------|
| Programa | Useful File Utilities v2.3.5 |
| Protección | ASProtect 1.2x–1.3x [Registered] + Stolen Code |
| Autor | SyXe'05 |
| Grupo | CracksLatinoS |

PDF original: **Primer_acercamiento_al_Stolen_Code_parte_2 - [por SyXe'05].pdf**

---

# Introducción

Esta segunda parte continúa el análisis iniciado en la primera parte del tutorial,
donde se explicó el funcionamiento del **Stolen Code en ASProtect**.

El objetivo aquí es:

- reconstruir completamente el ejecutable
- restaurar el flujo de ejecución
- finalizar la reconstrucción de la IAT
- obtener un ejecutable funcional tras el dump.

---

# Análisis del flujo de ejecución

En esta fase el programa ya puede ejecutarse hasta el punto en el que el
código robado es reinsertado en el flujo original.

Se identifican múltiples llamadas indirectas que redirigen la ejecución hacia
las secciones temporales creadas por el packer.

Estas secciones contienen partes del código original del programa.

---

# Restauración del flujo original

Para reconstruir el flujo correcto se procede a:

1. identificar cada bloque de código robado
2. localizar su posición original
3. reemplazar las llamadas indirectas por saltos directos.

Esto elimina la redirección utilizada por el packer.

---

# Reparación de saltos

Muchas instrucciones fueron transformadas por el packer en llamadas indirectas:

CALL XXXXXXXX

Estas instrucciones se reemplazan nuevamente por los saltos originales.

Ejemplo:

JE XXXXXXXX  
JNE XXXXXXXX  
JMP XXXXXXXX

Esto restaura el comportamiento original del programa.

---

# Reconstrucción final de la IAT

Una vez restaurado el flujo del programa se realiza el dump del ejecutable.

Posteriormente se utiliza **Import Reconstructor (ImpREC)** para reconstruir
la tabla de importaciones.

Pasos:

1. realizar dump del proceso
2. localizar la IAT
3. reconstruir imports
4. guardar ejecutable reparado.

---

# Verificación

Después de reconstruir la IAT el ejecutable se prueba fuera del debugger.

El programa se ejecuta correctamente y funciona sin la protección.

Esto confirma que:

- el código robado fue restaurado correctamente
- la tabla de importaciones es válida
- el ejecutable está completamente desempaquetado.

---

# Conclusión

Con este proceso se logra eliminar la protección **ASProtect con Stolen Code**.

El tutorial demuestra cómo:

- analizar el comportamiento del packer
- recuperar código robado
- reconstruir la IAT
- restaurar el flujo original del programa.

---

Autor: **SyXe'05**  
Grupo: **CracksLatinoS**
