from owlready2 import * 
import json
import argparse
import time


def carga_system(onto, val_onto): # Método para guardar en la ontología las nuevas instancias de mitigaciones con las propiedades definidas y asignarle Assets que protege
    archivo = open('catalogo_system.json')
    data = json.load(archivo)
    for i in data:
        
        # Si el id contiene System_properties es el individuo System
        if "System_properties" in i["id"]: 
            ind = onto.System("System_properties")
            ind.risk_acceptance = [i["risk_acceptance"]]
        
        # Si el id contiene Criterio_1_<<atributo>> se genera el individuo Criterio_Primer_Nivel (si no se divide en Criterio_2_, <<atributo>> tiene que referenciar a un atributo de la contramedida)
        elif "Criterio_1" in i["id"]:
            
            # print(i["id"].split("Criterio_1_")[1]) # se consigue extraer el nombre del atributo   Criterio_Primer_Nivel
            
            ind = onto.Criterio_Primer_Nivel(i["id"])
            ind.weight_value = [i["weight_value"]]
            ind.is_divided = [i["is_divided"]]  # Se usa para saber si el criterio esta desglosado o no (si esta el campo <<atributo>> del id no referencia a ninguna atributo)
        
        # Criterio_Segundo_Nivel
        
        # Si el id contiene el Criterio_2_<<atributo>> se genera el individuo de Criterio_Segundo_Nivel (<<atributo>> siempre tiene que referenciar a un atributo de la contramedida)
        elif "Criterio_2" in i["id"]:
            ind = onto.Criterio_Segundo_Nivel(i["id"])
            ind.weight_value = [i["weight_value"]]
            
            # Se añaden como subpesos del Criterio_1 desglosado
            ind.is_subcriteria_of.append(getattr(onto, i["is_subcriteria_of"]))
            getattr(onto, i["is_subcriteria_of"]).has_subcriteria.append(ind)
    
    archivo.close()
    onto.save(val_onto)
    print("Se ha ejecutado la carga system")



def carga_activos(onto, val_onto): # Método para guardar en la ontología las nuevas instancias de mitigaciones con las propiedades definidas y asignarle Assets que protege
    archivo = open('catalogo_activos.json')
    data = json.load(archivo)
    for i in data:
        ind = onto.Assets(i["id"])
        
        # Se genera el individuo con la "class" utilizando una variable auxiliar
        aux = [i["class"]]
        tipo = [i["type"]]
        ind = getattr(onto, aux[0])(i["id"])
        ind = getattr(onto, tipo[0])(i["id"])
        
    
    archivo.close()
    onto.save(val_onto)
    print("Se ha ejecutado la carga activos")


def carga_contramedidas(onto, val_onto): # Método para guardar en la ontología las nuevas instancias de mitigaciones con las propiedades definidas y asignarle Assets que protege
    archivo = open('catalogo_contramedidas.json')
    data = json.load(archivo)
    print("El fichero contramedidas se ha cargado")
    for i in data:
        ind = onto.Mitigations(i["id"])	
        ind.id = [i["id"]]
        ind.description = [i["description"]]
        ind.keywords = i["keywords"]
        ind.type = [i["type"]]
        ind.deployment_cost = [i["deployment_cost"]]
        ind.deployment_effort = [i["deployment_effort"]]
        ind.impact = [i["impact"]]
        ind.installation_complexity = [i["installation_complexity"]]
        ind.operation_complexity = [i["operation_complexity"]]
        ind.mitigation_factor = [i["mitigation_factor"]]
        ind.effectiveness = [i["effectiveness"]]
        ind.time_to_be_up_and_running = [i["time_to_be_up_and_running"]]
        ind.enabled = [False]
        ind.disabled = [False]
        
        # Esta sentencia es para DoNothing, si se incluye "All" protege a todos los tipos de activos
        if "All" in i["protected_assets"]:
            i["protected_assets"] = "HW", "SW", "Infrastructure", "Location", "Personnel", "Info_Data", "Processes_Functions_Services"
        
        for asset in i["protected_assets"]: 
            for x in onto.Assets.subclasses():	
                for y in x.subclasses():
                    if asset in str(y).split(".")[1]:		# Secondary_Asset.HW = "Secondary","HW" | selecting position 1 = HW
                        for si in y.instances():			# Instances: PC, Movil...
                            ind.protects.append(si)			# M1 protects PC, Movil...
    archivo.close()
    onto.save(val_onto)
    print("Se ha ejecutado la carga contramedidas")



