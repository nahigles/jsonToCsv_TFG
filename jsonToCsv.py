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
reglasCumplidas = False
global porcentajeReglasCumplidasEjecucion


numErrores = 0 # Errores por intento
numErroresNivel = 0 # Errores por nivel
numErroresTotales = 0 # Errores por sesion

numPasosPlanificados = 0 # Pasos planificados por intento
numPasosPlanificadosNivel = 0 # Pasos planificados por nivel
numPasosPlanificadosTotales = 0 # Todos los pasos planificados por sesion

numPasosEjecutados = 0 # Pasos ejecutados por intento
numPasosEjecutadosNivel = 0 # Pasos ejecutados por nivel
numPasosEjecutadosTotales = 0 # Pasos ejecutados por sesion

numPreguntasDormir = 0 # Numero de preguntas de dormir planificadas por intento
numPreguntasDormirNivel = 0 # Numero de preguntas de dormir planificadas por nivel
numPreguntasDormirTotales = 0 # Numero de preguntas de dormir planificadas por sesion

numUbicacionPlanificada = 0 # Numero de envios de ubuicacion planificados por intento
numUbicacionPlanificadaNivel = 0 # Numero de envios de ubuicacion planificados por nivel
numUbicacionPlanificadaTotales = 0 # Numero de envios de ubuicacion planificados por sesion

numParadasHechas = 0 # Intento
numParadasHechasNivel= 0 # Nivel
numParadasHechasTotales = 0 # Sesion

numParadasOmitidas = 0 # Intento
numParadasOmitidasNivel = 0 # Nivel
numParadasOmitidasTotales = 0 # Sesion

