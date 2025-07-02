# DESARROLLO DE UN SISTEMA PARA LA SELECCIÓN ÓPTIMA DE CONTRAMEDIDAS EN LA GESTIÓN DINÁMICA DE RIESGOS

Este proyecto implementa un sistema para la gestión dinámica de riesgos y la selección óptima de contramedidas mediante el uso de ontologías. El núcleo del sistema es el script `gestor.py`, que permite cargar activos, amenazas y contramedidas, calcular riesgos y seleccionar las mejores mitigaciones de forma automatizada.

## Estructura del repositorio
- `gestor.py`: Script principal que gestiona la ontología y ejecuta los distintos procesos.
- `catalogo_activos.json`: Catálogo de activos a proteger.
- `catalogo_amenazas.json`: Catálogo de amenazas consideradas.
- `catalogo_contramedidas.json`: Catálogo de contramedidas disponibles.
- `catalogo_system.json`: Configuración de criterios y pesos para la selección de contramedidas.
- `readme.txt`: Instrucciones originales de uso.

## Requisitos
- Python 3.x
- owlready2

Instalación de dependencias:
```bash
pip install owlready2
```

## Uso básico
El script `gestor.py` se ejecuta desde línea de comandos y toma como primer argumento el archivo de la ontología (por ejemplo, `tfgcaso1.owl`). Los métodos a ejecutar se indican con argumentos precedidos de `--`.

Ejemplo de uso:
```bash
python gestor.py tfgcaso1.owl --all
```

Esto ejecuta todos los métodos en orden recomendado. También se pueden ejecutar individualmente:
```bash
python gestor.py tfgcaso1.owl --carga_activos --carga_system --carga_amenazas --carga_contramedidas --test_pesos --threat_pot_risk --mitigation_to_potential_risk --selection
```

Para ver la ayuda:
```bash
python gestor.py --help
```

## Métodos principales
- `--carga_activos`: Carga los activos definidos en `catalogo_activos.json` en la ontología.
- `--carga_system`: Carga los criterios y pesos de decisión desde `catalogo_system.json`.
- `--carga_amenazas`: Carga las amenazas desde `catalogo_amenazas.json`.
- `--carga_contramedidas`: Carga las contramedidas desde `catalogo_contramedidas.json`.
- `--test_pesos`: Verifica la correcta ponderación de los pesos de los criterios.
- `--threat_pot_risk`: Genera los riesgos potenciales a partir de las amenazas.
- `--mitigation_to_potential_risk`: Relaciona mitigaciones con riesgos potenciales según los activos y palabras clave.
- `--selection`: Realiza la selección óptima de contramedidas y calcula el riesgo residual.

## Ejemplo de flujo de trabajo
1. Cargar activos, criterios, amenazas y contramedidas.
2. Verificar la ponderación de los pesos.
3. Generar riesgos potenciales.
4. Relacionar mitigaciones con riesgos.
5. Seleccionar la mejor contramedida para cada riesgo y calcular el riesgo residual.

## Catálogos de ejemplo
- **Activos:** PC1, PC2, Movil, Datos, Email
- **Amenazas:** Robo de equipos, Acceso no autorizado, Inundación
- **Contramedidas:** Control de acceso físico, CCTV, Autenticación multifactor, Do_Nothing

## Notas importantes
- El orden de ejecución de los métodos es importante para el correcto funcionamiento.
- El sistema utiliza ontologías OWL y la librería owlready2 para manipulación y razonamiento.
- Los criterios y pesos pueden personalizarse en `catalogo_system.json`.

## Autor
Pablo Maldonado

---

Este README fue generado automáticamente a partir de la documentación y el análisis del código fuente.