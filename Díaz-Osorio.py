# Importación de paquetes a utilizar...
import telebot          # Conecta con  la API de Telegram
from telebot import types                                                                                                                                                                                                                                                                                                                                                                   # SAMUEL SANTIAGO BOZA CASTRO
import re               # Manejo de Regex (Regular)                                                                                                                                                                                                                                                                                                                                             # MANUEL ALBERTO OSORIO LÓPEZ
import numpy as np          # Manejo de matrices                                                                                                                                                                                                                                                                                                                                            # ÁNDRES ENRIQUE DÍAZ SOTO
import pandas as pd         # Manejo de datos, creación de archivos excel, entre otros
import matplotlib.pyplot as plt         # Creación de plots

# Extraer datos
df = pd.read_excel('TEGII.xlsx')
datos_user = []
metodo = []
valor_conocido = []
valor_prueba = []
acento ='áéíóú'
sin_acento = 'aeiou'
variables = {}

# Funcion iteracion convergencia 1
def iteracion(t, psat1, psat2, y1, y2, message):
    traduccion = message.text.maketrans(acento, sin_acento)
    euler = 2.718281828
    gamma1 = 1.00
    gamma2 = 1.00
    a = 2.771 - (0.00523 * (t + 273.15))
    gammas = [gamma1, gamma2]
    xs = [10000, 5000]
    p1 = [0]
    while max(xs) - min(xs) > 0.000001:
        p1.pop(0)
        p = 1 / ((y1/ (gammas[0]*psat1)) + (y2/ (gammas[1]*psat2)))
        x1 = (y1 * p) / (gammas[0] * psat1)
        x2 = 1 - x1
        xs.pop(0)
        xs.append(x1)
        gammas[0] = euler ** (a * (x2 ** 2))
        gammas[1] = euler ** (a * (x1 ** 2))
        p1.append(p)
    return [xs[-1], 1 - xs[-1], p1[0], gammas[0], gammas[1]]

# Funcion iteracion convergencia 2 
def iteracion2(t, presion, x1, x2, elemento1, elemento2, message):
    traduccion = message.text.maketrans(acento, sin_acento)
    temp = [1, t]
    coef = [0, 0]
    p = [0, 0]
    euler = 2.718281828
    while max(temp) - min(temp) > 0.00000001:
        p1 = euler ** (df[df['Nombre'].str.lower().str.translate(traduccion) == elemento1.lower()]['A'].item() - df[df['Nombre'].str.lower().str.translate(traduccion) == elemento1.lower()]['B'].item() / (temp[-1] + df[df['Nombre'].str.lower() == elemento1.lower()]['C'].item()))
        p2 = euler ** (df[df['Nombre'].str.lower().str.translate(traduccion) == elemento2.lower()]['A'].item() - df[df['Nombre'].str.lower().str.translate(traduccion) == elemento2.lower()]['B'].item() / (temp[-1] + df[df['Nombre'].str.lower().str.translate(traduccion) == elemento2.lower()]['C'].item()))
        alfa = p1 / p2
        a = 2.771 - (0.00523 * temp[-1])
        coef1 = euler ** (a * (x2 ** 2))
        coef2 = euler ** (a * (x1 ** 2))
        psat1 = presion / ((x1 * coef1) + ((x2 * coef2) / alfa))
        coef[0] = coef1
        coef[1] = coef2
        p[0] = psat1
        p[1] = p2
        temp.pop(0)
        temp.append((df[df['Nombre'].str.lower().str.translate(traduccion) == elemento1.lower()]['B'].item()/(df[df['Nombre'].str.lower() == elemento1.lower()]['A'].item()) - np.log(psat1)) - df[df['Nombre'].str.lower() == elemento1.lower()]['C'].item())
    return coef[0], coef[1], p[0], p[1], temp[-1]