numErroresUbicacion = 0
numErroresDormir = 0
numErroresParada = 0
numTiempoExcedido = 0
numIntento = 1

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
    reglasCumplidas = info[10]

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
        reglasCumplidas = True

    elif e == "Se incumplen las reglas":
        reglasCumplidas = False

    elif eValue == "Envio de ubicacion omitido":
        tipoPregunta = 'Ubicacion'
        preguntaCorrecta = 'Erroneo'
        numErrores = numErrores + 1
        numPasosPlanificados += 1
        numUbicacionPlanificada += 1
        numErroresUbicacion += 1
    

    return tipoPregunta, preguntaCorrecta, tiempoSolicitudParada, tiempoSolicitudDormir, writeSleep, writeStop, tiempoExcedido, misionEmpezada, level, cambioNivel, levelPrev, reglasCumplidas


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
data = [['ID','Sesion', 'Nivel', 'Intento', 'Tiempo_Pregunta/Inicio', 'Tiempo_Respuesta/Final','Tiempo_Reaccion/Duracion(s)', 'Tipo_Pregunta','Respuesta', 'Pasos planificados', 'Pasos ejecutados', 'Errores ejecucion', '% Reglas respetadas', 'Num dormir planificado', 'Num ubicacion planificado', 'Paradas hechas', 'Errores ubicacion', 'Errores dormir','Errores parada','Errores por tiempo excedido']]

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
    infoEvent = MCEvent(i,eventName,eventValue, [tipoPregunta, preguntaCorrecta, tiempoSolicitudParada, tiempoSolicitudDormir, writeSleep, writeStop, misionEmpezada, cambioNivel, level, levelPrev, reglasCumplidas])

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
    reglasCumplidas = infoEvent[11]


        # Si es Dormir 
    if tipoPregunta == 'Dormir' and tiempoSolicitudDormir != '-' and writeSleep:
        if not tiempoExcedido:
            reactionTime = calculateTime(tiempoSolicitudDormir, timeStamp)
        else:
            reactionTime = 'Tiempo excedido'

        dataFil = [idSesion[0][-1], idSesion[1][-1],level, numIntento, tiempoSolicitudDormir, timeStamp,reactionTime, tipoPregunta, preguntaCorrecta]
        tiempoSolicitudDormir = '-'
        data.append(dataFil) # Anyado al final de la lista de datos

    # Si es Parada
    elif tipoPregunta == 'Parada' and tiempoSolicitudParada != '-' and writeStop:
        if not tiempoExcedido:
            reactionTime = calculateTime(tiempoSolicitudParada, timeStamp)
        else:
            reactionTime = 'Tiempo excedido'

        dataFil = [idSesion[0][-1], idSesion[1][-1],level,numIntento, tiempoSolicitudParada , timeStamp,reactionTime, tipoPregunta, preguntaCorrecta]
        tiempoSolicitudParada = '-'
        data.append(dataFil) # Anyado al final de la lista de datos

    # Si es Ubicacion lo pongo sinmas
    elif tipoPregunta == 'Ubicacion':
        dataFil = [idSesion[0][-1], idSesion[1][-1],level,numIntento,  timeStamp, '-','-', tipoPregunta, preguntaCorrecta]
        data.append(dataFil) # Anyado al final de la lista de datos

    tipoPregunta = '-'
    preguntaCorrecta = '-'
    
    tiempoEventoAnt = timeStamp # Guarda tiempo del evento anterior
    #print(f"Iteración {i} Num pasos planificados: {numPasosPlanificados}")

    duration = 0
    escribirMetricas = False
    # Guarda tiempo inicio sesion  
    if (not misionEmpezada) or (i == (numEvents-1)):
        if(tiempoInicioMision != '-'):
            if (i == (numEvents-1)):
                tiempoEventoAnt = timeStamp

            duration = calculateTime(tiempoInicioMision, tiempoEventoAnt)

            # Porcentaje de reglas cumplidas
            porcentajeReglasCumplidasEjecucion = 100

            if numErroresDormir > 0:
                porcentajeReglasCumplidasEjecucion -= 25
            if numErroresParada  > 0:
                porcentajeReglasCumplidasEjecucion -= 25
            if numErroresUbicacion  > 0:
                porcentajeReglasCumplidasEjecucion -= 25
            
            # Guarda porcentaje de reglas cumplidas y duracion por mision
            tiemposMisiones.append([porcentajeReglasCumplidasEjecucion, duration])
            tiempoInicioMision = '-'
            misionEmpezada = True
            

            escribirMetricas = True

    else:
        if(tiempoInicioMision == '-'):
            tiempoInicioMision = timeStamp

    # Guarda tiempo nivel
    avanzaNivel = False
    if(not cambioNivel) or (i == (numEvents -1)):
        if tiempoInicioNivel != '-':
            if i == (numEvents - 1):
                tiempoEventoAnt = timeStamp

            duration2 = calculateTime(tiempoInicioNivel, tiempoEventoAnt)
            nivelCompletado = reglasCumplidas and porcentajeReglasCumplidasEjecucion == 100
            tiemposNiveles.append([levelPrev, nivelCompletado, duration2])
            tiempoInicioNivel = '-'
            cambioNivel = True
            #if not (i == (numEvents -1)):
                #numIntento = 1
            avanzaNivel = True
    else:
        if tiempoInicioNivel == '-':
            tiempoInicioNivel = timeStamp

    if escribirMetricas:
            # Ayado metricas por mision
            #paradasHechasText = f"{numParadasHechas}/{numParadasHechas + numParadasOmitidas}"
            dataFil = [idSesion[0][-1], idSesion[1][-1], levelPrev,numIntento,  '', '', duration , 'Final intento', '', numPasosPlanificados, numPasosEjecutados, numErrores, porcentajeReglasCumplidasEjecucion, numPreguntasDormir, numUbicacionPlanificada, f"{numParadasHechas}/{numParadasHechas + numParadasOmitidas}"]
            data.append(dataFil) # Anyado al final de la lista de datos

            # Pasos planificados
            numPasosPlanificadosTotales += numPasosPlanificados
            numPasosPlanificadosNivel += numPasosPlanificados
            numPasosPlanificados = 0

            # Pasos ejecutados
            numPasosEjecutadosTotales += numPasosEjecutados
            numPasosEjecutadosNivel += numPasosEjecutados
            numPasosEjecutados = 0

            # Errores
            numErroresTotales += numErrores
            numErroresNivel += numErrores
            numErrores = 0

            # Preguntas dormir planificadas
            numPreguntasDormirTotales += numPreguntasDormir
            numPreguntasDormirNivel += numPreguntasDormir
            numPreguntasDormir = 0

            # Preguntas ubicacion planificadas
            numUbicacionPlanificadaTotales += numUbicacionPlanificada
            numUbicacionPlanificadaNivel += numUbicacionPlanificada
            numUbicacionPlanificada = 0

            # Paradas hechas y omitidas
            numParadasHechasTotales += numParadasHechas
            numParadasHechasNivel += numParadasHechas
            numParadasHechas = 0

            numParadasOmitidasTotales += numParadasOmitidas
            numParadasOmitidasNivel += numParadasOmitidas
            numParadasOmitidas = 0

            if not avanzaNivel:
                numIntento += 1
            else:
                dataFil = [idSesion[0][-1], idSesion[1][-1], levelPrev,numIntento,  '', '', duration2 , 'Final nivel', '', numPasosPlanificadosNivel, numPasosEjecutadosNivel, numErroresNivel, '', numPreguntasDormirNivel, numUbicacionPlanificadaNivel,  f"{numParadasHechasNivel}/{numParadasHechasNivel + numParadasOmitidasNivel}"]
                data.append(dataFil) # Anyado al final de la lista de datos
                avanzaNivel = False
                numPasosPlanificadosNivel = 0
                numPasosEjecutadosNivel = 0
                numErroresNivel = 0
                numPreguntasDormirNivel = 0
                numUbicacionPlanificadaNivel = 0
                numParadasHechasNivel = 0
                numParadasOmitidasNivel = 0

                numIntento = 1

            escribirMetricas = False

dataFil = ['Metricas sesion:']
data.append(dataFil) # Anyado al final de la lista de datos
dataFil = [idSesion[0][-1], idSesion[1][-1], len(tiemposNiveles),len(tiemposMisiones),  '', '','', '', '', numPasosPlanificadosTotales, numPasosEjecutadosTotales, numErroresTotales,'', numPreguntasDormirTotales, numUbicacionPlanificadaTotales, f"{numParadasHechasTotales}/{numParadasHechasTotales + numParadasOmitidasTotales}"]
data.append(dataFil) # Anyado al final de la lista de datos


print(f"Num pasos planificados: {numPasosPlanificadosTotales} \nNum pasos ejecutados: {numPasosEjecutadosTotales} \nNum dormir planificado: {numPreguntasDormirTotales} \nNum ubicacion planificado: {numUbicacionPlanificadaTotales} \nNum paradas hechas: {numParadasHechasTotales}/{numParadasHechasTotales + numParadasOmitidasTotales}") # Esto por usuario
print(f"\nNum errores: {numErroresTotales} \nNum errores ubi: {numErroresUbicacion} \nNum errores dormir: {numErroresDormir} \nNum errores parada: {numErroresParada} \nError por tiempo excedido: {numTiempoExcedido}")
print(f"\nTiempos misiones: {tiemposMisiones}")
print(f"Tiempos niveles: {tiemposNiveles}")

# Abro archivo .csv para guardar los datos leidos
file =  open('../datos.csv', 'w', newline='')
writer = csv.writer(file)
writer.writerows(data)
file.close()


