import csv
import json
import os
import pandas as pd

# Datos en crudo
tipoEvento = '-'
timeStamp = ''
numIntento = 0
cambioNivel = False

# Datos tipo pregunta y tiempo reaccion
tipoPregunta = '-'
preguntaCorrecta = '-'
tiempoSolicitudParada = '-'
tiempoSolicitudDormir = '-'
writeSleep = False
writeStop = False
tiempoExcedido = False

# Datos por intento
tiempoInicioIntento = ''
tiempoFinalIntento = ''
tiempoDuracionIntento = ''
completado = False
reglasPlanificacionCumplidas = False
reglasEjecucionCumplidas = 100
numPasosPlanificados = 0
numPasosEjecutados = 0
numErroresEjecucion = 0
numDormirPlanificado = 0
correctosDormir = 0
erroresDormir = 0
numUbicacionPlanificado = 0
correctosUbicacion = 0
erroresUbicacion = 0
paradasPosibles = 0
paradasRealizadas = 0
erroresParadaTiempoExcedido = 0
erroresTiempoExcedido = 0

inicioSesion = True

def MCEvent(i, e, eValue, info): 

    tipoEvento = info[0]
    cambioNivel = info[1]
    level = info[2]
    levelPrev = info[3]
    tiempoSolicitudParada = info[4]
    tiempoSolicitudDormir = info[5]
    tipoPregunta = info[6]
    preguntaCorrecta = info[7]

    if e == "Paciente y numero de sesion":
        tipoEvento = 'Paciente y número de sesion guardado'

    elif e == "Iniciando juego":
            cambioNivel = False
            tipoEvento = 'Inicio juego'
            levelPrev = level
            level = eValue[-1]
            if (levelPrev != level):
                cambioNivel = True

    elif e == "Empieza pregunta y decision":
        tipoEvento = 'Empieza pregunta y decision'
    elif e == "Termina pregunta y decision":
        tipoEvento = 'Termina pregunta y decision'
    elif e == "Planificacion guardada":
        tipoEvento = 'Planificacion guardada'

    elif e == "Hora de salda seleccionada":
        tipoEvento = 'Hora salida seleccionada'

    elif e == "Solicitud de parada":
        tipoEvento = 'Pregunta parada'
        tiempoSolicitudParada = timeStamp

    elif e == "Respuesta de parada SI":
        tipoEvento = 'Respuesta parada Si'
        tipoPregunta = 'Parada'

    elif e == "Respuesta de parada NO":
        tipoEvento = 'Respuesta parada No'
        tipoPregunta = 'Parada'

    elif e == "Solicitud de dormir":
        tipoEvento = 'Pregunta dormir'
        tiempoSolicitudDormir = timeStamp

    elif e == "Respuesta de dormir SI":
        tipoEvento = 'Respuesta dormir Si'
        tipoPregunta = 'Dormir'
        preguntaCorrecta = 'Correcto'

    elif e == "Respuesta de dormir NO":
        tipoEvento = 'Respuesta dormir No'
        tipoPregunta = 'Dormir'
        preguntaCorrecta = 'Erroneo'

    elif e == "Inicio de dormir":
        tipoEvento = 'Empieza a dormir'
    elif e == "Ubcacion enviada":
        tipoEvento = 'Ubicacion enviada'

    elif e == "Ubicacion bien enviada":
        tipoEvento = 'Ubicacion bien enviada'
        tipoPregunta = 'Ubicacion'
        preguntaCorrecta = 'Correcto'

    elif e == "Tiempo de respuesta excedido":
        tipoEvento = 'Tiempo excedido'
        preguntaCorrecta = 'Erroneo'
        if tiempoSolicitudDormir != '-':
            tipoPregunta = 'Dormir'
        elif tiempoSolicitudParada != '-':
            tipoPregunta = 'Parada'
        

    elif e == "Se cumplen las reglas":
        tipoEvento = 'Reglas cumplidas'

    elif e == "Se incumplen las reglas":
        tipoEvento = 'Reglas incumplidas'
    
    elif e == "Acabado":
        tipoEvento = 'Acabado'

    elif eValue == "Envio de ubicacion omitido":
        tipoEvento = 'Envio ubicacion omitido'
        tipoPregunta = 'Ubicacion'
        preguntaCorrecta = 'Erroneo'
    

    return tipoEvento, cambioNivel, level, levelPrev, tiempoSolicitudParada, tiempoSolicitudDormir, tipoPregunta, preguntaCorrecta

