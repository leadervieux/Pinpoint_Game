# Pinpoint_Game

Trabajamos dividiendo el proyecto en 3 partes: la parte de WordNet y generación de la palabra y las pistas, la parte de lematización, y finalmente la parte de interfaz y visualización.

## Instrucciones de ejecución

Descarga el archivo <Pinpoint_Game.ipynb> y ábrelo en Google Colab. Ejecuta las consultas.

### 5. Jugar
El juego te pedirá:
1. El idioma de las pistas (`spa`, `fra` o `eng`)
2. El idioma de la respuesta esperada (`spa`, `fra` o `eng`)

Las 5 pistas se mostrarán a continuación, de la más general a la más específica.

## Código

Decidimos usar GitHub para exponer nuestras ideas. A continuación, la explicación del código. 


### Wornet
La primera función clave, nombre_seguro(), consiste en verificar que un concepto (synset) posea una traducción válida en el idioma seleccionado, evitando errores críticos como el IndexError si WordNet no encuentra lemas para ese idioma.
A continuación, incorporamos una función fundamental para desambiguar el sentido correcto: obtener_synset_por_indice(). Como WordNet solo ordena los synsets por frecuencia en inglés, esta función utiliza el término en inglés como referencia canónica y realiza una intersección con los synsets del idioma de destino. Esto evita errores graves de traducción o polisemia (por ejemplo, evitar que la palabra francesa "forêt" se interprete por error como una broca en lugar de un bosque).
La tercera función, crear_palabras(), selecciona un índice aleatorio y comprueba mediante la función anterior que el concepto cumpla con condiciones estrictas: tener al menos un hiperónimo, dos hipónimos y una traducción válida, garantizando así la calidad del juego. Establecimos un límite de quinientos intentos para evitar bucles infinitos o bloqueos.
La cuarta función, obtener_indicios(), se encarga de generar exactamente cinco pistas estructuradas por jerarquía semántica: primero recuperamos hasta dos hiperónimos (conceptos más amplios), después completamos hasta cuatro con hipónimos (conceptos más específicos), y finalmente añadimos sinónimos o hipónimos de segundo nivel si faltan pistas. Todo esto filtrando siempre para que no aparezca la palabra buscada.
Por último, la función generar_partida() coordina todo el flujo. Selecciona el concepto validado y extrae de forma paralela la palabra pista en el idioma de las instrucciones y la palabra respuesta en el idioma elegido por el usuario, asegurando que siempre se disponga de las cinco pistas necesarias antes de iniciar el juego.

### Lematización

Para validar la respuesta del jugador no basta con comparar las cadenas de texto directamente: hay que normalizarlas primero y después reducirlas a su raíz, de modo que variantes como el plural, el género o las mayúsculas/acentos no impidan reconocer una respuesta correcta.

El proceso se hace en dos pasos:

1. **`normalize()`** : limpieza de la cadena: pasa el texto a minúsculas y elimina los acentos/diacríticos usando `unicodedata` (normalización NFD, luego se descartan los caracteres de la categoría `Mn`, es decir las marcas diacríticas). Por ejemplo, `"Île"` se convierte en `"ile"`.

2. **`stemmer_word()`** : aplica un *stemming* (reducción a la raíz de la palabra) sobre el texto ya normalizado, usando `SnowballStemmer` de NLTK. Usamos **tres stemmers distintos**, uno por idioma soportado (`SnowballStemmer("french")`, `SnowballStemmer("spanish")`, `SnowballStemmer("english")`), y se elige el stemmer correspondiente según el idioma de la partida en curso.

Finalmente, **`is_same_word()`** compara el stem de la propuesta del jugador con el stem de la respuesta esperada: si ambos stems coinciden, la respuesta se considera correcta — incluso si difiere en mayúsculas, acentos, singular/plural, o (parcialmente) género.

Ejemplo: si la respuesta esperada es `"chien"`, las propuestas `"Chien"`, `"CHIENS"` o `"chiens "` son todas aceptadas, porque una vez normalizadas y reducidas a su raíz (`stem`) dan el mismo resultado (`"chien"`).

> Nota: se trata de *stemming* (reducción heurística a una raíz aproximada) y no de lematización propiamente dicha (que requeriría un análisis morfológico completo para volver a la forma canónica exacta de la palabra). Elegimos Snowball porque NLTK ofrece una implementación lista para usar en los 3 idiomas del proyecto, lo cual cumple el requisito 4.2 del enunciado ("Lematización y/o stemming").
