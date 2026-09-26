"""
wordnet_pistas.py : Selección de conceptos y generación de indicios semánticos
"""
import random as rd
import nltk
from nltk.corpus import wordnet as wn

# Descargas silenciosas de los paquetes necesarios
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# Listas de vocabulario alineadas índice por índice
MOTS_ANGLAIS = [
    "guitar", "violin", "piano", "drum", "trumpet", "flute", "harp", "saxophone",
    "lawyer", "teacher", "doctor", "surgeon", "farmer", "engineer", "pilot", "nurse",
    "firefighter", "police_officer", "chef", "dentist", "architect", "plumber",
    "electrician", "mechanic", "astronaut", "scientist", "painter", "photographer",
    "elephant", "penguin", "kangaroo", "dolphin", "giraffe", "zebra", "tiger", "lion",
    "panda", "koala", "octopus", "eagle", "owl", "butterfly", "spider", "crocodile",
    "umbrella", "backpack", "camera", "telescope", "microscope", "compass", "map",
    "calculator", "keyboard", "mirror", "candle", "lantern", "basket", "ladder",
    "hospital", "airport", "library", "museum", "cathedral", "castle", "lighthouse",
    "stadium", "theater", "bakery", "pharmacy", "supermarket", "restaurant", "hotel",
    "bicycle", "helicopter", "sailboat", "submarine", "train", "airplane", "rocket",
    "motorcycle", "canoe", "tractor", "ambulance",
    "waterfall", "volcano", "mountain", "desert", "forest", "glacier", "island",
    "river", "cave", "cliff", "valley", "beach", "lake",
    "violinist", "carpenter", "blacksmith", "beekeeper",
]

MOTS_ESPAGNOL = [
    "guitarra", "violín", "piano", "tambor", "trompeta", "flauta", "arpa", "saxofón",
    "abogado", "profesor", "médico", "cirujano", "agricultor", "ingeniero", "piloto",
    "enfermera", "bombero", "policía", "cocinero", "dentista", "arquitecto", "fontanero",
    "electricista", "mecánico", "astronauta", "científico", "pintor", "fotógrafo",
    "elefante", "pingüino", "canguro", "delfín", "jirafa", "cebra", "tigre", "león",
    "panda", "koala", "pulpo", "águila", "búho", "mariposa", "araña", "cocodrilo",
    "paraguas", "mochila", "cámara", "telescopio", "microscopio", "brújula", "mapa",
    "calculadora", "teclado", "espejo", "vela", "linterna", "cesta", "escalera",
    "hospital", "aeropuerto", "biblioteca", "museo", "catedral", "castillo", "faro",
    "estadio", "teatro", "panadería", "farmacia", "supermercado", "restaurante", "hotel",
    "bicicleta", "helicóptero", "velero", "submarino", "tren", "avión", "cohete",
    "motocicleta", "canoa", "tractor", "ambulancia",
    "cascada", "volcán", "montaña", "desierto", "bosque", "glaciar", "isla",
    "río", "cueva", "acantilado", "valle", "playa", "lago",
    "violinista", "carpintero", "herrero", "apicultor",
]

MOTS_FRANCAIS = [
    "guitare", "violon", "piano", "tambour", "trompette", "flûte", "harpe", "saxophone",
    "avocat", "professeur", "médecin", "chirurgien", "agriculteur", "ingénieur", "pilote",
    "infirmière", "pompier", "policier", "cuisinier", "dentiste", "architecte", "plombier",
    "électricien", "mécanicien", "astronaute", "scientifique", "peintre", "photographe",
    "éléphant", "pingouin", "kangourou", "dauphin", "girafe", "zèbre", "tigre", "lion",
    "panda", "koala", "poulpe", "aigle", "hibou", "papillon", "araignée", "crocodile",
    "parapluie", "sac_à_dos", "appareil_photo", "télescope", "microscope", "boussole",
    "carte", "calculatrice", "clavier", "miroir", "bougie", "lanterne", "panier", "échelle",
    "hôpital", "aéroport", "bibliothèque", "musée", "cathédrale", "château", "phare",
    "stade", "théâtre", "boulangerie", "pharmacie", "supermarché", "restaurant", "hôtel",
    "vélo", "hélicoptère", "voilier", "sous-marin", "train", "avion", "fusée",
    "moto", "canoë", "tracteur", "ambulance",
    "cascade", "volcan", "montagne", "désert", "forêt", "glacier", "île",
    "rivière", "grotte", "falaise", "vallée", "plage", "lac",
    "violiniste", "charpentier", "forgeron", "apiculteur",
]


def nombre_seguro(synset, idioma):
    """
    Retorna el lema traducido si existe en el idioma dado, o None si no hay traducción.
    """
    if idioma == "eng":
        lemas = synset.lemmas()
    else:
        lemas = synset.lemmas(lang=idioma)

    if not lemas:
        return None
    nombre = lemas[0].name().replace("_", " ")
    return nombre.split("|")[0]


