# Sistema para la Selección Óptima de Contramedidas en la Gestión Dinámica de Riesgos

Este proyecto implementa un sistema basado en ontologías para la gestión dinámica de riesgos y la selección óptima de contramedidas. Utiliza archivos de catálogo en formato JSON y una ontología OWL para modelar activos, amenazas, contramedidas y riesgos.

## Estructura principal
- **gestor.py**: Script principal que gestiona la carga de datos, inferencias y selección de contramedidas.
- **catalogo_activos.json**: Catálogo de activos.
- **catalogo_amenazas.json**: Catálogo de amenazas.
- **catalogo_contramedidas.json**: Catálogo de contramedidas.
- **catalogo_system.json**: Configuración de criterios y pesos del sistema.
- **tfgcaso1.owl**: Ontología principal.

## Uso
El script principal es `gestor.py`. Se ejecuta desde línea de comandos y acepta varios argumentos:

```bash
python gestor.py <nombre_ontologia.owl> --<método>
```

### Métodos disponibles
- `--carga_activos`: Carga los activos desde el catálogo.
- `--carga_system`: Carga la configuración del sistema y los pesos de criterios.
- `--carga_amenazas`: Carga las amenazas desde el catálogo.
- `--carga_contramedidas`: Carga las contramedidas desde el catálogo.
- `--test_pesos`: Verifica la correcta ponderación de los pesos.
- `--threat_pot_risk`: Genera los riesgos potenciales a partir de las amenazas.
- `--mitigation_to_potential_risk`: Relaciona amenazas, riesgos y contramedidas.
- `--selection`: Realiza la selección óptima de contramedidas y calcula riesgos residuales.
- `--all`: Ejecuta todos los métodos en orden recomendado.
- `-h`, `--help`: Muestra la ayuda.

> **Nota:** Es importante ejecutar los métodos en el orden recomendado para un funcionamiento correcto. El argumento `--all` ejecuta todo el proceso automáticamente.

## Ejemplo de uso
```bash
python gestor.py tfgcaso1.owl --all
```

## Descripción general del proceso
1. **Carga de catálogos**: Se importan activos, amenazas y contramedidas a la ontología.
2. **Configuración de criterios**: Se definen los criterios y pesos para la evaluación de contramedidas.
3. **Generación de riesgos**: Se infieren los riesgos potenciales a partir de las amenazas.
4. **Relación de mitigaciones**: Se relacionan las contramedidas con los riesgos.
5. **Selección óptima**: Se calcula el score de cada contramedida y se seleccionan las más adecuadas, calculando el riesgo residual.

## Requisitos
- Python 3
- owlready2

Instalación de dependencias:
```bash
pip install owlready2
```

## Créditos
Desarrollado por Pablo Maldonado.

---
Este README fue generado automáticamente a partir de la documentación y el código fuente del proyecto.