def carga_amenazas(onto, val_onto): # Método para guardar en la ontología las nuevas instancias de mitigaciones con las propiedades definidas y asignarle Assets que protege
    archivo = open('catalogo_amenazas.json')
    data = json.load(archivo)
    print("El fichero amenazas se ha cargado")
    for i in data:
        ind = onto.Threat(i["id"])
        
        # Se genera el individuo con la "class" utilizando una variable auxiliar
        aux = [i["class"]]
        ind = getattr(onto, aux[0])(i["id"])
        
        # Se genera el individuo con el "type" utilizando una variable auxiliar
        tipo = [i["type"]]
        ind = getattr(onto, tipo[0])(i["id"])
        
        ind.probability = [i["probability"]]
        ind.impact = [i["impact"]]
        
        # De igual forma que en las mitigaciones
        for asset in i["affects"]: 
            for x in onto.Assets.subclasses():	
                for y in x.subclasses():
                    if asset in str(y).split(".")[1]:		# Secondary_Asset.HW = "Secondary","HW" | selecting position 1 = HW
                        for si in y.instances():			# Instances: PC, Movil...
                            ind.affects.append(si)			# M1 affects PC, Movil...
        
    archivo.close()
    onto.save(val_onto)
    print("Se ha ejecutado la carga amenazas")




# 
def threat_pot_risk(onto, val_onto):
    for t in onto.Threat.instances():
        
        
        
        print((str(t.is_a[2]).split(".")[1])) # Para mostrar los tipos de riesgos producidos (a veces falla y no se por que genera riesgos de tipo Threat o Willful attacks)
        # Generamos el riesgo a partir de la amenaza e introducimos su probabilidad e impacto
        pr = onto.Potential_Risk((str(t.is_a[2]).split(".")[1])+"_Potential_Risk")          # [Threat.Type]_Potential_risk
        pr.probability.append(t.probability[0])
        pr.impact.append(t.impact[0])
        
        
        # Traducimos a valor numérico la probabilidad y el impacto segun ITSRM
        probability = t.probability[0]
        impact = t.impact[0]
        probability_num = probability.replace("VL", "1").replace("VH", "5").replace("M", "3").replace("H", "4").replace("L", "2")
        # impact_num_5 = impact.replace("VL", "1").replace("VH", "5").replace("M", "3").replace("H", "4").replace("L", "2") 
        impact_num = impact.replace("VL", "1").replace("VH", "8").replace("M", "5").replace("H", "6").replace("L", "3") 
        # El impacto se cambia de escala utilizando la equivalencia de ITSRM
        # 1 (0-2)   |   2 (3) |   3 (4-5)   |   4 (6)     |   5 (7-10)
        
        
        # Calculo numerico de riesgo
        risk_level_num = int(probability_num) * int(impact_num)
        
        # Traduccion del riesgo con el excel de Risk Mapping de Enisa siguiendo ITSRM
        if risk_level_num > 16: risk_level = "VH" # =SI(B8>16;"Very High"; 
        elif risk_level_num >= 10 and risk_level_num <= 16: risk_level = "H" #SI(Y(B8>=10;B8<=16);"High";
        elif risk_level_num >= 5 and risk_level_num <= 9: risk_level = "M" #SI(Y(B8>=5;B8<=9);"Moderate";
        elif risk_level_num >= 3 and risk_level_num <= 4: risk_level = "L"  #SI(Y(B8>=3;B8<=4);"Low";
        else: risk_level = "VL" #SI(Y(B8>=1;B8<=2);"Very Low";
        
        # Añadimos los valores de riesgo
        pr.risk_level_num.append(risk_level_num)
        pr.risk_level.append(risk_level)
        
        # Generamos las relaciones de amenaza y riesgo potencial
        pr.related_to.append(t)
        t.generates.append(pr)
    onto.save(val_onto)