def _banco(idioma):
    if idioma == "spa":
        return MOTS_ESPAGNOL
    elif idioma == "fra":
        return MOTS_FRANCAIS
    return MOTS_ANGLAIS


# [MODIFICATION] : Nueva función para desambiguar el sentido correcto.
# WordNet solo ordena los synsets por frecuencia en inglés. Para evitar sentidos
# erróneos en español o francés (ej. 'forêt' interpretado como broca en lugar de bosque),
# se usa el synset del inglés como referencia canónica y se hace intersección con el idioma destino.
def obtener_synset_por_indice(indice, idioma):
    palabra_en = MOTS_ANGLAIS[indice]
    synsets_en = wn.synsets(palabra_en, pos=wn.NOUN)
    if not synsets_en:
        return None

    if idioma == "eng":
        return synsets_en[0]

    palabra_cible = _banco(idioma)[indice]
    synsets_cible = set(wn.synsets(palabra_cible, lang=idioma, pos=wn.NOUN))
    if not synsets_cible:
        return None

    for s in synsets_en:
        if s in synsets_cible:
            return s

    return next(iter(synsets_cible))


# [MODIFICATION] : Retorna un índice numérico en lugar de un string arbitrario
# para garantizar que la misma palabra y su traducción compartan exactamente el mismo concepto.
def crear_palabras(idioma_i, max_intentos=500):
    n = len(MOTS_ANGLAIS)
    for _ in range(max_intentos):
        indice = rd.randrange(n)
        s = obtener_synset_por_indice(indice, idioma_i)
        if s is None:
            continue
        if (len(s.hypernyms()) > 0
                and len(s.hyponyms()) > 1
                and nombre_seguro(s, idioma_i) is not None):
            return indice

    raise RuntimeError("No se encontró ninguna palabra válida en el banco.")


# [MODIFICATION] : Recibe el 'indice' validado y genera las pistas junto con
# el arreglo 'origen' que especifica la relación léxica (hiperónimo, hipónimo, sinónimo).
def obtener_indicios(indice, idioma_i):
    synset = obtener_synset_por_indice(indice, idioma_i)
    palabra = _banco(idioma_i)[indice]

    indicios = []
    origen = []

    hyperonymos = synset.hypernyms()
    hyponyms = synset.hyponyms()

    # 1. Hiperónimos
    candidatos_hiper = list(hyperonymos)
    if hyperonymos:
        candidatos_hiper += hyperonymos[0].hypernyms()

    for h in candidatos_hiper:
        if len(indicios) >= 2:
            break
        nombre = nombre_seguro(h, idioma_i)
        if nombre and nombre.lower() != palabra.replace("_", " ").lower() and nombre not in indicios:
            indicios.append(nombre)
            origen.append("hiperónimo")

    # 2. Hipónimos
    rd.shuffle(hyponyms)
    for h in hyponyms:
        if len(indicios) >= 4:
            break
        nombre = nombre_seguro(h, idioma_i)
        if nombre and nombre.lower() != palabra.replace("_", " ").lower() and nombre not in indicios:
            indicios.append(nombre)
            origen.append("hipónimo")

    # 3. Sinónimos
    if idioma_i == "eng":
        lemas = synset.lemmas()
    else:
        lemas = synset.lemmas(lang=idioma_i)

    sinonimos = [l.name().replace("_", " ").split("|")[0] for l in lemas]
    sinonimos = [s for s in sinonimos if s.lower() != palabra.replace("_", " ").lower()]
    rd.shuffle(sinonimos)
    for s in sinonimos:
        if len(indicios) >= 5:
            break
        if s not in indicios:
            indicios.append(s)
            origen.append("sinónimo")

    # 4. Hipónimos de hipónimos en caso de faltar pistas
    if len(indicios) < 5:
        for h in hyponyms:
            for nieto in h.hyponyms():
                nombre = nombre_seguro(nieto, idioma_i)
                if nombre and nombre.lower() != palabra.replace("_", " ").lower() and nombre not in indicios:
                    indicios.append(nombre)
                    origen.append("hipónimo")
                if len(indicios) >= 5:
                    break
            if len(indicios) >= 5:
                break

    return indicios[:5], origen[:5]


# [MODIFICATION] : Recibe DOS idiomas (idioma de pistas e idioma de respuesta).
# Antes, 'idioma_preg' se leía pero nunca se usaba. Al estar las 3 listas alineadas,
# la palabra esperada se toma directamente con _banco(idioma_preg)[indice].
def generar_partida(idioma_i, idioma_preg, max_intentos=100):
    for _ in range(max_intentos):
        indice = crear_palabras(idioma_i)
        indicios, origen = obtener_indicios(indice, idioma_i)
        if len(indicios) == 5:
            palabra_pista = _banco(idioma_i)[indice]
            palabra_respuesta = _banco(idioma_preg)[indice]
            return palabra_pista, indicios, origen, palabra_respuesta

    palabra_pista = _banco(idioma_i)[indice]
    palabra_respuesta = _banco(idioma_preg)[indice]
    return palabra_pista, indicios, origen, palabra_respuesta