# Funcion iteracion convergencia 3
def iteracion3(t, presion, y1, y2, elemento1, elemento2, message):
    traduccion = message.text.maketrans(acento, sin_acento)
    temp = [0, t]
    xs = [0,0]
    coef = [1, 1]
    euler = 2.718281828
    while max(temp) - min(temp) > 0.000000001:
        p1 = euler ** (df[df['Nombre'].str.lower().str.translate(traduccion) == elemento1.lower()]['A'].item() - df[df['Nombre'].str.lower().str.translate(traduccion) == elemento1.lower()]['B'].item() / (temp[-1] + df[df['Nombre'].str.lower().str.translate(traduccion) == elemento1.lower()]['C'].item()))
        p2 = euler ** (df[df['Nombre'].str.lower().str.translate(traduccion) == elemento2.lower()]['A'].item() - df[df['Nombre'].str.lower().str.translate(traduccion) == elemento2.lower()]['B'].item() / (temp[-1] + df[df['Nombre'].str.lower().str.translate(traduccion) == elemento2.lower()]['C'].item()))
        alfa = p1 / p2 
        a = 2.771 - (0.00523 * temp[-1])
        x1 = (y1 * presion) / (coef[0] * p1)
        x2 = 1 - x1
        coef1 = euler ** (a * (x2 ** 2))
        coef2 = euler ** (a * (x1 ** 2))
        coef[0] = coef1
        coef[1] = coef2
        psat1 = presion * ((y1 / coef1) + ((y2 * alfa) / coef2))
        xs[0] = x1
        xs[1] = x2
        temp.pop(0)
        temp.append((df[df['Nombre'].str.lower().str.translate(traduccion) == elemento1.lower()]['B'].item() / (df[df['Nombre'].str.lower().str.translate(traduccion) == elemento1.lower()]['A'].item() - np.log(psat1))) - df[df['Nombre'].str.lower().str.translate(traduccion)== elemento1.lower()]['C'].item())
    return xs[0], xs[1], coef[0], coef[1]

# Interaccion usuario
tb = telebot.TeleBot("1797995641:AAGvlpiGtmmIDbaJepeU968zONIqmWMtj5Q")
@tb.message_handler(commands = ['start', 'nuevocalculo'])
def dar_bienvendia(message):
    metodo.clear()
    datos_user.clear()    
    variables.clear()
    valor_conocido.clear()
    valor_prueba.clear()
    if message.text == '/start':
        tb.send_message(message.chat.id, 'Bienvenido al Bot de Cálculo de K')
        tb.send_message(message.chat.id, 'Para conocer los elementos disponibles, utilice el comando /elementosdisponibles')
    else:
        pass
    tb.send_message(message.chat.id, 'Por favor, introduzca el elemento 1:', reply_markup = types.ForceReply(selective = False))
    
@tb.message_handler(commands = ['elementosdisponibles'])
def lista_elemnetos(message):
    elementos = [x for x in df['Nombre']]
    texto = []
    for x in elementos:
        texto.append(f'-{x.title()}\n')
    tb.send_message(message.chat.id, f'{"".join(texto)}')
    tb.send_message(message.chat.id, 'Para realizar un cálculo, utilice el comando /nuevocalculo', reply_markup = types.ReplyKeyboardRemove(selective = False))