def mitigation_to_potential_risk(onto, val_onto):
# PREFIX o:URL es para abreviar y poder obtener los elementos de la ontología
    with onto:
        default_world.sparql("""
			PREFIX o:<http://www.semanticweb.org/carmen/ontologies/2023/6/interoperable_thesis#>
			INSERT {
				?mitigation o:reacts_against ?risk.
				?risk o:is_affected_by ?mitigation.
			}
			WHERE {
				?risk a o:Potential_Risk.
				?threat a o:Unknown.
		 		?threat rdf:type ?x.
		 		?threat o:generates ?risk.
		 		?mitigation a o:Mitigations.
		 		?mitigation o:keywords ?k.
		 		FILTER CONTAINS(str(?x), str(?k))
			}
		""")
        
        default_world.sparql("""
			PREFIX o:<http://www.semanticweb.org/carmen/ontologies/2023/6/interoperable_thesis#>
			INSERT {
				?mitigation o:reacts_against ?risk.
				?risk o:is_affected_by ?mitigation.
			}
			WHERE {
				?risk a o:Potential_Risk.
		 		?threat a o:Threat.
		 		?threat rdf:type ?x.
		 		?threat o:generates ?risk.
		 		?asset a o:Assets.
		 		?threat o:affects ?asset.
		 		?mitigation a o:Mitigations.
		 		?mitigation o:protects ?asset.
		 		?mitigation o:keywords ?k.
		 		FILTER CONTAINS(str(?x), str(?k))
			}
		""")
        default_world.sparql("""
			PREFIX o:<http://www.semanticweb.org/carmen/ontologies/2023/6/interoperable_thesis#>
			INSERT {
				?mitigation o:reacts_against ?risk.
				?risk o:is_affected_by ?mitigation.
			}
			WHERE {
				?risk a o:Potential_Risk.
				?threat a o:Threat.
		 		?threat o:generates ?risk.
		 		?mitigation a o:Mitigations.
		 		?mitigation o:keywords ?k.
		 		FILTER CONTAINS("All", str(?k))
			}
		""")
        onto.save(val_onto)


# Método para comprobar la correcta ponderación de los pesos
def test_pesos(onto):
    print("iniciando test pesos")
    # Inicializamos las variables de pesos a 0
    peso = 0
    Criterio_1= 0       # Es un poco innecesario pero me va a servir para reutilizar el codigo en la selección
    Criterio_2= 0
    
    print("Primer Nivel:  ",onto.Criterio_Primer_Nivel.instances()) # Muestra todos los pesos de primer nivel existentes
    
    # Iniciamos un recorrido por todos los pesos de primer nivel
    for i_Criterio_1 in onto.Criterio_Primer_Nivel.instances():
        Criterio_1 = 0
        print(i_Criterio_1) # Mostrar el peso de nivel 1 actual
        
        # Si el peso de nivel 1 esta dividido comprobamos todos los pesos de nivel 2 asociados
        if i_Criterio_1.is_divided[0]:
            Criterio_2 = 0
            
            # Se hace sumatorio de los valores de peso de los pesos de nivel 2 que forman parte del peso de nivel 1
            for i_Criterio_2 in i_Criterio_1.has_subcriteria:
                Criterio_2 += i_Criterio_2.weight_value[0]
                atributo = (str)(i_Criterio_2).split(".")[1].split("Criterio_2_")[1]  # De esta forma se extrae el <<atributo>>, no es útil para ahora
                print("el peso de nivel 2:", i_Criterio_2, "; con atributo:" ,atributo, "; y valor:", i_Criterio_2.weight_value[0], "; asociado al Criterio_1:", i_Criterio_1)  # Para comprobar
            
            # Comprobar ponderación de los pesos de segundo nivel de cada peso nivel 1
            if Criterio_2 < 1.0 or Criterio_2 > 1.0:
                print("Los pesos de nivel 2 de ", i_Criterio_1," no están correctamente ponderados")
        
        # Sumatorio de los pesos de nivel 1
        Criterio_1 = i_Criterio_1.weight_value[0]
        peso += Criterio_1
    
    print("peso", peso)
    # Se comprueba la ponderación de los pesos de nivel 1
    if peso < 1.0:
        print("Los pesos de nivel 1 no están correctamente ponderados")
        
    print("se ha ejecutado el test pesos")





