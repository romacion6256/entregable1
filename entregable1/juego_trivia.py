import os
import csv
import random
from itertools import chain
from functools import reduce
from typing import List, Generator, Tuple, Callable

# CARGA DE PREGUNTAS
def cargar_preguntas(ruta_archivo_csv: str) -> Generator[Tuple[str, List[str], str], None, None]:
    # Se usa os.path para construir rutas relativas de manera robusta
    ruta_archivo_csv = os.path.join(os.path.dirname(__file__), ruta_archivo_csv)
    with open(ruta_archivo_csv, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        next(lector)  # Saltar el encabezado
        # Usar yield y map para devolver cada línea transformada sin un bucle explícito
        yield from map(lambda x: (x[0], x[1:-1], x[-1]), lector)

# DECORADOR
def decorador_documento(descripcion: str):
    def wrapper(func: Callable):
        func.__doc__ = descripcion
        return func
    return wrapper

# ELECCION DE 5 PREGUNTAS ALEATORIAS
@decorador_documento("Selecciona 5 preguntas aleatorias del documento trivia_questions.csv")
def seleccionar_preguntas_aleatoreas(preguntas: List[Tuple[str, List[str], str]]) -> List[Tuple[str, List[str], str]]:
    return random.sample(preguntas, 5)

# CORRER EL JUEGO Y SISTEMA DE PUNTUACION
@decorador_documento("Corre el juego y calcula el puntaje")
def correr_trivia(preguntas_seleccionadas: List[Tuple[str, List[str], str]]) -> List[int]:
    # Función para procesar una sola pregunta
    def procesar_pregunta(pregunta, opciones, correcta):
        print(pregunta)
        list(map(lambda i_opcion: print(f"{i_opcion[0] + 1}. {i_opcion[1]}"), enumerate(opciones)))
        
        answer = input("Seleccione la opción correcta (1/2/3): ")
        return 10 if opciones[int(answer) - 1] == correcta else 0

    # Usamos map para aplicar procesar_pregunta a cada conjunto de pregunta, opciones y correcta
    puntaje = list(map(lambda y: procesar_pregunta(y[0], y[1], y[2]), preguntas_seleccionadas))
    
    return puntaje

# PREGUNTAR AL USUARIO SI QUIERE JUGAR DE NUEVO
@decorador_documento("Le pregunta al usuario si quiere jugar de nuevo")
def preguntar_jugar_de_nuevo() -> bool:
    respuesta = input("¿Quieres jugar otra vez? (s/n): ").lower()
    if respuesta == 's':
        return True
    elif respuesta == 'n':
        return False
    else:
        return preguntar_jugar_de_nuevo()
    
# COMBINAR TODAS LAS RESPUESTAS POSIBLES EN UNA SOLA LISTA
@decorador_documento("Combine all possible answers into a single list")
def respuestas_correctas(preguntas: List[Tuple[str, List[str], str]]) -> List[str]:
    respuestas_correctas = [[correcta] for _, _, correcta in preguntas]
    return list(chain(*respuestas_correctas))

# FUNCION PRINCIPAL
@decorador_documento("Función principal que corre la trivia")
def main():
    preguntas = list(cargar_preguntas('trivia_questions.csv'))
    
    preguntas_seleccionadas = seleccionar_preguntas_aleatoreas(preguntas)
    puntajes = correr_trivia(preguntas_seleccionadas)
        
    puntaje_total = reduce(lambda x, y: x + y, puntajes)  
    print(f"Tu puntaje final es: {puntaje_total}")

    todas_las_respuestas = respuestas_correctas(preguntas_seleccionadas)
    print("Todas las respuestas correctas en este juego fueron:")
    list(map(lambda x: print(f"{x[0] + 1}. {x[1]}"), enumerate(todas_las_respuestas)))
      
    if preguntar_jugar_de_nuevo():
        return main()
    else:
        return print("Gracias por jugar")

if __name__ == "__main__":    
    main()