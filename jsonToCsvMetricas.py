import csv
import json
import os
import pandas as pd
import numpy as np
from scipy.stats import pearsonr


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
reglasPlanificacionCumplidas = False
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

# Datos por nivel
completadoNivel = False
numPasosPlanificadosNivel = 0
numPasosEjecutadosNivel = 0
numErroresEjecucionNivel = 0
numDormirPlanificadoNivel = 0
correctosDormirNivel = 0
erroresDormirNivel = 0
numUbicacionPlanificadoNivel = 0
correctosUbicacionNivel = 0
erroresUbicacionNivel = 0
paradasPosiblesNivel = 0
paradasRealizadasNivel = 0
erroresParadaTiempoExcedidoNivel = 0
erroresTiempoExcedidoNivel = 0

# Datos por sesion
numPasosPlanificadosSesion = 0
numPasosEjecutadosSesion = 0
numErroresEjecucionSesion = 0
numDormirPlanificadoSesion = 0
correctosDormirSesion = 0
erroresDormirSesion = 0
numUbicacionPlanificadoSesion = 0
correctosUbicacionSesion = 0
erroresUbicacionSesion = 0
paradasPosiblesSesion = 0
paradasRealizadasSesion = 0
erroresParadaTiempoExcedidoSesion = 0
erroresTiempoExcedidoSesion = 0
numIntentosTotales = 0
numNivelesTotales = 0
numNivelesCompletados = 0

def MCEvent(i, e, eValue, info): 

    tipoEvento = info[0]
    cambioNivel = info[1]
    level = info[2]
    levelPrev = info[3]
    tiempoSolicitudParada = info[4]
    tiempoSolicitudDormir = info[5]
    tipoPregunta = info[6]
    preguntaCorrecta = info[7]

    # Variables globales
    global numDormirPlanificado
    global correctosDormir
    global erroresDormir
    global numUbicacionPlanificado
    global correctosUbicacion
    global erroresUbicacion
    global paradasPosibles
    global paradasRealizadas
    global erroresParadaTiempoExcedido
    global erroresTiempoExcedido
    global reglasPlanificacionCumplidas

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
        paradasPosibles += 1

    elif e == "Respuesta de parada SI":
        tipoEvento = 'Respuesta parada Si'
        tipoPregunta = 'Parada'
        paradasRealizadas += 1

    elif e == "Respuesta de parada NO":
        tipoEvento = 'Respuesta parada No'
        tipoPregunta = 'Parada'

    elif e == "Solicitud de dormir":
        tipoEvento = 'Pregunta dormir'
        tiempoSolicitudDormir = timeStamp
        numDormirPlanificado += 1

    elif e == "Respuesta de dormir SI":
        tipoEvento = 'Respuesta dormir Si'
        tipoPregunta = 'Dormir'
        preguntaCorrecta = 'Correcto'
        correctosDormir += 1

    elif e == "Respuesta de dormir NO":
        tipoEvento = 'Respuesta dormir No'
        tipoPregunta = 'Dormir'
        preguntaCorrecta = 'Erroneo'
        #erroresDormir += 1

    elif e == "Inicio de dormir":
        tipoEvento = 'Empieza a dormir'
    elif e == "Ubcacion enviada":
        tipoEvento = 'Ubicacion enviada'

    elif e == "Ubicacion bien enviada":
        tipoEvento = 'Ubicacion bien enviada'
        tipoPregunta = 'Ubicacion'
        preguntaCorrecta = 'Correcto'
        correctosUbicacion += 1

    elif e == "Tiempo de respuesta excedido":
        tipoEvento = 'Tiempo excedido'
        preguntaCorrecta = 'Erroneo'
        erroresTiempoExcedido += 1
        if tiempoSolicitudDormir != '-':
            tipoPregunta = 'Dormir'
            #erroresDormir += 1
        elif tiempoSolicitudParada != '-':
            tipoPregunta = 'Parada'
            erroresParadaTiempoExcedido += 1
        

    elif e == "Se cumplen las reglas":
        tipoEvento = 'Reglas cumplidas'
        reglasPlanificacionCumplidas = True

    elif e == "Se incumplen las reglas":
        tipoEvento = 'Reglas incumplidas'
        reglasPlanificacionCumplidas = False
    
    elif e == "Acabado":
        tipoEvento = 'Acabado'

    elif eValue == "Envio de ubicacion omitido":
        tipoEvento = 'Envio ubicacion omitido'
        tipoPregunta = 'Ubicacion'
        preguntaCorrecta = 'Erroneo'
        erroresUbicacion += 1
    

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

def cleanDataSesion(df):
    df = df.drop(columns=["Tiempo inicio", "Tiempo final"])
    return df