def selection(onto, val_onto):
    
    # Score es la multiplicación de peso y puntuación | score = weight_value * m.<<atributo>>
    score = 0   # Representa el score total de la mitigación
    score_1 = 0 # Representa el score de cada criterio de nivel 1, es decir, su puntuación multiplicada por su peso
    score_2 = 0 # Representa el score del sumatorio de los scores de cada criterio de nivel 2, para los criterios desglosados, esta será su puntuación
    
    for r in onto.Potential_Risk.instances():
        print()
        print()
        print("el riesgo ",r)
        
        mitigations = r.is_affected_by	
        risk_level = r.risk_level[0].replace("VL", "1").replace("VH", "5").replace("L", "2").replace("M", "3").replace("H", "4")
        
        if len(mitigations) > 0:
            
            score_mitigations = []
            considered_mitigations = []
            
            print("+|","Inicio de mitigations")
            print()
            
            for m in mitigations:
                
                mitigation_impact = m.impact[0].replace("VL", "1").replace("VH", "5").replace("L", "2").replace("M", "3").replace("H", "4")
                if not m.disabled[0] and mitigation_impact <= risk_level:			
                    
                    
                    
                    print()
                    print("+|","La mitigación ",m) # Muestro por pantalla la mitigación 
                    print()
                    score = 0 # Inicializo a 0 para cada mitigación
                    
                    # El sumatorio de todos los pesos de primer nivel 
                    for i_Criterio_1 in onto.Criterio_Primer_Nivel.instances():
                        score_1 = 0 
                        
                        # Si un crtierio de primer nivel esta desglosado, su puntuación es la suma de los scores de los criterios de nivel 2
                        if i_Criterio_1.is_divided[0]:
                            score_2 = 0
                            
                            print("el criterio desglosado", i_Criterio_1)
                            
                            # Sumatorio de los scores de los criterios de nivel 2
                            for i_Criterio_2 in i_Criterio_1.has_subcriteria:
                                # Extraigo el atributo asociado del nombre del peso
                                criterio = (str)(i_Criterio_2).split(".")[1].split("Criterio_2_")[1]
                                # print("+|----","atributo asociado",criterio)
                                
                                # Extraigo el valor de puntuación de la contramedida y la guardo en una variable auxiliar
                                aux_puntuacion = getattr(m,criterio)
                                print("+|----","el criterio_2 (", criterio, ") y su puntuación", aux_puntuacion[0])
                                
                                # Incremento score_2 con el score de este criterio de nivel 2
                                score_2 += i_Criterio_2.weight_value[0] * aux_puntuacion[0]
                                print("+|----","incremento de score_2", score_2)
                            print()
                            print("+|----","score_2 total de (",i_Criterio_1, ") es : ", score_2)
                            # El score del criterio de nivel 1 es su peso por el score_2 obtenido del sumatorio
                            score_1 = i_Criterio_1.weight_value[0] * score_2
                            print(m,i_Criterio_1,score_1)
                            print()
                            
                        # Para los pesos que no esten desglosados
                        else:
                            # Extraigo el atributo asociado del nombre del peso
                            criterio = (str)(i_Criterio_1).split(".")[1].split("Criterio_1_")[1]
                            # print("+|----","atributo asociado",criterio)
                            
                            # Extraigo el valor de puntuación de la contramedida y la guardo en una variable auxiliar distinta
                            aux = getattr(m,criterio)
                            print("+|----","el criterio no desglosado (", criterio, ") y su puntuación", aux[0])
                            
                            # El score del criterio de nivel 1 es el peso por el valor del atributo asociado
                            score_1 = i_Criterio_1.weight_value[0] * aux[0]
                            
                            print(m,i_Criterio_1,score_1)
                            print()
                        
                        # Incremento el score total con el score obtenido del criterio de nivel 1
                        score += score_1
                        print("El score acumulado de (", m, ") es :", score)
                        print()
                        
                    
                    # Muestro el score obtenido de esta mitigación
                    print("Mitigation ", m, "Score ", score)
                    print()
                    
                    # Ambas listas se van añadiendo en el mismo orden, una guarda el score y otra la mitigación
                    score_mitigations.append(score)
                    considered_mitigations.append(m)
                    
                    
            print(score_mitigations)
            print(considered_mitigations)
            if len(considered_mitigations) > 0:
                
                max_mitigation_id = score_mitigations.index(max(score_mitigations)) # Busco la mitigación con más score
                
                print("+|",(str(r).split(".")[1]),"[",(str(considered_mitigations).split(".")[1]),"]") # Muestra por pantalla las mitigaciones consideradas para cada riesgo
                
                print("max score",score_mitigations[max_mitigation_id], "; de la mitigación:", considered_mitigations[max_mitigation_id].id)
                if "Do_Nothing" not in considered_mitigations[max_mitigation_id].id: 
                    print("Se va a aplicar la mitigación: ", considered_mitigations[max_mitigation_id])
                    
                    # La mitigación cambia a enabled true y se inicia el cálculo de riesgo residual
                    considered_mitigations[max_mitigation_id].enabled = [True]
                    residual_risk(onto,r, considered_mitigations[max_mitigation_id], val_onto)
                else:
                    print("Las mitigaciones para el riesgo",r, "no han superado el score de Do_Nothing, por tanto, no se hace nada")
                
		
        else:
            print(r,"No existen mitigaciones para este riesgo")											# No se tendría que llegar a esta parte del código, puesto que siempre estará la mitigación DoNothing
    onto.save(val_onto)
    print("Se ha ejecutado la selección")






