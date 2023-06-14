import pygame
import random 

pygame.init() # inicia nuestro programa pygame
pygame.font.init()
# creamos las dimensiones de la ventana
ANCHO = 700
ALTURA = 800
lineas = 10
columnas = 10
minas = 12
flagcount = 12
color_num = {1:"blue", 2:"green", 3:"red", 4:"blue4", 5:"brown", 6:"cyan", 7:"black", 8:"grey"} #creamos un diccionario
                                                                                          # para el color de cada número
lado = ANCHO // lineas # calculamos el lado que usaremos para cada casilla cuadrada (en px)
num_font = pygame.font.SysFont("Arial", 20)
game_over_font = pygame.font.SysFont("Arial", 100)
color_casilla = "ghostwhite"
color_descubierto = "dimgray"

# mostramos la ventana con el título "Buscaminas"
ventana = pygame.display.set_mode((ANCHO,ALTURA))
pygame.display.set_caption('Buscaminas')


def buscar_vecinos(row, col, totrows, totcols): # creamos una función que nos devuelve una lista con
                                                # las coordenadas de las casillas vecinas de una casilla
                                                # qué está en una matriz de tamaño totrows*totcols
    vecinos = []
    if row > 0: # NORTE
        vecinos.append((row-1, col))
        if col > 0 : # NOROESTE
            vecinos.append((row-1, col-1))
        if col < totcols-1: # NORESTE
            vecinos.append((row-1, col+1))
    if col > 0: # OESTE
        vecinos.append((row, col-1))
    if col < totcols-1: # ESTE
        vecinos.append((row, col+1))
    if row < totcols-1: # SUR
        vecinos.append((row+1, col))
        if col > 0 : # SUROESTE
            vecinos.append((row+1, col-1))
        if col < totcols-1: # NORESTE
            vecinos.append((row+1, col+1))
    return vecinos

        
def crear_campo_minas(rows, cols, minas): # este campo de minas contiene toda la información y no será visible
    campo = [[0 for i in range(rows)] for j in range(cols)] # creamos una matriz de tamaño rows x cols llena de ceros
    
    minas_pos = set() # creamos un conjunto de minas en el que insertaremos las coordenadas de nuestras minas
                    
    while len(minas_pos) < minas: # generamos un cierto numero de minas aleatoriamente dentro de la matriz
        row = random.randrange(0, rows)
        col = random.randrange(0, cols)
        pos = row, col
        if pos in minas_pos: # nos aseguramos de no poner la misma mina dos veces
            continue
        minas_pos.add(pos) # añadimos la mina creada aleatoriamente
        campo[row][col] = -1 # añadimos la mina al campo reemplazando el 0 por -1 para indicar su presencia
        
    # vamos a incrementar en uno todos los vecinos de cada mina que no sean minas
    for mina in minas_pos: # recorremos cada mina
        vecinos = buscar_vecinos(*mina, rows, cols) # creamos una lista de los vecinos,
                                                    # aquí, *mine nos permite descomponer la tupla mina en sus dos valores
        
        for r, c in vecinos: # recorremos los vecinos con r tomando el valor de la fila (row) y c de la columna
            if campo[r][c] != -1: # si un vecino no es una mina...
                campo[r][c] += 1 # ...lo incrementamos de 1
    return campo
            
                    
                    
