import csv
import json

tipoPregunta = '-'
preguntaCorrecta = '-'
tiempoSolicitudParada = '-'
tiempoSolicitudDormir = '-'
timeStamp = ''
writeSleep = False
writeStop = False

numErrores = 0

# Si tiempoSolicitudParada o tiempoSolicitudDormir es  - es que no hay pregunta

def MCEvent(i, e, info): 

    tipoPregunta = info[0]
    preguntaCorrecta = info[1]
    tiempoSolicitudParada = info[2]
    tiempoSolicitudDormir = info[3]
    writeSleep = info[4]
    writeStop = info[5]

    global numErrores

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
        numErrores = numErrores + 1

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
        numErrores = numErrores + 1

    elif e == "Tiempo de respuesta excedido":
        preguntaCorrecta = 'Erroneo'
        numErrores = numErrores + 1
        #tiempoSolicitudDormir = 'No respuesta'
        #tiempoSolicitudParada = 'No respuesta'

    elif e == "Se cumplen las reglas":
        a = ''
    elif e == "Se incumplen las reglas":
        b = ''

    return tipoPregunta, preguntaCorrecta, tiempoSolicitudParada, tiempoSolicitudDormir, writeSleep, writeStop


def calculateTime(t1,t2):
    t1s = t1.split(':')
    t2s = t2.split(':')
    t =(float(t2s[1]) - float(t1s[1]))*60.0 + (float(t2s[2]) - float(t1s[2]))

    t = round(t, 6)
    return t


ruta =  "../Mision Colombia/"
name = "2_MisionColombia_2025-10-30_1.json"

with open(ruta + name) as archivo:
    datos_JSON = json.load(archivo)


numEvents = len(datos_JSON[name]) # Numero de eventos del json

# ID del paciente y numero de sesion
txt = datos_JSON[name][0]["Eventos"][0]["Paciente y numero de sesion"]

splitText = txt.split(", ")

# Fecha y Tiempo
txt = datos_JSON[name][0]["Tiempo"]
splitT = txt.split(" ")
date = splitT[0]
timeStamp = splitT[1]
level = datos_JSON[name][1]['Eventos'][0]["Iniciando juego"][-1]

# Datos con los titulos de cada columna
data = [['ID','Sesion', 'Nivel', 'Tiempo_Pregunta', 'Tiempo_Respuesta','Tiempo_Reaccion', 'Tipo_Pregunta','Respuesta']]

# Siguiente fila que quiero anyadir
#dataFil = [splitText[0][-1], splitText[1][-1],level,  timeStamp, 9.0, '-','-','-']
#data.append(dataFil) # Anyado al final de la lista de datos



# Voy anyadiendo siguientes filas
for i in range(2,numEvents):
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
  
    # Si es Dormir 
    if tipoPregunta == 'Dormir' and tiempoSolicitudDormir != '-' and writeSleep:
        reactionTime = calculateTime(tiempoSolicitudDormir, timeStamp)
        dataFil = [splitText[0][-1], splitText[1][-1],level,  tiempoSolicitudDormir, timeStamp,reactionTime, tipoPregunta, preguntaCorrecta]
        tiempoSolicitudDormir = '-'
        data.append(dataFil) # Anyado al final de la lista de datos

    # Si es Parada
    elif tipoPregunta == 'Parada' and tiempoSolicitudParada != '-' and writeStop:
        reactionTime = calculateTime(tiempoSolicitudParada, timeStamp)
        dataFil = [splitText[0][-1], splitText[1][-1],level, tiempoSolicitudParada , timeStamp,reactionTime, tipoPregunta, preguntaCorrecta]
        tiempoSolicitudParada = '-'
        data.append(dataFil) # Anyado al final de la lista de datos

    # Si es Ubicacion lo pongo sinmas
    # Siguiente fila que quiero anyadir
    elif tipoPregunta == 'Ubicacion':
        dataFil = [splitText[0][-1], splitText[1][-1],level,  timeStamp, '-','-', tipoPregunta, preguntaCorrecta]
        data.append(dataFil) # Anyado al final de la lista de datos

    tipoPregunta = '-'
    preguntaCorrecta = '-'
    
    #print(f"Iteración {i}")

print(f"Num errores: {numErrores}") # Esto por usuario

# Abro archivo .csv para guardar los datos leidos
file =  open('../datos.csv', 'w', newline='')
writer = csv.writer(file)
writer.writerows(data)
file.close()


