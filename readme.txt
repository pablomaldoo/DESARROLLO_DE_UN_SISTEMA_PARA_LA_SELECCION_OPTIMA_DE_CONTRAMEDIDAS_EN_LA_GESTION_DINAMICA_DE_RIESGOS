Instrucciones para usar el gestor.py

Toma varios argumentos, pueden tomar cualquier posición, pero es recomendable de la siguiente forma:

python gestor.py <<Arg1>> --<<Arg2>>

El primer argumento es el nombre de la ontología, en este caso sería: tfgcaso1.owl

El segundo argumento es el método que se quiere utilizar con -- antes. Los métodos disponibles son los siguientes, es importante su orden:

carga_activos
carga_system
carga_amenazas
carga_contramedidas
test_pesos
threat_pot_risk
mitigation_to_potential_risk
selection


También se puede acceder a --help o -h que muestra por pantalla:

Ejecutar métodos con una ontología.

positional arguments:
  val_onto              Nombre del archivo de la ontología.

options:
  -h, --help            show this help message and exit
  --all                 Ejecutar todos los métodos. Despliega todo el entorno con todos los procesos en orden.
  --carga_activos       Ejecutar carga_activos. Genera los individuos de los activos que se introducen en su catálogo.
  --carga_system        Ejecutar carga_system. Genera el individuo System_properties y los sistemas de pesos.
  --carga_amenazas      Ejecutar carga_amenazas. Genera los individuos de las amenazas que se introducen en su catálogo.
  --carga_contramedidas
                        Ejecutar carga_contramedidas. Genera los individuos de las contramedidas que se introducen en su catálogo.
  --test_pesos          Ejecutar test_pesos. Realiza una ponderación de los valores de peso.
  --threat_pot_risk     Ejecutar threat_pot_risk. Genera los individuos de riesgo a través de las amenazas existentes.
  --mitigation_to_potential_risk
                        Ejecutar mitigation_to_potential_risk. Genera la inferencia para relacionar las amenazas y los riesgos adecuadamente.
  --selection           Ejecutar selection. Inicia el proceso de selección de contramedidas, este método llama al método de riesgo residual para generar los riesgos residuales derivados.


¡Importante! Si se quiere iniciar los métodos individualmente, es importante que se ejecuten en el orden que se muestra.