def residual_risk(onto,pr,m, val_onto): 
    print("Calculando el riesgo residual de ", pr, "con la mitigación", m)
    s = onto.System_properties
    risk_acceptance = s.risk_acceptance[0].replace("VL", "1").replace("VH", "5").replace("L", "2").replace("M", "3").replace("H", "4")  # Todo sigue con valores no numericos
    mf = (m.mitigation_factor[0])     
    ef = (m.effectiveness[0])         
    mitigation_factor = float((mf*ef)/100) 
    
    
    probability = pr.probability[0]
    impact = pr.impact[0]
    
    probability_num = int(probability.replace("VL", "1").replace("VH", "5").replace("M", "3").replace("H", "4").replace("L", "2")) 
    impact_num = int(impact.replace("VL", "1").replace("VH", "8").replace("M", "5").replace("H", "6").replace("L", "3") ) 
    # El impacto se cambia de escala utilizando la equivalencia de ITSRM
        # 1 (0-2)   |   2 (3) |   3 (4-5)   |   4 (6)     |   5 (7-10)
    
    
    
    
    risk_level = pr.risk_level[0]
    risk_level_accept = risk_level.replace("VL", "1").replace("VH", "5").replace("L", "2").replace("M", "3").replace("H", "4")
    
    if risk_level_accept >= risk_acceptance:
        rr = onto.Residual_Risk((str(pr).split(".")[1].split("Potential")[0])+"Residual_Risk")
        
        
        mitigation_type = m.type[0]
        
        
        
        residual_probability_num = probability_num
        residual_impact_num = impact_num
        risk_level_num = float(probability_num) * (float)(impact_num)
        
        
        
        residual_risk_level_num = 0
        
        if mitigation_type == "Corrective":
            residual_impact_num = float(impact_num) * (1-mitigation_factor)
            residual_probability_num = probability_num
        elif mitigation_type == "Preventive":
            residual_probability_num = int(probability_num) * (1-mitigation_factor)
            residual_impact_num = impact_num
        else:
            residual_risk_level_num = risk_level_num
            
        
        
        
        residual_risk_level_num = float(residual_probability_num) * float(residual_impact_num)
        
        
        
        if residual_risk_level_num > 16: residual_risk_level = "VH" # =SI(B8>16;"Very High"; 
        elif residual_risk_level_num >= 10 and residual_risk_level_num <= 16: residual_risk_level = "H" #SI(Y(B8>=10;B8<=16);"High";
        elif residual_risk_level_num >= 5 and residual_risk_level_num <= 9: residual_risk_level = "M" #SI(Y(B8>=5;B8<=9);"Moderate";
        elif residual_risk_level_num >= 3 and residual_risk_level_num <= 4: residual_risk_level = "L"  #SI(Y(B8>=3;B8<=4);"Low";
        else: residual_risk_level = "VL" #SI(Y(B8>=1;B8<=2);"Very Low";
        
        rr.residual_risk_level = [residual_risk_level]
        rr.residual_risk_level_num = [residual_risk_level_num]
        rr.residual_impact_num = [residual_impact_num]
        rr.residual_probability_num = [residual_probability_num]
        
        
        
        
        # El impacto ahora se cambia de escala utilizando la equivalencia de ITSRM
        # 1 (0-2)   |   2 (3) |   3 (4-5)   |   4 (6)     |   5 (7-10)
        # Y como corresponden con VL-VH se establece de manera directa
        
        if residual_impact_num >= 7: residual_impact = "VH" 
        elif residual_impact_num >= 6 and residual_impact_num < 7: residual_impact = "H" 
        elif residual_impact_num >= 5 and residual_impact_num <= 9: residual_impact = "M" 
        elif residual_impact_num >= 3 and residual_impact_num <= 4: residual_impact = "L"  
        else: residual_impact = "VL"
        
        if residual_probability_num < 2: residual_probability = "VL"     
        elif residual_probability_num < 3: residual_probability = "L"
        elif residual_probability_num < 4: residual_probability = "M"
        elif residual_probability_num < 5: residual_probability = "H"
        else: residual_probability = "VH"
        
        rr.residual_impact = [residual_impact]
        rr.residual_probability = [residual_probability]
        
        m.generates.append(rr)
        pr.generates.append(rr)
        rr.related_to.append(pr)
        rr.related_to.append(m)
    
    
    onto.save(val_onto)




