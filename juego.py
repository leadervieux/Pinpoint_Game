"""
juego.py — Lógica del juego y bucle de consola
Ejecutar con: python3 juego.py
"""
from wordnet_pistas import generar_partida
from lematizacion import normalize, is_same_word

IDIOMAS_VALIDOS = ("eng", "fra", "spa")
NOMBRES_IDIOMA = {"eng": "inglés", "fra": "francés", "spa": "español"}


class Game:
    """
    [MODIFICATION] : 'self.rounds' ahora es una LISTA de diccionarios en lugar de un diccionario simple.
    Esto previene que rondas con palabras repetidas se sobreescriban y facilita el acceso indexado por ronda.
    """
    def __init__(self, round_count, langage_pistas, langage_respuesta, generar_partida_fn):
        self.langage_pistas = langage_pistas
        self.langage_respuesta = langage_respuesta
        self.rounds = []
        
        while len(self.rounds) < round_count:
            palabra_pista, indicios, origen, palabra_respuesta = generar_partida_fn(
                langage_pistas, langage_respuesta
            )
            if palabra_pista and indicios and palabra_respuesta:
                self.rounds.append({
                    "palabra_pista": palabra_pista,
                    "indicios": indicios,
                    "origen": origen,
                    "palabra_respuesta": palabra_respuesta,
                })
                
        self.r = 0
        self.clues = 0
        self.score = 0
        self.round_finished = False
        self.n_round = round_count

    def is_last(self):
        return self.r == (self.n_round - 1)

    def answer(self, text):
        if self.round_finished:
            return "Round_finished"
            
        word_normalised = normalize(text)
        if not word_normalised:
            return "Empty"
            
        # [MODIFICATION] : Compara contra la respuesta esperada en el idioma seleccionado para responder
        respuesta_esperada = self.rounds[self.r]["palabra_respuesta"]
        if is_same_word(text, respuesta_esperada, self.langage_respuesta):
            self.score += 6 - self.clues
            self.round_finished = True
            return "words_found"
            
        if self.clues < 4:
            self.clues += 1
            return "wrong"
            
        self.round_finished = True
        return "out_of_clues"

    def next_round(self):
        if not self.round_finished or self.is_last():
            return False
        self.r += 1
        self.clues = 0
        self.round_finished = False
        return True


def pedir_idioma(mensaje):
    """
    [MODIFICATION] : Entrada segura de idioma en minúsculas y validada contra la tupla de idiomas.
    """
    idioma = ""
    while idioma not in IDIOMAS_VALIDOS:
        idioma = input(mensaje).strip().lower()
        if idioma not in IDIOMAS_VALIDOS:
            print("Idioma no válido. Ingrese 'eng', 'fra' o 'spa'.")
    return idioma


def pedir_numero_rondas():
    """
    [MODIFICATION] : Permite definir el número de rondas dinámicamente por la consola.
    """
    while True:
        texto = input("¿Cuántas rondas deseas jugar? (ej: 3): ").strip()
        if texto.isdigit() and int(texto) > 0:
            return int(texto)
        print("Por favor, ingrese un número entero positivo.")


def play_console():
    print("=== Pinpoint · WordNet Edition ===\n")
    lang_pistas = pedir_idioma("Idioma de las pistas (eng, fra, spa): ")
    lang_respuesta = pedir_idioma("Idioma de la respuesta esperada (eng, fra, spa): ")
    n_round = pedir_numero_rondas()

    print(f"\nPistas en {NOMBRES_IDIOMA[lang_pistas]}, respuestas en {NOMBRES_IDIOMA[lang_respuesta]}.")
    print("Generando partida, espera un momento...\n")
    game = Game(n_round, lang_pistas, lang_respuesta, generar_partida)

    while True:
        print(f"=== Ronda {game.r + 1}/{game.n_round} | Puntaje actual: {game.score} ===")
        while not game.round_finished:
            # [MODIFICATION] : Muestra la pista junto con su categoría semántica (hiperónimo, hipónimo, sinónimo)
            clue = game.rounds[game.r]["indicios"][game.clues]
            origen = game.rounds[game.r]["origen"][game.clues]
            print(f"Pista {game.clues + 1} [{origen}]: {clue}")
            
            text = input("  Tu respuesta (o 'exit' para salir): ").strip()
            if text.lower() == "exit":
                print(f"\nPartida cancelada. Puntaje final: {game.score}")
                return
                
            resultado = game.answer(text)
            if resultado == "Empty":
                print("  Debes escribir una respuesta.")
            elif resultado == "wrong":
                print("  Incorrecto, aquí tienes otra pista...")
            elif resultado == "words_found":
                print(f"  ¡Correcto! La palabra era '{game.rounds[game.r]['palabra_respuesta']}'. Puntaje: {game.score}\n")
            elif resultado == "out_of_clues":
                print(f"  Se acabaron las pistas. La respuesta correcta era '{game.rounds[game.r]['palabra_respuesta']}'.\n")
                
        if not game.next_round():
            break

    print(f"=== Juego terminado. Puntaje final: {game.score} ===")


if __name__ == "__main__":
    play_console()