@tb.message_handler(func = lambda message: message.reply_to_message)
def pedir_x(message):
    traduccion = message.text.maketrans(acento, sin_acento)
    if message.reply_to_message.text == 'Por favor, introduzca el elemento 1:':
        if message.text.lower().translate(traduccion) in [x for x in df['Nombre'].str.lower().str.translate(traduccion)]:    
            tb.send_message(message.chat.id, 'Introduzca elemento 2:', reply_markup = types.ForceReply(selective = False))
            datos_user.append(message.text.lower().translate(traduccion))
        else:
            tb.send_message(message.chat.id, 'Elemento no encontrado, por favor intente de nuevo!')
            tb.send_message(message.chat.id, 'Por favor, introduzca el elemento 1:', reply_markup = types.ForceReply(selective = False))
    elif message.reply_to_message.text == 'Introduzca elemento 2:':
        if message.text.lower().translate(traduccion) in [x for x in df['Nombre'].str.lower().str.translate(traduccion)]:
            datos_user.append(message.text.lower().translate(traduccion))
            markup = types.ReplyKeyboardMarkup(row_width=1)
            itembtn1 = types.KeyboardButton('Ley de Raoult Modificada')
            itembtn2 = types.KeyboardButton('Correlación de Wilson')
            markup.add(itembtn1, itembtn2)
            tb.send_message(message.chat.id, "Que metodo desea usar?", reply_markup=markup)
        else:
            tb.send_message(message.chat.id, 'Elemento no encontrado, por favor intente de nuevo!')
            tb.send_message(message.chat.id, 'Introduzca elemento 2:', reply_markup = types.ForceReply(selective = False))
    elif message.reply_to_message.text == 'Introduzca Temperatura en grados Celsius (Valor Numerico):':
        datos_user.append(float(message.text))
        if valor_prueba[0] == 'Fracción Líquida (Elemento 1)':
            tb.send_message(message.chat.id, 'Introduzca Fracción Líquida (Elemento 1):', reply_markup = types.ForceReply(selective = False))
        elif valor_prueba[0] == 'Fracción de Vapor (Elemento 1)':
            tb.send_message(message.chat.id, 'Introduzca Fracción de Vapor (Elemento 1):', reply_markup = types.ForceReply(selective = False))
    elif message.reply_to_message.text == 'Introduzca Presión en Kpa (Valor Numerico):':
        datos_user.append(float(message.text))
        if valor_prueba[0] == 'Fracción Líquida (Elemento 1)':
            tb.send_message(message.chat.id, 'Introduzca Fracción Líquida (Elemento 1):', reply_markup = types.ForceReply(selective = False))
        elif valor_prueba[0] == 'Fracción de Vapor (Elemento 1)':
            tb.send_message(message.chat.id, 'Introduzca Fracción de Vapor (Elemento 1):', reply_markup = types.ForceReply(selective = False))
    elif message.reply_to_message.text == 'Introduzca Fracción Líquida (Elemento 1):':
        if float(message.text) > 1 or float(message.text) < 0:
            tb.send_message(message.chat.id, 'Por favor, introduzca un valor válido (Entre 0 y 1)')
            tb.send_message(message.chat.id, 'Introduzca Fracción Líquida (Elemento 1):', reply_markup = types.ForceReply(selective = False))
        else:
            if valor_conocido[0] == 'Temperatura':
                # Ley de Raoult A
                datos_user.append(float(message.text))
                euler = 2.718281828
                temp = datos_user[2] + 273.15
                elemento1 = datos_user[0]
                elemento2 = datos_user[1]
                x1 = datos_user[3]
                x2 = 1 - x1
                df.fillna(1)
                df['C'] = df['C'].apply(lambda x: x - 273.15)
                datos = pd.DataFrame(columns=['P1', 'P2', 'COEF1', 'COEF2'])
                p1 = euler ** (df[df['Nombre'].str.lower().str.translate(traduccion) == elemento1.lower()]['A'].item() - df[df['Nombre'].str.lower().str.translate(traduccion) == elemento1.lower()]['B'].item() / (temp + df[df['Nombre'].str.lower().str.translate(traduccion) == elemento1.lower()]['C'].item()))
                datos['P1'] = [p1]
                datos.index = [temp]
                p2 = euler ** (df[df['Nombre'].str.lower().str.translate(traduccion) == elemento2.lower()]['A'].item() - df[df['Nombre'].str.lower().str.translate(traduccion) == elemento2.lower()]['B'].item() / (temp + df[df['Nombre'].str.lower().str.translate(traduccion) == elemento2.lower()]['C'].item()))
                datos['P2'] = p2
                a = 2.771 - (0.00523 * temp)
                coef1 = euler ** (a * (x2 ** 2))
                datos['COEF1'] = coef1
                coef2 = euler ** (a * (x1 ** 2))
                datos['COEF2'] = coef2
                p = (x1 * coef1 * p1) + (x2 * coef2 * p2) 
                y1 = (x1 * coef1 * p1) / p
                y2 = (x2 * coef2 * p2) / p
                datos['Y1'] = y1 
                datos['Y2'] = y2
                k1 = y1 / x1
                k2 = y2 / x2
                tb.send_message(message.chat.id, f'Valor K de {elemento1}: {k1}')
                tb.send_message(message.chat.id, f'Valor K de {elemento2}: {k2}')
                variables.update({'P1':p1, 'P2':p2, 'A':a, 'GAMMA 1':coef1, 'GAMMA 2':coef2, 'P':p, 'Y1':y1, 'Y2':y2})
                markup = types.ReplyKeyboardMarkup(row_width=1)
                itembtn1 = types.KeyboardButton('Sí')
                itembtn2 = types.KeyboardButton('No')
                markup.add(itembtn1, itembtn2)
                tb.send_message(message.chat.id, 'Desea algún otro valor del cálculo?', reply_markup=markup)
            elif valor_conocido[0] == 'Presión':
                #Ley de Raoult C
                datos_user.append(float(message.text))
                euler = 2.718281828
                presion = datos_user[2]
                elemento1 = datos_user[0]
                elemento2 = datos_user[1]
                x1 = datos_user[3]
                x2 = 1 - x1
                df.fillna(1)
                df['C'] = df['C'].apply(lambda x: x - 273.15)
                t1 = (df[df['Nombre'].str.lower().str.translate(traduccion) == elemento1.lower()]['B'].item() / (df[df['Nombre'].str.lower().str.translate(traduccion) == elemento1.lower()]['A'].item() - np.log(presion))) - df[df['Nombre'].str.lower().str.translate(traduccion) == elemento1.lower()]['C'].item()
                t2 = (df[df['Nombre'].str.lower().str.translate(traduccion) == elemento2.lower()]['B'].item() / (df[df['Nombre'].str.lower().str.translate(traduccion) == elemento2.lower()]['A'].item() - np.log(presion))) - df[df['Nombre'].str.lower().str.translate(traduccion) == elemento2.lower()]['C'].item()
                t = (x1 * t1) + (x2 * t2)
                coef1, coef2, psat1, p2, temp = iteracion2(t, presion, x1, x2, elemento1, elemento2, message)
                y1 = (x1 * coef1 * psat1) / presion
                y2 = 1 - y1
                k1 = y1 / x1
                k2 = y2 / x2
                tb.send_message(message.chat.id, f'Valor K de {elemento1}: {k1}')
                tb.send_message(message.chat.id, f'Valor K de {elemento2}: {k2}')
                variables.update({'T1':t1, 'T2':t2, 'GAMMA 1':coef1, 'GAMMA 2':coef2, 'Y1':y1, 'Y2':y2, 'T': temp})
                markup = types.ReplyKeyboardMarkup(row_width=1)
                itembtn1 = types.KeyboardButton('Sí')
                itembtn2 = types.KeyboardButton('No')
                markup.add(itembtn1, itembtn2)
                tb.send_message(message.chat.id, 'Desea algún otro valor del cálculo?', reply_markup=markup)
    elif message.reply_to_message.text == 'Introduzca Fracción de Vapor (Elemento 1):':
        if float(message.text) > 1 or float(message.text) < 0:
            tb.send_message(message.chat.id, 'Por favor, introduzca un valor válido (Entre 0 y 1)')
            tb.send_message(message.chat.id, 'Introduzca Fracción de Vapor (Elemento 1):', reply_markup = types.ForceReply(selective = False))
        else:
            if valor_conocido[0] == 'Temperatura':
                # Ley de Raoult B
                datos_user.append(float(message.text))
                euler = 2.718281828
                temp = datos_user[2] + 273.15
                elemento1 = datos_user[0]
                elemento2 = datos_user[1]
                y1 = datos_user[3]
                y2 = 1 - y1
                df.fillna(1) #Borrar
                df['C'] = df['C'].apply(lambda x: x - 273.15)
                datos = pd.DataFrame(columns=['P1', 'P2', 'COEF1', 'COEF2'])
                p1 = euler ** (df[df['Nombre'].str.lower().str.translate(traduccion) == elemento1.lower()]['A'].item() - df[df['Nombre'].str.lower().str.translate(traduccion) == elemento1.lower()]['B'].item() / (temp + df[df['Nombre'].str.lower().str.translate(traduccion) == elemento1.lower()]['C'].item()))
                datos['P1'] = [p1]
                datos.index = [temp]
                p2 = euler ** (df[df['Nombre'].str.lower().str.translate(traduccion) == elemento2.lower()]['A'].item() - df[df['Nombre'].str.lower().str.translate(traduccion) == elemento2.lower()]['B'].item() / (temp + df[df['Nombre'].str.lower().str.translate(traduccion) == elemento2.lower()]['C'].item()))
                datos['P2'] = p2
                a = 2.771 - (0.00523 * temp)
                x1, x2, p, coef1, coef2 = iteracion(temp, p1, p2, y1, y2, message)
                datos['X1'] = x1 
                datos['X2'] = x2
                k1 = y1 / x1
                k2 = y2 / x2
                tb.send_message(message.chat.id, f'Valor K de {elemento1}: {k1}')
                tb.send_message(message.chat.id, f'Valor K de {elemento2}: {k2}')
                variables.update({'P1':p1, 'P2':p2, 'A':a, 'GAMMA 1':coef1, 'GAMMA 2':coef2, 'X1':x1, 'X2':x2, 'P': p})
                markup = types.ReplyKeyboardMarkup(row_width=1)
                itembtn1 = types.KeyboardButton('Sí')
                itembtn2 = types.KeyboardButton('No')
                markup.add(itembtn1, itembtn2)
                tb.send_message(message.chat.id, 'Desea algún otro valor del cálculo?', reply_markup=markup)
            elif valor_conocido[0] == 'Presión':
                # Ley de Raoult D
                datos_user.append(float(message.text))
                presion = datos_user[2]
                elemento1 = datos_user[0]
                elemento2 = datos_user[1]
                y1 = datos_user[3]
                y2 = 1 - y1
                df.fillna(1)
                df['C'] = df['C'].apply(lambda x: x - 273.15)
                t1 = (df[df['Nombre'].str.lower().str.translate(traduccion) == elemento1.lower()]['B'].item() / (df[df['Nombre'].str.lower().str.translate(traduccion) == elemento1.lower()]['A'].item() - np.log(presion))) - df[df['Nombre'].str.lower().str.translate(traduccion) == elemento1.lower()]['C'].item()
                t2 = (df[df['Nombre'].str.lower().str.translate(traduccion) == elemento2.lower()]['B'].item() / (df[df['Nombre'].str.lower().str.translate(traduccion) == elemento2.lower()]['A'].item() - np.log(presion))) - df[df['Nombre'].str.lower().str.translate(traduccion) == elemento2.lower()]['C'].item()
                t = (y1 * t1) + (y2 * t2)
                x1, x2, coef1, coef2 = iteracion3(t, presion, y1, y2, elemento1, elemento2, message)
                k1 = y1 / x1
                k2 = y2 / x2
                tb.send_message(message.chat.id, f'Valor K de {elemento1}: {k1}')
                tb.send_message(message.chat.id, f'Valor K de {elemento2}: {k2}')
                variables.update({'T1':t1, 'T2':t2, 'GAMMA 1':coef1, 'GAMMA 2':coef2, 'T':t, 'X1':x1, 'x2':x2})
                markup = types.ReplyKeyboardMarkup(row_width=1)
                itembtn1 = types.KeyboardButton('Sí')
                itembtn2 = types.KeyboardButton('No')
                markup.add(itembtn1, itembtn2)
                tb.send_message(message.chat.id, 'Desea algún otro valor del cálculo?', reply_markup=markup)
    elif message.reply_to_message.text == 'Introduzca Temperatura el Sistema en grados Celsius (Valor Numerico):':
        datos_user.append(float(message.text))
        tb.send_message(message.chat.id, 'Introduzca Presión del Sistema (Valor Numerico):', reply_markup = types.ForceReply(selective = False))
    # Metodo Wilson
    elif message.reply_to_message.text == 'Introduzca Presión del Sistema (Valor Numerico):':
        if metodo[0] == 'Correlación de Wilson':
            datos_user.append(float(message.text))
            elemento1 = datos_user[0]
            elemento2 = datos_user[1]
            euler = 2.718281828
            temp = (datos_user[2] * (9/5)) + 491.67
            presion = datos_user[3]/ 6.895
            df['Pc (kpa)'] = df['Pc (kpa)'].apply(lambda x: x / 6.895)
            df['Tc (°C)'] = df['Tc (°C)'].apply(lambda x: (x * (9/5)) + 491.67)
            pci1 = df[df['Nombre'].str.lower().str.translate(traduccion) == elemento1.lower()]['Pc (kpa)'].item()
            tci1 = df[df['Nombre'].str.lower().str.translate(traduccion) == elemento1.lower()]['Tc (°C)'].item()
            W1 = df[df['Nombre'].str.lower().str.translate(traduccion) == elemento1.lower()]['W'].item()
            k1 = (pci1 / presion) * (euler ** (5.37 * (1 + W1) * (1 - (tci1 / temp))))
            pci2 = df[df['Nombre'].str.lower().str.translate(traduccion) == elemento2.lower()]['Pc (kpa)'].item()
            tci2 = df[df['Nombre'].str.lower().str.translate(traduccion) == elemento2.lower()]['Tc (°C)'].item()
            W2 = df[df['Nombre'].str.lower().str.translate(traduccion) == elemento2.lower()]['W'].item()
            k2 = (pci2 / presion) * (euler ** (5.37 * (1 + W2) * (1 - (tci2 / temp))))
            tb.send_message(message.chat.id, f'Valor K de {elemento1}: {k1}')
            tb.send_message(message.chat.id, f'Valor K de {elemento2}: {k2}')
            variables.update({'Pci 1': pci1, 'Tci 1': tci1, 'W1': W1, 'Pci 2': pci2, 'Tci 2': tci2, 'W2': W2})
            markup = types.ReplyKeyboardMarkup(row_width=1)
            itembtn1 = types.KeyboardButton('Sí')
            itembtn2 = types.KeyboardButton('No')
            markup.add(itembtn1, itembtn2)
            tb.send_message(message.chat.id, 'Desea algún otro valor del cálculo?', reply_markup=markup)
        else:
            datos_user.append(float(message.text))
            tb.send_message(message.chat.id, 'Introduzca Presión de Convergencia (Valor Numerico):', reply_markup = types.ForceReply(selective = False))
    