def cleanDataNivel(df):
    df = cleanDataSesion(df)
    df = df.drop(columns=["Completado"])
    return df

def cleanDataIntento(df):
    df = cleanDataNivel(df)
    df = df.drop(columns=["Reglas planificacion cumplidas"])
    return df

def cleanDataTiempoReacciones(df):
    df = df.drop(columns=["Tipo","Tiempo inicio", "Tiempo respuesta", "Respuesta"])
    df = df.dropna(axis = 0)
    df = df[df['Tiempo reaccion(s)'] != 'Tiempo excedido']
    return df

def calcular_p_valores(df):      
    # 1. Nos aseguramos de quedarnos solo con columnas numéricas para evitar errores
    df_numerico = df.select_dtypes(include=[np.number])
    columnas = df_numerico.columns
    m = len(columnas)
    
    # 2. Inicializamos la matriz de p-valores
    p_valores = np.zeros((m, m))
    cor_valores = np.zeros((m, m))
    
    # 3. Doble bucle para calcular el p-valor entre cada par de variables
    for i in range(m):
        for j in range(m):
            if i == j:
                # La correlación de una variable consigo misma siempre es 1 (p-valor = 0)
                p_valores[i, j] = 0.0
                cor_valores[i, j] = 1.0
            else:
                # Calculamos pearsonr. Es importante que no haya valores nulos (NaN)
                # .dropna() elimina filas con NaN en esa pareja para evitar que devuelva NaN
                df_limpio = df_numerico[[columnas[i], columnas[j]]].dropna()
                
                if len(df_limpio) > 1:  # Se necesitan al menos 2 puntos para calcular la correlación
                    cor_val, p_val = pearsonr(df_limpio[columnas[i]], df_limpio[columnas[j]])
                    p_valores[i, j] = p_val
                    cor_valores[i, j] = cor_val
                else:
                    p_valores[i, j] = np.nan
                    cor_valores[i, j] = np.nan

    return pd.DataFrame(cor_valores, columns=columnas, index=columnas), pd.DataFrame(p_valores, columns=columnas, index=columnas)

def corr(fileName, type):
    df = pd.read_excel('{0}.xlsx'.format(fileName))
    df = df.drop(columns=["ID"])
    if type == 1:
        df = cleanDataTiempoReacciones(df)
    elif type == 2:
        df = cleanDataIntento(df)
    elif type == 3:
        df = cleanDataNivel(df)
    elif type == 4:
        df = cleanDataSesion(df)

    # Obtener la matriz de p-values y correlacion
    matriz_cor_valores, matriz_p_valores = calcular_p_valores(df)
    print(matriz_p_valores)
    matriz_p_valores.to_excel(str(type) + "pvalues.xlsx")
    matriz_cor_valores.to_excel(str(type) + "corvalues.xlsx")

    # df.to_excel(str(type) + "output.xlsx")
    #print(df.corr())




ruta =  "./Mision Colombia/"

nombresArchivos = os.listdir(ruta)

nArchivos = len(nombresArchivos)

