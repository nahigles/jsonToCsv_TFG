import csv
import json
import os

tipoPregunta = '-'
timeStamp = ''
numIntento = 0
cambioNivel = False

def MCEvent(i, e, eValue, info): 

    tipoPregunta = info[0]
    cambioNivel = info[1]
    level = info[2]
    levelPrev = info[3]


    if e == "Paciente y numero de sesion":
        tipoPregunta = 'Paciente y número de sesion guardado'

    elif e == "Iniciando juego":
            cambioNivel = False
            tipoPregunta = 'Inicio juego'
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

    elif e == "Respuesta de parada SI":
         tipoPregunta = 'Respuesta parada Si'

    elif e == "Respuesta de parada NO":
         tipoPregunta = 'Respuesta parada No'

    elif e == "Solicitud de dormir":
        tipoPregunta = 'Pregunta dormir'

    elif e == "Respuesta de dormir SI":
        tipoPregunta = 'Respuesta dormir Si'

    elif e == "Respuesta de dormir NO":
        tipoPregunta = 'Respuesta dormir No'

    elif e == "Inicio de dormir":
        tipoPregunta = 'Empieza a dormir'
    elif e == "Ubcacion enviada":
        tipoPregunta = 'Ubicacion enviada'

    elif e == "Ubicacion bien enviada":
        tipoPregunta = 'Ubicacion bien enviada'

    elif e == "Tiempo de respuesta excedido":
        tipoPregunta = 'Tiempo excedido'

    elif e == "Se cumplen las reglas":
        tipoPregunta = 'Reglas cumplidas'

    elif e == "Se incumplen las reglas":
        tipoPregunta = 'Reglas incumplidas'
    
    elif e == "Acabado":
        tipoPregunta = 'Acabado'

    elif eValue == "Envio de ubicacion omitido":
        tipoPregunta = 'Envio ubicacion omitido'
    

    return tipoPregunta, cambioNivel, level, levelPrev


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
    timeStamp = ''   
    cambioNivel = False

    # Voy anyadiendo siguientes filas
    for i in range(1,numEvents):

        # Fecha y Tiempo
        txt = datos_JSON[name][i]["Tiempo"]
        splitT = txt.split(" ")
        date = splitT[0]
        timeStamp = splitT[1]

        eventName = list(datos_JSON[name][i]["Eventos"][0].keys())[0]
        eventValue = list(datos_JSON[name][i]["Eventos"][0].values())[0]
        infoEvent = MCEvent(i,eventName,eventValue, [tipoPregunta, cambioNivel, level, levelPrev])

        tipoPregunta = infoEvent[0]
        cambioNivel = infoEvent[1]
        level = infoEvent[2]
        levelPrev = infoEvent[3]
        
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