def calculateTime(t1,t2):
    t1s = t1.split(':')
    t2s = t2.split(':')
    t =(float(t2s[0]) - float(t1s[0]))*60*60 + (float(t2s[1]) - float(t1s[1]))*60.0 + (float(t2s[2]) - float(t1s[2]))

    t = round(t, 6)
    return t

def getDateTime(txt):
    splitT = txt.split(" ")
    date = splitT[0]
    time = splitT[1]
    return date,time

def saveCsvExcel(fileName, infoToSave):
    file =  open(fileName + '.csv', 'w', newline='')
    writer = csv.writer(file)
    writer.writerows(infoToSave)
    file.close()

    df = pd.read_csv(fileName + ".csv", encoding = 'unicode_escape')
    df.to_excel(fileName + ".xlsx", sheet_name="Sheet1", index=False)


ruta =  "./Mision Colombia/"

nombresArchivos = os.listdir(ruta)

nArchivos = len(nombresArchivos)

# Datos con los titulos de cada columna
data = [['ID','Sesion', 'Nivel', 'Intento', 'Fecha', 'Tiempo', 'Evento']]
dataPreguntas = [['ID','Sesion', 'Nivel', 'Intento', 'Tipo', 'Tiempo inicio', 'Tiempo respuesta', 'Tiempo reaccion(s)', 'Respuesta']]
dataIntentos = [['ID','Sesion', 'Nivel', 'Intento','Tiempo inicio', 'Tiempo final', 'Tiempo duracion', 'Completado', 'Reglas planificacion cumplidas', '%Reglas respetadas ejecucion', 'Pasos planificados','Pasos ejecutados','Errores ejecucion','Num dormir planificado','Correctos dormir', 'Errores dormir','Num ubicacion planificado','Correctos ubicacion','Errores ubicacion', 'Paradas posibles','Paradas realizadas', 'Errores parada por tiempo excedido', 'Num errores por tiempo excedido']]

