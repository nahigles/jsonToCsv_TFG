import csv
import json

tipoPregunta = '-'
preguntaCorrecta = '-'
tiempoSolicitudParada = '-'
tiempoSolicitudDormir = '-'
timeStamp = ''
writeSleep = False
writeStop = False
tiempoExcedido = False
misionEmpezada = False
tiempoInicioMision = '-'
tiempoEventoAnt = '-'
cambioNivel = False
tiempoInicioNivel = '-'

numErrores = 0
numPasosPlanificados = 0
numPasosEjecutados = 0
numPreguntasDormir = 0
numUbicacionPlanificada = 0
numErroresUbicacion = 0
numErroresDormir = 0
numErroresParada = 0
numTiempoExcedido = 0
numParadasHechas = 0
numParadasOmitidas = 0

tiemposMisiones = []
tiemposNiveles = []


def MCEvent(i, e, eValue, info): 

    tipoPregunta = info[0]
    preguntaCorrecta = info[1]
    tiempoSolicitudParada = info[2]
    tiempoSolicitudDormir = info[3]
    writeSleep = info[4]
    writeStop = info[5]
    tiempoExcedido = False
    misionEmpezada = info[6]
    cambioNivel = info[7]
    level = info[8]
    levelPrev = info[9]

    global numErrores
    global numPasosPlanificados
    global numPasosEjecutados
    global numPreguntasDormir
    global numUbicacionPlanificada
    global numErroresUbicacion
    global numErroresDormir
    global numErroresParada
    global numTiempoExcedido
    global numParadasHechas
    global numParadasOmitidas


    if e == "Paciente y numero de sesion":
        a = ''

    elif e == "Iniciando juego":
            misionEmpezada = not misionEmpezada
            levelPrev = level
            level = eValue[-1]
            if (levelPrev != level):
                cambioNivel = not cambioNivel


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
         numParadasHechas += 1

    elif e == "Respuesta de parada NO":
         tipoPregunta = 'Parada'
         writeStop = True
         numParadasOmitidas += 1

    elif e == "Solicitud de dormir":
        tipoPregunta = 'Dormir'
        tiempoSolicitudDormir = timeStamp
        writeSleep = False
        numPasosPlanificados += 1
        numPreguntasDormir += 1

    elif e == "Respuesta de dormir SI":
        tipoPregunta = 'Dormir'
        preguntaCorrecta = 'Correcto'
        writeSleep = True
        numPasosEjecutados = numPasosEjecutados + 1

    elif e == "Respuesta de dormir NO":
        tipoPregunta = 'Dormir'
        preguntaCorrecta = 'Erroneo'
        writeSleep = True
        numErrores = numErrores + 1
        numErroresDormir += 1

    elif e == "Inicio de dormir":
        c = ''
    elif e == "Ubcacion enviada":
        tipoPregunta = 'Ubicacion'

    elif e == "Ubicacion bien enviada":
        tipoPregunta = 'Ubicacion'
        preguntaCorrecta = 'Correcto'
        numPasosPlanificados += 1
        numPasosEjecutados = numPasosEjecutados + 1
        numUbicacionPlanificada += 1

    elif e == "Tiempo de respuesta excedido":
        preguntaCorrecta = 'Erroneo'
        numErrores = numErrores + 1
        numTiempoExcedido += 1

        if tiempoSolicitudDormir != '-':
            tipoPregunta = 'Dormir'
            writeSleep = True
            numErroresDormir += 1
        elif tiempoSolicitudParada != '-':
            tipoPregunta = 'Parada'
            writeStop = True
            numErroresParada += 1

        tiempoExcedido = True

    elif e == "Se cumplen las reglas":
        a = ''
    elif e == "Se incumplen las reglas":
        b = ''
    elif eValue == "Envio de ubicacion omitido":
        tipoPregunta = 'Ubicacion'
        preguntaCorrecta = 'Erroneo'
        numErrores = numErrores + 1
        numPasosPlanificados += 1
        numUbicacionPlanificada += 1
        numErroresUbicacion += 1
    

    return tipoPregunta, preguntaCorrecta, tiempoSolicitudParada, tiempoSolicitudDormir, writeSleep, writeStop, tiempoExcedido, misionEmpezada, level, cambioNivel, levelPrev


def calculateTime(t1,t2):
    t1s = t1.split(':')
    t2s = t2.split(':')
    t =(float(t2s[0]) - float(t1s[0]))*60*60 + (float(t2s[1]) - float(t1s[1]))*60.0 + (float(t2s[2]) - float(t1s[2]))

    t = round(t, 6)
    return t


ruta =  "../Mision Colombia/"
name = "2_MisionColombia_2025-10-30_1.json"

with open(ruta + name) as archivo:
    datos_JSON = json.load(archivo)


numEvents = len(datos_JSON[name]) # Numero de eventos del json

# ID del paciente y numero de sesion
txt = datos_JSON[name][0]["Eventos"][0]["Paciente y numero de sesion"]
idSesion = txt.split(", ")