def get_pos_tabla(mouse_pos):
    mx, my = mouse_pos #cogemos la pos del ratón
    linea = (my//lado)
    columna = int(mx // lado)
    # calculamos en qué línea está el ratón con el cociente entero
    return linea, columna
    
# ------------------------------------------------- inicio función draw              
def draw(ventana, campo, cubierta): #la función draw nos permite dibujar la pantalla de juego
    ventana.fill("white") # ponemos el fondo blanco
    
    for i, lin in enumerate(campo): # recorremos las líneas del campo con el indíce i
        y = i * lado # la coordenada vertical de una casilla será el indice de la línea multiplicado
                 #  por el lado de cada casilla ya que estará bajo i casillas de tamaño "lado"
        for j, valor in enumerate(lin):
            x = j * lado # de la misma manera calculamos la coordenada horizontal
            if cubierta[i][j] == -2: #si ponemos una bandera en la casilla, la pintamos de rojo y reiniciamos el for
                pygame.draw.rect(ventana, "red", (x,y, lado, lado))
                pygame.draw.rect(ventana, "black", (x,y, lado, lado), 4) # dibujamos un borde negro para nuestras casillas
                continue
            if cubierta[i][j] == 1: # miramos si la casilla ha sido descubierta
                if campo[i][j] == -1: # si la casilla descubierta es una mina:
                    pygame.draw.rect(ventana, "black", (x,y, lado, lado)) # pintamos la casilla de negro
                else:
                    pygame.draw.rect(ventana, color_descubierto, (x,y, lado, lado)) # en caso afirmativo, dibujamos un cuadrado
                                                                            # de tamaño lado*lado en la posicíon x,y con
                                                                            # un color oscuro ya que ha sido descubierto
                    pygame.draw.rect(ventana, "black", (x,y, lado, lado), 4) # dibujamos un borde negro para nuestras casillas
            
            if cubierta[i][j] == 0:
                pygame.draw.rect(ventana, color_casilla, (x,y, lado, lado)) # en caso afirmativo, dibujamos un cuadrado de 
                                                                            # tamaño lado x lado en la posición x,y con
                                                                            # un color más claro
                pygame.draw.rect(ventana, "black", (x,y, lado, lado), 4) # dibujamos un borde negro para nuestras casillas
                continue # este continue resetea el while impidiendo que se dibuje el número en una casilla no descubierta 
            
                
            
            # dibujemos los números
            if valor > 0: #excluimos casillas vacías o minas
                text = num_font.render(str(valor), 1, color_num[valor]) # creamos una variable de texto donde
                                                                        # renderizamos el valor cambiando su tipo a
                                                                        # string renderizándolo en arial, 20 (=num_font)  
                                                                        # y mirando el color en el diccionario de 
                                                                        # colores con antialiasing igual a 1
                ventana.blit(text, (x + lado/2 - text.get_width()/2, y +lado/2 - text.get_height()/2))
# el método blit permite dibujar una imagen sobre otra, en este caso la usamos para dibujar los números sobre la casilla
# si dibujáramos en (x,y), blit pondría el número desde la esquina superior derecha de cada casillas. añadir lado/2 nos
# permite centrar el cursor en medio de la casilla. sin embargo blit dibujará nuestro numero en la esquina inferior
# derecha, por tanto hemos de mover nuestro cursor de media anchura del texto hacía la izquierda y 
# de media altura hacía arriba
                         
                         
    pygame.display.update() # actualizamos la ventana para poder visualizar los gráficos
    
# ------------------------------------------------- fin función draw
 
    
def descubrir_desde_pos(linea, columna, cubierta, campo): # esta función descubre todas las casillas vecinas a las casillas
                                                          # blancas conectadas a una casilla inicial(que debe ser blanca)
    queue = [] # crea una lista en la que pondremos todas las casillas blancas
    queue.append((linea, columna)) #añade nuestra casilla inicial
    visitadas = set() # creamos un conjunto con las casillas ya visitadas para asegurarnos de que el bucle while termina
    
    while len(queue) != 0: #este while descubre exhaus
        actual = queue.pop(0) #saca una casilla de la lista y la guarda en la variable actual
          
        vecinos = buscar_vecinos(*actual, lineas, columnas) # descompone la casilla y busca sus vecinos
        for l, c in vecinos:
            if (l, c) not in visitadas: #verifica que la casilla no haya sido ya visitada para evitar bucles infinitos
                valor = campo[l][c] 
                cubierta[l][c] = 1 #descubre todas las casillas vecinas
                if valor == 0: #si la casilla está vacía, queremos descubrir sus vecinoas
                    queue.append((l,c)) # así que la añadimos a la lista para explorar los vecinos en el siguiente bucle
        visitadas.add(actual) #marcamos la casilla cómo visitada

def draw_text(ventana, texto):
        msg = game_over_font.render(texto, 1, "black")
        ventana.blit(msg, (ALTURA/2 - msg.get_width()/2, ALTURA/2-msg.get_height()/2))
        pygame.display.update()
        
def main():
    acabado = False 
    campo = crear_campo_minas(lineas, columnas, minas) # creamos la tabla con las minas
    banderas = set() #creamos un conjuntos con las banderas
    cubierta = [[0 for i in range(lineas)] for j in range(columnas)] # creamos la tabla donde las casillas están cubiertas
    #------------------------------------------ inicio bucle de juego
    while not acabado:
    #------------------------------------------ inicio bucle eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # nos permite salir del juego
                acabado = True
                break
            draw(ventana, campo, cubierta)
            if event.type == pygame.MOUSEBUTTONDOWN: # si el mouse hace un click:
                mouse_button = pygame.mouse.get_pressed()
                l, c = get_pos_tabla(pygame.mouse.get_pos()) # buscamos la línea y columna de la tabla que ha pulsado
                if l >= lineas or c >= columnas: # si el mouse hace un click fuera de la tabla...
                        continue # ...volvemos al inicio del for
                if mouse_button[0] and cubierta[l][c] !=-2:
                    if campo[l][c] ==-1: #si clicamos una mina perdemos la partida
                        pygame.draw.rect(ventana, "black", (c*lado, l*lado, lado, lado))
                        draw_text(ventana, "Perdiste :(")
                        pygame.time.delay(2000)
                        acabado = True                        
                    else:
                        cubierta[l][c] = 1 # si se pulsa click izquierdo descubrimos una casilla
                        if campo[l][c] == 0:
                            descubrir_desde_pos(l, c, cubierta, campo) # si la casilla está vacía descubrimos
                                                                       # todas las casillas vacías y sus vecinos
                if mouse_button[2]: #el boton derecho sirve para gestionar banderas
                    if cubierta[l][c] == -2: # quitamos una bandera si ya hay una en la casilla
                        banderas.remove((l,c)) # la sacamos de la lista
                        cubierta[l][c] = 0
                        flagcount += 1
                    elif cubierta[l][c] == 0 and flagcount > 0:
                        flagcount -= 1
                        banderas.add((l,c))# si se pulsa click derecho añadimos una bandera
                        cubierta[l][c] = -2 # usaremos el código -2 para identificar la bandera. esta va en la cubierta para 
                                        # no sobreescribir el valor real de la casilla en el campo
                if not any(0 in i for i in cubierta): # si no hay ninguna casilla que no haya sido descubierta o lleve bandera ganamos
                    draw_text(ventana, "Ganaste :)")
                    pygame.time.delay(2000)
                    acabado = True
                
                draw(ventana, campo, cubierta)
    #------------------------------------------ fin bucle eventos
    
    pygame.quit()
    #------------------------------------------ fin bucle de juego
main()
