"""
lematizacion.py : Normalización y comparación de respuestas
"""
import unicodedata
from nltk.stem.snowball import SnowballStemmer

# Inicialización de los stemmers de Snowball por idioma
stemmer_fr = SnowballStemmer("french")
stemmer_en = SnowballStemmer("english")
stemmer_es = SnowballStemmer("spanish")


def normalize(texte: str) -> str:
    """
    Convierte a minúsculas y elimina acentos y signos diacríticos (forma NFD).
    """
    texte = texte.lower().strip()
    texte = unicodedata.normalize('NFD', texte)
    texte = ''.join(c for c in texte if unicodedata.category(c) != 'Mn')
    return texte


def stemmer_word(word: str, lang: str) -> str:
    """
    Aplica el stemmer del idioma correspondiente sobre la cadena normalizada.
    
    [MODIFICATION] : SnowballStemmer a veces no recorta el sufijo plural en ciertas
    palabras cortas o después de quitar acentos (ej. 'velos' permanece como 'velos').
    Añadimos esta condición de seguridad para tolerar respuestas en plural del jugador.
    """
    original = normalize(word)
    if lang == "fra":
        stemmed = stemmer_fr.stem(original)
    elif lang == "spa":
        stemmed = stemmer_es.stem(original)
    elif lang == "eng":
        stemmed = stemmer_en.stem(original)
    else:
        return original

    # [MODIFICATION] : Recorte manual de la 's' final si el stemmer no la redujo
    if stemmed == original and original.endswith("s") and len(original) > 3:
        stemmed = original[:-1]
    return stemmed


def is_same_word(proposition: str, answer: str, lang: str) -> bool:
    """
    Determina si la propuesta del jugador coincide con la solución esperada.
    """
    return stemmer_word(proposition, lang) == stemmer_word(answer, lang)