for name in nombresArchivos:

    with open(ruta + name) as archivo:
        datos_JSON = json.load(archivo)


    numEvents = len(datos_JSON[name]) # Numero de eventos del json

    # ID del paciente y numero de sesion
    inicioSesion = True
    txt = datos_JSON[name][0]["Eventos"][0]["Paciente y numero de sesion"]
    idSesion = txt.split(", ")

    idNum = idSesion[0].split()[-1]
    sesionNum = idSesion[1].split()[-1]

    level = -1
    levelPrev = -1

    txt = datos_JSON[name][0]["Tiempo"]
    date, timeStamp = getDateTime(txt)

    dataFil = [idNum, sesionNum,'', '', date, timeStamp, 'Paciente y número de sesion guardado']
    data.append(dataFil) # Anyado al final de la lista de datos

    # Voy anyadiendo siguientes filas
    for i in range(1,numEvents):

        # Fecha y Tiempo
        txt = datos_JSON[name][i]["Tiempo"]
        date, timeStamp = getDateTime(txt)

        eventName = list(datos_JSON[name][i]["Eventos"][0].keys())[0]
        eventValue = list(datos_JSON[name][i]["Eventos"][0].values())[0]
        infoEvent = MCEvent(i,eventName,eventValue, [tipoEvento, cambioNivel, level, levelPrev, tiempoSolicitudParada, tiempoSolicitudDormir, tipoPregunta, preguntaCorrecta])

        tipoEvento = infoEvent[0]
        cambioNivel = infoEvent[1]
        level = infoEvent[2]
        levelPrev = infoEvent[3]
        tiempoSolicitudParada = infoEvent[4]
        tiempoSolicitudDormir = infoEvent[5]
        tipoPregunta = infoEvent[6]
        preguntaCorrecta = infoEvent[7]
        
        if tipoEvento == 'Inicio juego':

            if cambioNivel:
                numIntento = 1
          
            else:
                numIntento += 1

            if inicioSesion:
                inicioSesion = False
                dataFilIntentoPrev = [idNum, sesionNum, level, numIntento,timeStamp]
                # Guardo previo
            else:
                tiempoDuracionIntento = calculateTime(dataFilIntentoPrev[4], timeStamp)
                dataFilIntento = [dataFilIntentoPrev[0], dataFilIntentoPrev[1], dataFilIntentoPrev[2], dataFilIntentoPrev[3],dataFilIntentoPrev[4], timeStamp, tiempoDuracionIntento, 'Completado', 'Reglas planificacion cumplidas', '%Reglas respetadas ejecucion', 'Pasos planificados','Pasos ejecutados','Errores ejecucion','Num dormir planificado','Correctos dormir', 'Errores dormir','Num ubicacion planificado','Correctos ubicacion','Errores ubicacion', 'Paradas posibles','Paradas realizadas', 'Errores parada por tiempo excedido', 'Num errores por tiempo excedido']
                dataIntentos.append(dataFilIntento)
                # Guardo actual
                dataFilIntentoPrev = [idNum, sesionNum, level, numIntento,timeStamp]
            
            # Guardo Intento
            #dataIntentos.append(dataFilIntento)

        # Guardo datos crudos de los eventos
        dataFil = [idNum, sesionNum,level, numIntento, date, timeStamp, tipoEvento]
        data.append(dataFil) # Anyado al final de la lista de datos

        if tipoPregunta != '-':
            # Si el evento es tipo ubicacion
            if tipoPregunta == 'Ubicacion':
                dataFil = [idNum, sesionNum, level, numIntento, tipoPregunta,timeStamp, '','', preguntaCorrecta]
                dataPreguntas.append(dataFil)
            else:
                # Si el evento es tipo Dormir
                if tiempoSolicitudDormir != '-':
                    tiempoReaccion = calculateTime(tiempoSolicitudDormir, timeStamp)
                    if tipoEvento != 'Tiempo excedido':
                        dataFil  = [idNum, sesionNum, level, numIntento, tipoPregunta, tiempoSolicitudDormir,timeStamp,tiempoReaccion, preguntaCorrecta]
                    else:
                        dataFil  = [idNum, sesionNum, level, numIntento, tipoPregunta, tiempoSolicitudDormir,'','Tiempo excedido', preguntaCorrecta]

                    tiempoSolicitudDormir = '-'
                    dataPreguntas.append(dataFil)

                # Si el evento es tipo Ubicacion
                elif tiempoSolicitudParada != '-':
                    tiempoReaccion = calculateTime(tiempoSolicitudParada, timeStamp)
                    if tipoEvento != 'Tiempo excedido':
                        dataFil  = [idNum, sesionNum, level, numIntento, tipoPregunta, tiempoSolicitudParada,timeStamp,tiempoReaccion, preguntaCorrecta]
                    else:
                        dataFil  = [idNum, sesionNum, level, numIntento, tipoPregunta, tiempoSolicitudParada,'','Tiempo excedido', preguntaCorrecta]

                    tiempoSolicitudParada = '-'
                    dataPreguntas.append(dataFil)      


        # Guardo datos del intento
        # tiempoDuracionIntento = calculateTime(dataFilIntento[4], timeStamp)
        # dataFilIntento = [dataFilIntento[0], dataFilIntento[1], dataFilIntento[2], dataFilIntento[3],dataFilIntento[4], timeStamp, tiempoDuracionIntento, 'Complet', 'Reg plan cumpl', '%Reglas resp ej', 'Planificados','Pejecutados','Err ej','N dormir plan','Corrct dormir', 'Err dormir','N ubi plan','Corrct ubicacion','Errores ubicacion', 'Paradas posibles','Paradas realizadas', 'Errores parada por tiempo excedido', 'Num errores por tiempo excedido']
        # dataIntentos.append(dataFilIntento)

        # Reinicio tipo pregunta y preguntacorrecta
        tipoPregunta = '-'
        preguntaCorrecta = '-'
       
# DATOS CRUDOS
saveCsvExcel('datosCrudos', data)

# # DATOS PREGUNTAS Y TIEMPO REACCION
saveCsvExcel('datosPreguntasReaccion', dataPreguntas)

# DATOS POR INTENTO
saveCsvExcel('datosIntentos', dataIntentos)