# Datos con los titulos de cada columna
data = [['ID','Sesion', 'Nivel', 'Tiempo_Pregunta', 'Tiempo_Respuesta','Tiempo_Reaccion', 'Tipo_Pregunta','Respuesta']]

level = -1
levelPrev = -1

# Voy anyadiendo siguientes filas
for i in range(1,numEvents):

    # Fecha y Tiempo
    txt = datos_JSON[name][i]["Tiempo"]
    splitT = txt.split(" ")
    date = splitT[0]
    timeStamp = splitT[1]

    eventName = list(datos_JSON[name][i]["Eventos"][0].keys())[0]
    eventValue = list(datos_JSON[name][i]["Eventos"][0].values())[0]
    infoEvent = MCEvent(i,eventName,eventValue, [tipoPregunta, preguntaCorrecta, tiempoSolicitudParada, tiempoSolicitudDormir, writeSleep, writeStop, misionEmpezada, cambioNivel, level, levelPrev])

    tipoPregunta = infoEvent[0]
    preguntaCorrecta = infoEvent[1]
    tiempoSolicitudParada = infoEvent[2]
    tiempoSolicitudDormir = infoEvent[3]
    writeSleep = infoEvent[4]
    writeStop = infoEvent[5]
    tiempoExcedido = infoEvent[6]
    misionEmpezada = infoEvent[7]
    level = infoEvent[8]
    cambioNivel = infoEvent[9]
    levelPrev = infoEvent[10]

    # Guarda tiempo inicio sesion  
    if (not misionEmpezada) or (i == (numEvents-1)):
        if(tiempoInicioMision != '-'):
            if (i == (numEvents-1)):
                tiempoEventoAnt = timeStamp

            duration = calculateTime(tiempoInicioMision, tiempoEventoAnt)
            tiemposMisiones.append(duration)
            tiempoInicioMision = '-'
            misionEmpezada = True
    else:
        if(tiempoInicioMision == '-'):
            tiempoInicioMision = timeStamp

    # Guarda tiempo nivel
    if(not cambioNivel) or (i == (numEvents -1)):
        if tiempoInicioNivel != '-':
            if i == (numEvents - 1):
                tiempoEventoAnt = timeStamp

            duration = calculateTime(tiempoInicioNivel, tiempoEventoAnt)
            tiemposNiveles.append([levelPrev,duration])
            tiempoInicioNivel = '-'
            cambioNivel = True
    else:
        if tiempoInicioNivel == '-':
            tiempoInicioNivel = timeStamp

    # Si es Dormir 
    if tipoPregunta == 'Dormir' and tiempoSolicitudDormir != '-' and writeSleep:
        if not tiempoExcedido:
            reactionTime = calculateTime(tiempoSolicitudDormir, timeStamp)
        else:
            reactionTime = 'Tiempo excedido'

        dataFil = [idSesion[0][-1], idSesion[1][-1],level,  tiempoSolicitudDormir, timeStamp,reactionTime, tipoPregunta, preguntaCorrecta]
        tiempoSolicitudDormir = '-'
        data.append(dataFil) # Anyado al final de la lista de datos

    # Si es Parada
    elif tipoPregunta == 'Parada' and tiempoSolicitudParada != '-' and writeStop:
        if not tiempoExcedido:
            reactionTime = calculateTime(tiempoSolicitudParada, timeStamp)
        else:
            reactionTime = 'Tiempo excedido'

        dataFil = [idSesion[0][-1], idSesion[1][-1],level, tiempoSolicitudParada , timeStamp,reactionTime, tipoPregunta, preguntaCorrecta]
        tiempoSolicitudParada = '-'
        data.append(dataFil) # Anyado al final de la lista de datos

    # Si es Ubicacion lo pongo sinmas
    elif tipoPregunta == 'Ubicacion':
        dataFil = [idSesion[0][-1], idSesion[1][-1],level,  timeStamp, '-','-', tipoPregunta, preguntaCorrecta]
        data.append(dataFil) # Anyado al final de la lista de datos

    tipoPregunta = '-'
    preguntaCorrecta = '-'
    
    tiempoEventoAnt = timeStamp # Guarda tiempo del evento anterior
    #print(f"Iteración {i} Num pasos planificados: {numPasosPlanificados}")

print(f"Num pasos planificados: {numPasosPlanificados} \nNum pasos ejecutados: {numPasosEjecutados} \nNum dormir planificado: {numPreguntasDormir} \nNum ubicacion planificado: {numUbicacionPlanificada} \nNum paradas hechas: {numParadasHechas}/{numParadasHechas + numParadasOmitidas}") # Esto por usuario
print(f"\nNum errores: {numErrores} \nNum errores ubi: {numErroresUbicacion} \nNum errores dormir: {numErroresDormir} \nNum errores parada: {numErroresParada} \nError por tiempo excedido: {numTiempoExcedido}")
print(f"\nTiempos misiones: {tiemposMisiones}")
print(f"Tiempos niveles: {tiemposNiveles}")

# Abro archivo .csv para guardar los datos leidos
file =  open('../datos.csv', 'w', newline='')
writer = csv.writer(file)
writer.writerows(data)
file.close()


