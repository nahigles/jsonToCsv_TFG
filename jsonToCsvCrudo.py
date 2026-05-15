import csv
import json
import os

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

# Errores
numErroresUbicacion = 0
numErroresUbicacionNivel = 0
numErroresUbicacionTotales = 0

numErroresDormir = 0
numErroresDormirNivel = 0
numErroresDormirTotales = 0

numErroresParada = 0
numErroresParadaNivel = 0
numErroresParadaTotales = 0

numTiempoExcedido = 0
numTiempoExcedidoNivel = 0
numTiempoExcedidoTotales = 0

numIntento = 0

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
        tipoPregunta = 'Paciente y número de sesion guardado'

    elif e == "Iniciando juego":
            cambioNivel = False
            tipoPregunta = 'Inicio juego'
            misionEmpezada = not misionEmpezada
            levelPrev = level
            level = eValue[-1]
            if (levelPrev != level):
                cambioNivel = True

    elif e == "Empieza pregunta y decision":
        tipoPregunta = 'Empieza pregunta y decision'
    elif e == "Termina pregunta y decision":
        tipoPregunta = 'Termina pregunta y decision'
    elif e == "Planificacion guardada":
        tipoPregunta = 'Planificacion guardada'

    elif e == "Hora de salda seleccionada":
        tipoPregunta = 'Hora salida seleccionada'

    elif e == "Solicitud de parada":
        tipoPregunta = 'Pregunta parada'
        tiempoSolicitudParada = timeStamp
        writeStop = False

    elif e == "Respuesta de parada SI":
         tipoPregunta = 'Respuesta parada Si'
         writeStop = True
         numParadasHechas += 1

    elif e == "Respuesta de parada NO":
         tipoPregunta = 'Respuesta parada No'
         writeStop = True
         numParadasOmitidas += 1

    elif e == "Solicitud de dormir":
        tipoPregunta = 'Pregunta dormir'
        tiempoSolicitudDormir = timeStamp
        writeSleep = False
        numPasosPlanificados += 1
        numPreguntasDormir += 1

    elif e == "Respuesta de dormir SI":
        tipoPregunta = 'Respuesta dormir Si'
        preguntaCorrecta = 'Correcto'
        writeSleep = True
        numPasosEjecutados = numPasosEjecutados + 1

    elif e == "Respuesta de dormir NO":
        tipoPregunta = 'Respuesta dormir No'
        preguntaCorrecta = 'Erroneo'
        writeSleep = True
        numErrores = numErrores + 1
        numErroresDormir += 1

    elif e == "Inicio de dormir":
        tipoPregunta = 'Empieza a dormir'
    elif e == "Ubcacion enviada":
        tipoPregunta = 'Ubicacion enviada'

    elif e == "Ubicacion bien enviada":
        tipoPregunta = 'Ubicacion bien enviada'
        preguntaCorrecta = 'Correcto'
        numPasosPlanificados += 1
        numPasosEjecutados = numPasosEjecutados + 1
        numUbicacionPlanificada += 1

    elif e == "Tiempo de respuesta excedido":
        tipoPregunta = 'Tiempo excedido'
        preguntaCorrecta = 'Erroneo'
        numErrores = numErrores + 1
        numTiempoExcedido += 1

        if tiempoSolicitudDormir != '-':
            tipoPregunta = 'Tiempo excedido por pregunta dormir'
            writeSleep = True
            numErroresDormir += 1
        elif tiempoSolicitudParada != '-':
            tipoPregunta = 'Tiempo excedido por pregunta parada'
            writeStop = True
            numErroresParada += 1

        tiempoExcedido = True

    elif e == "Se cumplen las reglas":
        reglasCumplidas = True
        tipoPregunta = 'Reglas cumplidas'

    elif e == "Se incumplen las reglas":
        reglasCumplidas = False
        tipoPregunta = 'Reglas incumplidas'
    
    elif e == "Acabado":
        tipoPregunta = 'Acabado'

    elif eValue == "Envio de ubicacion omitido":
        tipoPregunta = 'Envio ubicacion omitido'
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

nombresArchivos = os.listdir(ruta)

nArchivos = len(nombresArchivos)
print(f"Numero de archivos: {nArchivos}")

# Datos con los titulos de cada columna
data = [['ID','Sesion', 'Nivel', 'Intento', 'Fecha', 'Tiempo', 'Evento']]

for name in nombresArchivos:

    with open(ruta + name) as archivo:
        datos_JSON = json.load(archivo)


    numEvents = len(datos_JSON[name]) # Numero de eventos del json

    # ID del paciente y numero de sesion
    txt = datos_JSON[name][0]["Eventos"][0]["Paciente y numero de sesion"]
    idSesion = txt.split(", ")

    idNum = idSesion[0].split()[-1]
    sesionNum = idSesion[1].split()[-1]

    level = -1
    levelPrev = -1

    txt = datos_JSON[name][0]["Tiempo"]
    splitT = txt.split(" ")
    date = splitT[0]
    timeStamp = splitT[1]

    dataFil = [idNum, sesionNum,'', '', date, timeStamp, 'Paciente y número de sesion guardado']
    data.append(dataFil) # Anyado al final de la lista de datos

    # Reinicio por sesion
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

        
        if tipoPregunta == 'Inicio juego':
            if cambioNivel:
                numIntento = 1
            else:
                numIntento += 1

        dataFil = [idNum, sesionNum,level, numIntento, date, timeStamp, tipoPregunta]
        data.append(dataFil) # Anyado al final de la lista de datos

        tipoPregunta = '-'
       
# Abro archivo .csv para guardar los datos leidos
file =  open('../datosCrudos.csv', 'w', newline='')
writer = csv.writer(file)
writer.writerows(data)
file.close()


