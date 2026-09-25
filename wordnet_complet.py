from nltk.corpus import wordnet as wn
import random as rd

import nltk
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)
nltk.download('omw-2.0', quiet=True)


# ============================================================
# LISTA INGLES (100 PALABRAS)
# ============================================================
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

# ============================================================
# LISTA ESPAÑOL (100 PALABRAS)
# ============================================================
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

# ============================================================
# LISTA FRANCESA (100 PALABRAS)
# ============================================================
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
    "violoniste", "charpentier", "forgeron", "apiculteur",
]


## Obtener la idioma de las instrucciones y de la pregunta

idioma_i = input("Ingrese el idioma de las instrucciones (spa, fra, eng): ")
while idioma_i != "spa" and idioma_i != "fra" and idioma_i != "eng":
    print("Idioma no válido. Por favor, ingrese 'spa', 'fra' o 'eng'.")
    idioma_i = input("Ingrese el idioma de las instrucciones (spa, fra, eng): ")

idioma_preg = input("Ingrese el idioma de la pregunta (spa, fra, eng): ")
while idioma_preg != "spa" and idioma_preg != "fra" and idioma_preg != "eng":
    print("Idioma no válido. Por favor, ingrese 'spa', 'fra' o 'eng'.")
    idioma_preg = input("Ingrese el idioma de la pregunta (spa, fra, eng): ")


# ------------------------------------------------------------
# Para verificar si un synset tiene traducción en el idioma dado, y obtener el nombre del primer lema en ese idioma.
# ------------------------------------------------------------
def nombre_seguro(synset, idioma):
    """
    Retorna el nombre del primer lema de 'synset' en el idioma dado.
    Si NO existe traducción en ese idioma para este synset, retorna None
    (en vez de plantar con IndexError).
    """
    lemas = synset.lemmas(lang=idioma)

    if not lemas:
        return None
    nombre = lemas[0].name().replace("_", " ")
    nombre = nombre.split("|")[0]
    return nombre


# ------------------------------------------------------------
# Elección de palabra
# ------------------------------------------------------------
def crear_palabras(idioma_i, max_intentos=500):
    if idioma_i == "spa":
        banco_palabras = MOTS_ESPAGNOL
    elif idioma_i == "fra":
        banco_palabras = MOTS_FRANCAIS
    elif idioma_i == "eng":
        banco_palabras = MOTS_ANGLAIS

    for _ in range(max_intentos):
        palabra = rd.choice(banco_palabras)
        synsets = wn.synsets(palabra, lang=idioma_i, pos=wn.NOUN)

        if not synsets:
            continue

        s = synsets[0]
        if (len(s.hypernyms()) > 0
                and len(s.hyponyms()) > 1
                and nombre_seguro(s, idioma_i) is not None):
            return palabra

    raise RuntimeError("No se encontró ninguna palabra válida en el banco. Revisa la lista.")


# ------------------------------------------------------------
# Generación de indicios
# ------------------------------------------------------------
def obtener_indicios(palabra, idioma_i):
    synsets = wn.synsets(palabra, lang=idioma_i, pos=wn.NOUN)
    synset = synsets[0]

    indicios = []
    origen = [] 
 
    hyperonymos = synset.hypernyms()
    hyponyms = synset.hyponyms()

    # --- Hiperónimos : intentamos 2, con reserva a nivel 3 si falta ---
    candidatos_hiper = list(hyperonymos)
    if hyperonymos:
        candidatos_hiper += hyperonymos[0].hypernyms()  # abuelo, como reserva

    for h in candidatos_hiper:
        if len(indicios) >= 2:
            break
        nombre = nombre_seguro(h, idioma_i)
        if nombre and nombre.lower() != palabra.replace("_", " ").lower() and nombre not in indicios:
            indicios.append(nombre)
            origen.append("hiperónimo")

    # --- Hipónimos : tantos como haga falta, saltando los sin traducción ---
    rd.shuffle(hyponyms)
    for h in hyponyms:
        if len(indicios) >= 4:  # dejamos sitio para 1 sinónimo al final
            break
        nombre = nombre_seguro(h, idioma_i)
        if nombre and nombre.lower() != palabra.replace("_", " ").lower() and nombre not in indicios:
            indicios.append(nombre)
            origen.append("hipónimo")

    # --- Sinónimo (excluyendo la palabra misma) ---
    lemas = synset.lemmas(lang=idioma_i)
    
    sinonimos_bruts = [l.name().replace("_", " ").split("|")[0] for l in lemas]
    sinonimos = [s for s in sinonimos_bruts if s.lower() != palabra.replace("_", " ").lower()]
    rd.shuffle(sinonimos)
    for s in sinonimos:
        if len(indicios) >= 5:
            break
        if s not in indicios:
            indicios.append(s)
            origen.append("sinónimo")

    # --- Reserva finale : hipónimos de hipónimos, si todavía falta ---
    if len(indicios) < 5:
        for h in hyponyms:
            for nieto in h.hyponyms():
                nombre = nombre_seguro(nieto, idioma_i)
                if nombre and nombre.lower() != palabra.replace("_", " ").lower() and nombre not in indicios:
                    indicios.append(nombre)
                if len(indicios) >= 5:
                    break
            if len(indicios) >= 5:
                break

    return indicios[:5], origen[:5], uso_definicion_como_repli


# ------------------------------------------------------------
# Para generar una partida, intentamos hasta 100 veces encontrar una palabra con 5 indicios sin usar la definición. Si no lo logramos, aceptamos la última palabra encontrada aunque usemos la definición.
# ------------------------------------------------------------
def generar_partida(idioma_i, max_intentos=100):
    for _ in range(max_intentos):
        palabra = crear_palabras(idioma_i)
        indicios, origen, uso_definicion = obtener_indicios(palabra, idioma_i)

        if len(indicios) == 5 and not uso_definicion:
            return palabra, indicios, origen

    # Si después de todos los intentos no hemos encontrado nada satisfactorio,
    # aceptamos el último resultado encontrado en lugar de fallar.
    return palabra, indicios, origen


# ------------------------------------------------------------
# Prueba de la función generar_partida
# ------------------------------------------------------------
palabra, indicios, origen = generar_partida(idioma_i)

print(f"\n(respuesta oculta para depuración: {palabra})\n")
for i, ind in enumerate(zip(indicios,origen), start=1):
    print(f"Indicio {i} [{org}]: {ind}")



