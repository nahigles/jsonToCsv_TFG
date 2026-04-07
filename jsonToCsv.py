import csv
import json

tipoPregunta = '-'
preguntaCorrecta = '-'
tiempoSolicitudParada = '-'
tiempoSolicitudDormir = '-'
timeStamp = ''
writeSleep = False
writeStop = False

# Si tiempoSolicitudParada o tiempoSolicitudDormir es  - es que no hay pregunta

def MCEvent(i, e, info): 

# info = [tipoPregunta, preguntaCorrecta, tiempoSolicitudParada, tiempoSolicitudDormir]
    tipoPregunta = info[0]
    preguntaCorrecta = info[1]
    tiempoSolicitudParada = info[2]
    tiempoSolicitudDormir = info[3]
    writeSleep = info[4]
    writeStop = info[5]

    # tipoPregunta = '-'
    # preguntaCorrecta = '-'
    # tiempoSolicitudParada = '-'
    # tiempoSolicitudDormir = '-'

    if e == "Paciente y numero de sesion":
        a = ''

    elif e == "Iniciando juego":
        a = ''

    elif e == "Empieza pregunta y decision":
        a = ''
    elif e == "Termina pregunta y decision":
        a = ''
    elif e == "Planificacion guardada":
        f = ''

    elif e == "Hora de salda seleccionada":
        e = ''

    elif e == "Solicitud de parada":
        tipoPregunta = 'Parada'
        tiempoSolicitudParada = timeStamp
        writeStop = False

    elif e == "Respuesta de parada SI":
         tipoPregunta = 'Parada'
         writeStop = True

    elif e == "Respuesta de parada NO":
         tipoPregunta = 'Parada'
         writeStop = True

    elif e == "Solicitud de dormir":
        tipoPregunta = 'Dormir'
        tiempoSolicitudDormir = timeStamp
        writeSleep = False

    elif e == "Respuesta de dormir SI":
        tipoPregunta = 'Dormir'
        preguntaCorrecta = 'Correcto'
        writeSleep = True

    elif e == "Respuesta de dormir NO":
        tipoPregunta = 'Dormir'
        preguntaCorrecta = 'Erroneo'
        writeSleep = True

    elif e == "Inicio de dormir":
        c = ''
    elif e == "Ubcacion enviada":
        tipoPregunta = 'Ubicacion'

    elif e == "Ubicacion bien enviada":
        tipoPregunta = 'Ubicacion'
        preguntaCorrecta = 'Correcto'

    elif e == "Envio de ubicación omitido":
        tipoPregunta = 'Ubicacion'
        preguntaCorrecta = 'Erroneo'

    elif e == "Tiempo de respuesta excedido":
        preguntaCorrecta = 'Erroneo'

    elif e == "Se cumplen las reglas":
        a = ''
    elif e == "Se incumplen las reglas":
        b = ''

    return tipoPregunta, preguntaCorrecta, tiempoSolicitudParada, tiempoSolicitudDormir, writeSleep, writeStop


ruta =  "../Mision Colombia/"
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
    #print(datos_JSON[name][i]["Tiempo"])
    txt = datos_JSON[name][i]["Tiempo"]
    splitT = txt.split(" ")
    date = splitT[0]
    timeStamp = splitT[1]

    eventName = list(datos_JSON[name][i]["Eventos"][0].keys())[0]
    infoEvent = MCEvent(i,eventName, [tipoPregunta, preguntaCorrecta, tiempoSolicitudParada, tiempoSolicitudDormir, writeSleep, writeStop])

    tipoPregunta = infoEvent[0]
    preguntaCorrecta = infoEvent[1]
    tiempoSolicitudParada = infoEvent[2]
    tiempoSolicitudDormir = infoEvent[3]
    writeSleep = infoEvent[4]
    writeStop = infoEvent[5]

# Escribo si ell tiempoubi no esta en - y es ubi o so tiempo dormir no esta en - y es dormir (negando todo eso)
# significa que no esta pendiente de dale a responder
    #if not((tiempoSolicitudDormir != '-' and tipoPregunta == 'Dormir') or (tiempoSolicitudParada  != '-' and tipoPregunta == 'Parada')):
    
    #Escribo dormir cuando el tipo sea dormir y tiempo solicitud dormir no sea -    
       
    # Si es Dormir 
    if tipoPregunta == 'Dormir' and tiempoSolicitudDormir != '-' and writeSleep:
        print(f"Tiempo Solicitud dormir: {tiempoSolicitudDormir} y Tiempo sol parada: {tiempoSolicitudParada} ,Tipo: {infoEvent[0]}")  
        print(f"HAGYDSBSUAYHDGBUASYGHDBIHDGY: {tipoPregunta}")
        dataFil = [splitText[0][-1], splitText[1][-1],1,  tiempoSolicitudDormir, timeStamp,7, tipoPregunta, preguntaCorrecta]
        tiempoSolicitudDormir = '-'
        data.append(dataFil) # Anyado al final de la lista de datos
    # Si es Parada
    elif tipoPregunta == 'Parada' and tiempoSolicitudParada != '-' and writeStop:
        dataFil = [splitText[0][-1], splitText[1][-1],1, tiempoSolicitudParada , timeStamp,8, tipoPregunta, preguntaCorrecta]
        tiempoSolicitudParada = '-'
        data.append(dataFil) # Anyado al final de la lista de datos
    # Si es Ubicacion lo pongo sinmas
    # Siguiente fila que quiero anyadir
    elif tipoPregunta == 'Ubicacion':
        dataFil = [splitText[0][-1], splitText[1][-1],1,  timeStamp, '-',8, tipoPregunta, preguntaCorrecta]
        data.append(dataFil) # Anyado al final de la lista de datos
    #print(f"Tiempo Solicitud dormir: {tiempoSolicitudDormir} y Tiempo sol parada: {tiempoSolicitudParada} ,Tipo: {infoEvent[0]}")

    tipoPregunta = '-'
    preguntaCorrecta = '-'
    #tiempoSolicitudParada = '-'
    #tiempoSolicitudDormir = '-'
    
    print(f"Iteración {i}")


# Abro archivo .csv para guardar los datos leidos
file =  open('../datos.csv', 'w', newline='')
writer = csv.writer(file)
writer.writerows(data)
file.close()


