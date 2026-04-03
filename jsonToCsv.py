import csv
import json

tiempoSolicitudParada = ''
tiempoSolicitudDormir = ''
timeStamp = ''

# Si tiempoSolicitudParada o tiempoSolicitudDormir es  - es que no hay pregunta

def MCEvent(i, e): 

    tipoPregunta = '-'
    preguntaCorrecta = '-'

    if e == "Paciente y numero de sesion":
        print(f"{e} is a weekend.")

    elif e == "Iniciando juego":
        print(f"{e} is a weekend.")

    elif e == "Empieza pregunta y decision":
        print(f"{e} is a weekend.")
    elif e == "Termina pregunta y decision":
        print(f"{e} is a weekday.")
    elif e == "Planificacion guardada":
        print(f"{e} is a weekday.")

    elif e == "Hora de salda seleccionada":
        print(f"{e} is a weekday.")

    elif e == "Solicitud de parada":
        tipoPregunta = 'Parada'
        tiempoSolicitudParada = timeStamp
        print(f"{e} is a weekday.")

    elif e == "Respuesta de parada SI":
        print(f"{e} is a weekday.")

    elif e == "Respuesta de parada NO":
        print(f"{e} is a weekday.")

    elif e == "Solicitud de dormir":
        tipoPregunta = 'Dormir'
        tiempoSolicitudDormir = timeStamp
        print(f"{e} is a weekday.")

    elif e == "Respuesta de dormir SI":
        preguntaCorrecta = 'Correcto'
        print(f"{e} is a weekday.")  

    elif e == "Respuesta de dormir NO":
        preguntaCorrecta = 'Erroneo'
        print(f"{e} is a weekday.")  

    elif e == "Inicio de dormir":
        print(f"{e} is a weekday.")

    elif e == "Ubcacion enviada":
        tipoPregunta = 'Ubicacion'
        print(f"{e} is a weekday.")

    elif e == "Ubicacion bien enviada":
        preguntaCorrecta = 'Correcto'
        print(f"{e} is a weekday.")

    elif e == "Envio de ubicación omitido":
        preguntaCorrecta = 'Erroneo'
        print(f"{e} is a weekday.")

    elif e == "Tiempo de respuesta excedido":
        preguntaCorrecta = 'Erroneo'
        print(f"{e} is a weekday.")

    elif e == "Se cumplen las reglas":
        print(f"{e} is a weekday.")
    elif e == "Se incumplen las reglas":
        print(f"{e} is a weekday.")

    return tipoPregunta, preguntaCorrecta

    # EventosInfo.MCEmpiezaDecision, "Empieza pregunta y decision" },
    #     { EventosInfo.MCTerminaDecision, "Termina pregunta y decision" },
    #     { EventosInfo.MCPlanifcacionGuardada, "Planificacion guardada" },
    #     { EventosInfo.MCHoraSalidaSeleccionada, "Hora de salda seleccionada" },
    #     { EventosInfo.MCPreguntaParada, "Solicitud de parada" },
    #     { EventosInfo.MCRespuestaParadaSi, "Respuesta de parada SI" },
    #     { EventosInfo.MCRespuestaParadaNo, "Respuesta de parada NO" },
    #     { EventosInfo.MCPreguntaDormir, "Solicitud de dormir" },
    #     { EventosInfo.MCRespuestaDormirSi, "Respuesta de dormir SI" },
    #     { EventosInfo.MCRespuestaDormirNo, "Respuesta de dormir NO" },
    #     { EventosInfo.MCComienzoDormir, "Inicio de dormir" },
    #     { EventosInfo.MCTerminoDormir, "Final de dormir" },
    #     { EventosInfo.MCUbicacionEnviada, "Ubcacion enviada" },
    #     { EventosInfo.MCUbicacionEnviadaBien, "Ubicacion bien enviada" },
    #     { EventosInfo.MCUbicacionOmisionEnvio, "Envio de ubicación omitido" },
    #     { EventosInfo.MCPreguntaSinRespuesta, "Tiempo de respuesta excedido" },
    #     { EventosInfo.MCReglasCumplidas, "Se cumplen las reglas" },
    #     { EventosInfo.MCReglasIncumplidas, "Se incumplen las reglas" },


ruta =  "Mision Colombia/"
name = "2_MisionColombia_2025-10-30_1.json"

with open(ruta + name) as archivo:
    datos_JSON = json.load(archivo)


numEvents = len(datos_JSON[name]) # Numero de eventos del json
print(len(datos_JSON[name]))
print(datos_JSON[name][0]["Tiempo"])

# ID del paciente y numero de sesion
txt = datos_JSON[name][0]["Eventos"][0]["Paciente y numero de sesion"]
print(datos_JSON[name][0]["Eventos"][0]["Paciente y numero de sesion"])

splitText = txt.split(", ")
print("P: " + splitText[0][-1])
print("S: " + splitText[1][-1])

# Fecha y Tiempo
print(datos_JSON[name][0]["Tiempo"])
txt = datos_JSON[name][0]["Tiempo"]
splitT = txt.split(" ")
date = splitT[0]
timeStamp = splitT[1]

# Datos con los titulos de cada columna
data = [['ID','Sesion', 'Nivel', 'Tiempo_Pregunta', 'Tiempo_Respuesta','Tiempo_Reaccion', 'Tipo_Pregunta','Respuesta']]

# Siguiente fila que quiero anyadir
dataFil = [splitText[0][-1], splitText[1][-1],1,  timeStamp, 9.0, '-','-','-']
data.append(dataFil) # Anyado al final de la lista de datos



# Voy anyadiendo siguientes filas
for i in range(1,numEvents):
    print(datos_JSON[name][i]["Tiempo"])
    txt = datos_JSON[name][i]["Tiempo"]
    splitT = txt.split(" ")
    date = splitT[0]
    timeStamp = splitT[1]

    eventName = list(datos_JSON[name][i]["Eventos"][0].keys())[0]
    infoEvent = MCEvent(i,eventName)


    # Siguiente fila que quiero anyadir
    dataFil = [splitText[0][-1], splitText[1][-1],1,  timeStamp, 9.0,'-', infoEvent[0], infoEvent[1]]
    data.append(dataFil) # Anyado al final de la lista de datos
    print(f"Iteración {i}")



# data = [['ID','Sesion', 'Tiempo_Pregunta', 'Tiempo_Respuesta','Respuesta'],
#      [slitText[0][-1], slitText[1][-1], 2, 9.0, 'Correcta'],
#      ['Sanchit', 'COE', 2, 9.1, 'Correcta'],
#      ['Aditya', 'IT', 2, 9.3, 'Correcta'],
#      ['Sagar', 'SE', 1, 9.5, 'Correcta'],
#      ['Prateek', 'MCE', 3, 7.8, 'Correcta'],
#      ['Sahil', 'EP', 2, 9.1, 'Correcta']]

# Abro archivo .csv para guardar los datos leidos
file =  open('datos.csv', 'w', newline='')
writer = csv.writer(file)
writer.writerows(data)
file.close()