@tb.message_handler(func = lambda message: True)
def respuesta(message):
    if message.text == 'Ley de Raoult Modificada':
        metodo.append(message.text)
        markup = types.ReplyKeyboardMarkup(row_width=1)
        itembtn1 = types.KeyboardButton('Temperatura')
        itembtn2 = types.KeyboardButton('Presión')
        markup.add(itembtn1, itembtn2)
        tb.send_message(message.chat.id, "Valor que conoce:", reply_markup=markup)
    elif message.text == 'Correlación de Wilson':
        metodo.append(message.text)
        tb.send_message(message.chat.id, 'Introduzca Temperatura el Sistema en grados Celsius (Valor Numerico):', reply_markup = types.ForceReply(selective = False))
    elif message.text == 'Temperatura' or message.text == 'Presión':
        valor_conocido.append(message.text)
        markup = types.ReplyKeyboardMarkup(row_width=1)
        itembtn1 = types.KeyboardButton('Fracción Líquida (Elemento 1)')
        itembtn2 = types.KeyboardButton('Fracción de Vapor (Elemento 1)')
        markup.add(itembtn1, itembtn2)
        tb.send_message(message.chat.id, "Valor de Prueba:", reply_markup=markup)    
    elif message.text == 'Fracción Líquida (Elemento 1)' or message.text =='Fracción de Vapor (Elemento 1)':
        valor_prueba.append(message.text)
        if valor_conocido[0] == 'Temperatura':
            tb.send_message(message.chat.id, 'Introduzca Temperatura en grados Celsius (Valor Numerico):', reply_markup = types.ForceReply(selective = False))
        elif valor_conocido[0] == 'Presión':
            tb.send_message(message.chat.id, 'Introduzca Presión en Kpa (Valor Numerico):', reply_markup = types.ForceReply(selective = False))
    
    elif message.text == 'Sí':
        keys = [x for x in variables.keys()]
        if len(keys) % 2 ==0:
            markup = types.ReplyKeyboardMarkup(row_width=2)
            for x, y in zip(keys[0::2], keys[1::2]):
                item = types.KeyboardButton(x)
                item2 = types.KeyboardButton(y)
                markup.add(item, item2)
        else:
            markup = types.ReplyKeyboardMarkup(row_width=1)
            for x in keys:
                item = types.KeyboardButton(x)
                markup.add(item)
        tb.send_message(message.chat.id, "Que valor desea conocer?", reply_markup=markup)   
    elif message.text == 'No':
        tb.send_message(message.chat.id, 'Para hacer otro cálculo, por favor utilice el comando /nuevocalculo', reply_markup = types.ReplyKeyboardRemove(selective = False))
    elif message.text in variables.keys():
        tb.send_message(message.chat.id, f'El valor de {message.text} es: {variables.get(message.text)}')
        markup = types.ReplyKeyboardMarkup(row_width=1)
        itembtn1 = types.KeyboardButton('Sí')
        itembtn2 = types.KeyboardButton('No')
        markup.add(itembtn1, itembtn2)
        tb.send_message(message.chat.id, 'Desea algún otro valor del cálculo?', reply_markup=markup)

tb.polling(none_stop=True, interval=0, timeout=1)