# Datos con los titulos de cada columna
data = [['ID','Sesion', 'Nivel', 'Intento', 'Fecha', 'Tiempo', 'Evento']]
dataPreguntas = [['ID','Sesion', 'Nivel', 'Intento', 'Tipo', 'Tiempo inicio', 'Tiempo respuesta', 'Tiempo reaccion(s)', 'Respuesta']]
dataIntentos = [['ID','Sesion', 'Nivel', 'Intento','Tiempo inicio', 'Tiempo final', 'Tiempo duracion', 'Completado', 'Reglas planificacion cumplidas', '%Reglas respetadas ejecucion', 'Pasos planificados','Pasos ejecutados','Errores ejecucion','Num dormir planificado','Correctos dormir', 'Errores dormir','Num ubicacion planificado','Correctos ubicacion','Errores ubicacion', 'Paradas posibles','Paradas realizadas', 'Errores parada por tiempo excedido', 'Num errores por tiempo excedido']]
dataNiveles = [['ID','Sesion', 'Nivel', 'Num intentos','Tiempo inicio', 'Tiempo final', 'Tiempo duracion', 'Completado', 'Pasos planificados','Pasos ejecutados','Errores ejecucion','Num dormir planificado','Correctos dormir', 'Errores dormir','Num ubicacion planificado','Correctos ubicacion','Errores ubicacion', 'Paradas posibles','Paradas realizadas', 'Errores parada por tiempo excedido', 'Num errores por tiempo excedido']]
dataSesiones = [['ID','Sesion', 'Num niveles', 'Num intentos', 'Completados','Tiempo inicio', 'Tiempo final', 'Tiempo duracion', 'Pasos planificados','Pasos ejecutados','Errores ejecucion','Num dormir planificado','Correctos dormir', 'Errores dormir','Num ubicacion planificado','Correctos ubicacion','Errores ubicacion', 'Paradas posibles','Paradas realizadas', 'Errores parada por tiempo excedido', 'Num errores por tiempo excedido']]

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
    tiempoInicioSesion = timeStamp

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
        
        if tipoEvento == 'Inicio juego' or i == (numEvents - 1):

            if i != (numEvents - 1):
                if cambioNivel:
                    numIntento = 1
            
                else:
                    numIntento += 1

            if inicioSesion:
                inicioSesion = False
                # Guardo previo
                dataFilIntentoPrev = [idNum, sesionNum, level, numIntento,timeStamp]
                tiempoIniNivel = timeStamp
            else:

                # INTENTOS
                # Calculos intento
                numUbicacionPlanificado = correctosUbicacion + erroresUbicacion
                tiempoDuracionIntento = calculateTime(dataFilIntentoPrev[4], timeStamp)
                numPasosPlanificados = numDormirPlanificado + numUbicacionPlanificado
                numPasosEjecutados = correctosDormir + correctosUbicacion
                erroresDormir = numDormirPlanificado - correctosDormir
                numErroresEjecucion = erroresDormir + erroresUbicacion

                # Calculos nivel
                numPasosPlanificadosNivel += numPasosPlanificados
                numPasosEjecutadosNivel += numPasosEjecutados
                numErroresEjecucionNivel += numErroresEjecucion
                numDormirPlanificadoNivel += numDormirPlanificado
                correctosDormirNivel += correctosDormir
                erroresDormirNivel += erroresDormir
                numUbicacionPlanificadoNivel += numUbicacionPlanificado
                correctosUbicacionNivel += correctosUbicacion
                erroresUbicacionNivel += erroresUbicacion
                paradasPosiblesNivel += paradasPosibles
                paradasRealizadasNivel += paradasRealizadas
                erroresParadaTiempoExcedidoNivel += erroresParadaTiempoExcedido
                erroresTiempoExcedidoNivel += erroresTiempoExcedido

                # Porcentaje de reglas cumplidas
                porcentajeReglasCumplidasEjecucion = 100

                if erroresDormir > 0:
                    porcentajeReglasCumplidasEjecucion -= 25
                if erroresParadaTiempoExcedido  > 0:
                    porcentajeReglasCumplidasEjecucion -= 25
                if erroresUbicacion  > 0:
                    porcentajeReglasCumplidasEjecucion -= 25


                completado = porcentajeReglasCumplidasEjecucion == 100 and reglasPlanificacionCumplidas
                completadoNivel = completado or completadoNivel
            
                if completado:
                    numNivelesCompletados += 1

                # NIVELES
                if cambioNivel or i == (numEvents - 1):

                    # Guardo nivel
                    duracionNivel = calculateTime(tiempoIniNivel, timeStamp)
                    dataFilNivel = [dataFilIntentoPrev[0], dataFilIntentoPrev[1], dataFilIntentoPrev[2], dataFilIntentoPrev[3],tiempoIniNivel, timeStamp, duracionNivel, completadoNivel, numPasosPlanificadosNivel, numPasosEjecutadosNivel, numErroresEjecucionNivel, numDormirPlanificadoNivel, correctosDormirNivel, erroresDormirNivel, numUbicacionPlanificadoNivel, correctosUbicacionNivel, erroresUbicacionNivel, paradasPosiblesNivel, paradasRealizadasNivel, erroresParadaTiempoExcedidoNivel, erroresTiempoExcedidoNivel]
                    dataNiveles.append(dataFilNivel)
                    tiempoIniNivel = timeStamp

                    # Acumuladores por sesion
                    numIntentosTotales += dataFilIntentoPrev[3]
                    numNivelesTotales += 1
                    numPasosPlanificadosSesion += numPasosPlanificadosNivel
                    numPasosEjecutadosSesion += numPasosEjecutadosNivel
                    numErroresEjecucionSesion += numErroresEjecucionNivel
                    numDormirPlanificadoSesion += numDormirPlanificadoNivel
                    correctosDormirSesion += correctosDormirNivel
                    erroresDormirSesion += erroresDormirNivel
                    numUbicacionPlanificadoSesion += numUbicacionPlanificadoNivel
                    correctosUbicacionSesion += correctosUbicacionNivel
                    erroresUbicacionSesion += erroresUbicacionNivel
                    paradasPosiblesSesion += paradasPosiblesNivel
                    paradasRealizadasSesion += paradasRealizadasNivel
                    erroresParadaTiempoExcedidoSesion += erroresParadaTiempoExcedidoNivel
                    erroresTiempoExcedidoSesion += erroresTiempoExcedidoNivel

                    # Restablezco contadores
                    completadoNivel = False

                    numPasosPlanificadosNivel = 0
                    numPasosEjecutadosNivel = 0
                    numErroresEjecucionNivel = 0
                    numDormirPlanificadoNivel = 0
                    correctosDormirNivel = 0
                    erroresDormirNivel = 0
                    numUbicacionPlanificadoNivel = 0
                    correctosUbicacionNivel = 0
                    erroresUbicacionNivel = 0
                    paradasPosiblesNivel = 0
                    paradasRealizadasNivel = 0
                    erroresParadaTiempoExcedidoNivel = 0
                    erroresTiempoExcedidoNivel = 0

                # INTENTOS
                # Guardo intento
                dataFilIntento = [dataFilIntentoPrev[0], dataFilIntentoPrev[1], dataFilIntentoPrev[2], dataFilIntentoPrev[3],dataFilIntentoPrev[4], timeStamp, tiempoDuracionIntento, completado, reglasPlanificacionCumplidas, porcentajeReglasCumplidasEjecucion, numPasosPlanificados, numPasosEjecutados, numErroresEjecucion, numDormirPlanificado, correctosDormir, erroresDormir,numUbicacionPlanificado,correctosUbicacion, erroresUbicacion, paradasPosibles, paradasRealizadas, erroresParadaTiempoExcedido, erroresTiempoExcedido]
                dataIntentos.append(dataFilIntento)

                # Guardo actual
                dataFilIntentoPrev = [idNum, sesionNum, level, numIntento,timeStamp]

                # Restablezco contadores por intento
                numDormirPlanificado = 0
                correctosDormir = 0
                erroresUbicacion = 0
                correctosUbicacion = 0
                paradasRealizadas = 0
                paradasPosibles = 0
                erroresParadaTiempoExcedido = 0
                erroresTiempoExcedido = 0
            

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


        # Reinicio tipo pregunta y preguntacorrecta
        tipoPregunta = '-'
        preguntaCorrecta = '-'

    # Guardo datos sesion
    duracionSesion = calculateTime(tiempoInicioSesion, timeStamp)
    dataFilSesion = [idNum, sesionNum, numNivelesTotales, numIntentosTotales, numNivelesCompletados, tiempoInicioSesion, timeStamp, duracionSesion, numPasosPlanificadosSesion, numPasosEjecutadosSesion, numErroresEjecucionSesion, numDormirPlanificadoSesion, correctosDormirSesion, erroresDormirSesion, numUbicacionPlanificadoSesion, correctosUbicacionSesion, erroresUbicacionSesion, paradasPosiblesSesion, paradasRealizadasSesion, erroresParadaTiempoExcedidoSesion, erroresTiempoExcedidoSesion]
    dataSesiones.append(dataFilSesion) 

    numPasosPlanificadosSesion = 0
    numPasosEjecutadosSesion = 0
    numErroresEjecucionSesion = 0
    numDormirPlanificadoSesion = 0
    correctosDormirSesion = 0
    erroresDormirSesion = 0
    numUbicacionPlanificadoSesion = 0
    correctosUbicacionSesion = 0
    erroresUbicacionSesion = 0
    paradasPosiblesSesion = 0
    paradasRealizadasSesion = 0
    erroresParadaTiempoExcedidoSesion = 0
    erroresTiempoExcedidoSesion = 0
    numIntentosTotales = 0
    numNivelesTotales = 0
    numNivelesCompletados = 0
       

# Escribo datos finales
writeDatas = False
writeCorrelacion = True

# DATOS CRUDOS 0
if writeDatas:
    saveCsvExcel('datosCrudos', data)

# DATOS PREGUNTAS Y TIEMPO REACCION 1
if writeDatas:
    saveCsvExcel('datosPreguntasReaccion', dataPreguntas)
if writeCorrelacion:
    corr('datosPreguntasReaccion',1)

# DATOS POR INTENTO 2
if writeDatas:
    saveCsvExcel('datosIntentos', dataIntentos)
if writeCorrelacion:
    corr('datosIntentos',2)

# DATOS POR NIVEL 3
if writeDatas:
    saveCsvExcel('datosNiveles', dataNiveles)
if writeCorrelacion:
    corr('datosNiveles', 3)

# DATOS POR SESION 4
if writeDatas:
    saveCsvExcel('datosSesiones', dataSesiones)
if writeCorrelacion:
    corr('datosSesiones', 4)