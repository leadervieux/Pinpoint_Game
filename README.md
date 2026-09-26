# Pinpoint_Game

Trabajamos dividiendo el proyecto en 3 partes: la parte de WordNet y generación de la palabra y las pistas, la parte de lematización, y finalmente la parte de interfaz y visualización.

## Instrucciones de ejecución

### Requisitos previos
- Python 3.9 o superior

### 1. Clonar el repositorio
```bash
git clone <https://github.com/leadervieux/Pinpoint_Game.git>
cd Pinpoint_Game
```

### 2. Crear y activar un entorno virtual

**macOS / Linux :**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows :**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar las dependencias
```bash
pip install nltk
```

### 4. Ejecutar el juego
```bash
python3 trabajo_final.py
```

> Nota: en la primera ejecución, el script descarga automáticamente los recursos de WordNet y Open Multilingual WordNet necesarios (`wordnet`, `omw-1.4`, `omw-2.0`). Esto solo toma unos segundos y no se repite en las ejecuciones siguientes.

### 5. Jugar
El juego te pedirá:
1. El idioma de las pistas (`spa`, `fra` o `eng`)
2. El idioma de la respuesta esperada (`spa`, `fra` o `eng`)

Las 5 pistas se mostrarán a continuación, de la más general a la más específica.

## Código

Decidimos usar GitHub / Google Colab para exponer nuestras ideas. A continuación, la explicación del código. 


### Wornet
En primer lugar, creamos 3 bancos de palabras diferentes (francés, español, inglés). Optamos por esta opción porque elegir una palabra al azar directamente en WordNet es demasiado arriesgado, dado el número de palabras muy específicas ("niche") que existen -- difíciles de encontrar, y con pocas pistas por palabra. El usuario puede elegir el idioma que desee para las pistas, pero también para su respuesta. La primera función, nombre_seguro(), consiste en verificar que la palabra elegida exista efectivamente en la base de datos de WordNet. La segunda, crear_palabras(), elige una palabra del banco correspondiente al idioma seleccionado, verificando que tenga al menos 1 hiperónimo, 2 hipónimos y una traducción válida, para facilitarnos el resto del código y las verificaciones. Pusimos un bucle de 500 iteraciones para no hacer fallar el ordenador en caso de problema con las palabras. Una tercera función gestiona las pistas, y recupera sistemáticamente sustantivos (más fáciles de adivinar, menos específicos). Por último, la generación de la partida, que es la que coordina todo esto, y que verifica si efectivamente tenemos 5 pistas. Si no, elegimos otra palabra al azar.

### Lematización

Para validar la respuesta del jugador no basta con comparar las cadenas de texto directamente: hay que normalizarlas primero y después reducirlas a su raíz, de modo que variantes como el plural, el género o las mayúsculas/acentos no impidan reconocer una respuesta correcta.

El proceso se hace en dos pasos:

1. **`normalize()`** — limpieza de la cadena: pasa el texto a minúsculas y elimina los acentos/diacríticos usando `unicodedata` (normalización NFD, luego se descartan los caracteres de la categoría `Mn`, es decir las marcas diacríticas). Por ejemplo, `"Île"` se convierte en `"ile"`.

2. **`stemmer_word()`** — aplica un *stemming* (reducción a la raíz de la palabra) sobre el texto ya normalizado, usando `SnowballStemmer` de NLTK. Usamos **tres stemmers distintos**, uno por idioma soportado (`SnowballStemmer("french")`, `SnowballStemmer("spanish")`, `SnowballStemmer("english")`), y se elige el stemmer correspondiente según el idioma de la partida en curso.

Finalmente, **`is_same_word()`** compara el stem de la propuesta del jugador con el stem de la respuesta esperada: si ambos stems coinciden, la respuesta se considera correcta — incluso si difiere en mayúsculas, acentos, singular/plural, o (parcialmente) género.

Ejemplo: si la respuesta esperada es `"chien"`, las propuestas `"Chien"`, `"CHIENS"` o `"chiens "` son todas aceptadas, porque una vez normalizadas y reducidas a su raíz (`stem`) dan el mismo resultado (`"chien"`).

> Nota: se trata de *stemming* (reducción heurística a una raíz aproximada) y no de lematización propiamente dicha (que requeriría un análisis morfológico completo para volver a la forma canónica exacta de la palabra). Elegimos Snowball porque NLTK ofrece una implementación lista para usar en los 3 idiomas del proyecto, lo cual cumple el requisito 4.2 del enunciado ("Lematización y/o stemming").
