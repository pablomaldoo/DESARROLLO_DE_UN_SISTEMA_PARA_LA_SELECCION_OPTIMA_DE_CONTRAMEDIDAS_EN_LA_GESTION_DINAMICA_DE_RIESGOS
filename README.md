# DESARROLLO DE UN SISTEMA PARA LA SELECCIÓN ÓPTIMA DE CONTRAMEDIDAS EN LA GESTIÓN DINÁMICA DE RIESGOS

Este proyecto implementa un sistema para la gestión dinámica de riesgos y la selección óptima de contramedidas utilizando ontologías. El núcleo del sistema es el script `gestor.py`, que permite cargar y procesar información sobre activos, amenazas, contramedidas y riesgos, así como ejecutar procesos de inferencia y selección.

## Uso

El script principal es `gestor.py` y se ejecuta desde la línea de comandos:

```bash
python gestor.py <nombre_ontologia.owl> --<método>
```

### Argumentos principales

- El primer argumento es el nombre del archivo de la ontología (por ejemplo: `tfgcaso1.owl`).
- El segundo argumento es el método a ejecutar, precedido por `--`.

### Métodos disponibles

- `--carga_activos`: Carga los activos definidos en el catálogo.
- `--carga_system`: Carga las propiedades del sistema y los pesos de criterios.
- `--carga_amenazas`: Carga las amenazas definidas en el catálogo.
- `--carga_contramedidas`: Carga las contramedidas y las asocia a los activos.
- `--test_pesos`: Realiza una comprobación de la ponderación de los pesos.
- `--threat_pot_risk`: Genera los riesgos potenciales a partir de las amenazas.
- `--mitigation_to_potential_risk`: Relaciona las mitigaciones con los riesgos potenciales.
- `--selection`: Ejecuta el proceso de selección óptima de contramedidas.
- `--all`: Ejecuta todos los métodos en orden recomendado.

También puedes usar `--help` o `-h` para ver la ayuda completa.

> **Nota:** Es importante ejecutar los métodos en el orden recomendado para asegurar la correcta construcción de la ontología y la inferencia de riesgos y contramedidas.

## Requisitos

- Python 3
- owlready2
- Archivos de catálogo en formato JSON (activos, amenazas, contramedidas, sistema)
- Archivo de ontología OWL

## Descripción general

El sistema permite:
- Cargar activos, amenazas y contramedidas desde archivos JSON.
- Generar riesgos potenciales a partir de las amenazas.
- Relacionar automáticamente las contramedidas con los riesgos.
- Realizar la selección óptima de contramedidas en función de criterios y pesos definidos.
- Calcular el riesgo residual tras la aplicación de contramedidas.

---