# ----------------------------------------------------------------------------------------------------------- # 



# Configuración de argparse, para pasarle argumentos al script y que sea más cómodo 
def main():
    print("main")
    
    parser = argparse.ArgumentParser(description="Ejecutar métodos con una ontología.")
    parser.add_argument("val_onto", help="Nombre del archivo de la ontología.")
    parser.add_argument("--all", action="store_true", help="Ejecutar todos los métodos. Despliega todo el entorno con todos los procesos en orden.")
    parser.add_argument("--carga_activos", action="store_true", help="Ejecutar carga_activos. Genera los individuos de los activos que se introducen en su catálogo.")
    parser.add_argument("--carga_system", action="store_true", help="Ejecutar carga_system. Genera el individuo System_properties y los sistemas de pesos.")
    parser.add_argument("--carga_amenazas", action="store_true", help="Ejecutar carga_amenazas. Genera los individuos de las amenazas que se introducen en su catálogo.")
    parser.add_argument("--carga_contramedidas", action="store_true", help="Ejecutar carga_contramedidas. Genera los individuos de las contramedidas que se introducen en su catálogo.")
    parser.add_argument("--test_pesos", action="store_true", help="Ejecutar test_pesos. Realiza una ponderación de los valores de peso.")
    parser.add_argument("--threat_pot_risk", action="store_true", help="Ejecutar threat_pot_risk. Genera los individuos de riesgo a través de las amenazas existentes.")
    parser.add_argument("--mitigation_to_potential_risk", action="store_true", help="Ejecutar mitigation_to_potential_risk. Genera la inferencia para relacionar las amenazas y los riesgos adecuadamente.")
    parser.add_argument("--selection", action="store_true", help="Ejecutar selection. Inicia el proceso de selección de contramedidas, este método llama al método de riesgo residual para generar los riesgos residuales derivados.")

    args = parser.parse_args()
    
    # Ontologia
    val_onto = f"{args.val_onto}"
    
    # Cargar la ontología
    onto = get_ontology(val_onto).load()
    
    # Ejecutar métodos de los argumentos
    if args.all or args.carga_activos:
        carga_activos(onto, val_onto)
        time.sleep(4)
    
    if args.all or args.carga_system:
        carga_system(onto, val_onto)
        time.sleep(4)
    
    if args.all or args.carga_amenazas:
        carga_amenazas(onto, val_onto)
        time.sleep(4)
    
    if args.all or args.carga_contramedidas:
        carga_contramedidas(onto, val_onto)
        time.sleep(4)
    
    if args.all or args.test_pesos:
        print("Test pesos")
        test_pesos(onto)
        time.sleep(4)
    
    if args.all or args.threat_pot_risk:
        print("threat_pot_risk")
        threat_pot_risk(onto, val_onto)
        time.sleep(4)
    
    if args.all or args.mitigation_to_potential_risk:
        print("mitigation_to_potential_risk")
        mitigation_to_potential_risk(onto, val_onto)
        time.sleep(4)
    
    if args.all or args.selection:
        selection(onto, val_onto)
        time.sleep(4)

if __name__ == "__main__":
    main()