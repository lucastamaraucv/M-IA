"""Aplica mejoras al notebook 14_Natural_Language con bloques de colores y teoria detallada."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _enhance_nb import enhance
from _styles import teoria, tu_turno, solucion_md, dato, aviso

NB = r"C:\Users\Lucas Tamara\Desktop\M IA\Python para la Inteligencia Artificial\01MIAR_ABR26\01MIAR_14_Natural_Language.ipynb"

import json
nb = json.load(open(NB, encoding="utf-8"))


def find_id(text_fragment):
    for c in nb["cells"]:
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        if text_fragment in src:
            return c["id"]
    return None


# Anclas (cell_ids reales del notebook 14)
ID_TITULO         = nb["cells"][0]["id"]                                  # 0  - portada
ID_NLTK           = find_id("## NLTK")                                    # 1
ID_GUTENBERG      = find_id("Corpus Gutenberg")                           # 4
ID_PUNKT          = find_id("Paquete *punkt*")                            # 10
ID_CONCORDANCIA   = find_id("### Concordancia")                           # 14
ID_FREQ           = find_id("### Frecuencia de las palabras")             # 21
ID_PUNTUACION     = find_id("Signos de puntuaci")                         # 23
ID_STOPWORDS      = find_id("Stopwords (preposiciones")                   # 26
ID_SELECCION      = find_id("### Seleccionar palabras")                   # 32
ID_COLOCACIONES   = find_id("### Colocaciones")                           # 35
ID_SINONIMOS      = find_id("Paquete *wordnet*")                          # 38
ID_STEMMING       = find_id("### Stemming y lematizaci")                  # 46
ID_LEMA           = find_id("Buscar el lema de las palabras")             # 49
ID_TEXTO_ONLINE   = find_id("### Texto online")                           # 51
ID_HTML           = find_id("### Extraer texto de HTML")                  # 55
ID_BS4            = find_id("#### Beautiful Soup")                        # 57
ID_SENTIMIENTO    = find_id("### An")                                     # 59  (Analisis de Sentimiento)
ID_ENTRENAMIENTO  = find_id("#### Entrenamiento del modelo")              # 69


plan = []

# -------- INTRO al notebook --------
plan.append((ID_TITULO, [
    {"type": "md", "src": teoria(
        "Como leer este notebook (version mejorada)",
        """Este notebook fue **enriquecido** para ayudarte a aprender escribiendo codigo. Vas a encontrar tres tipos de bloques de colores:

<div style="background-color:#e7f5ff;border-left:6px solid #1c7ed6;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>AZUL = TEORIA</b></div> -> explicacion en palabras simples antes de cada concepto.

<div style="background-color:#fff9db;border-left:6px solid #f59f00;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>AMARILLO = TU TURNO</b></div> -> el ejercicio que TU debes resolver. Hay una celda vacia debajo donde escribes el codigo.

<div style="background-color:#ebfbee;border-left:6px solid #2f9e44;padding:6px 10px;border-radius:4px;margin:4px 0;display:inline-block;"><b>VERDE = SOLUCION</b></div> -> codigo de referencia comentado por si te trabas. Destapa solo despues de intentar.

> **Promesa importante**: el codigo y la teoria del profesor original no se han tocado. Solo se han ANADIDO bloques. Asi puedes seguir comparando con la version original cuando quieras."""
    )},
    {"type": "md", "src": teoria(
        "Que es el Procesamiento de Lenguaje Natural (NLP)?",
        """**NLP** (Natural Language Processing) es la rama de la IA que se ocupa de **convertir texto humano en informacion procesable por una maquina**. Aplicaciones tipicas:

- Buscadores y motores de recomendacion (Google, Amazon).
- Asistentes virtuales (Siri, Alexa).
- Traduccion automatica (DeepL, Google Translate).
- Analisis de sentimiento en redes sociales.
- Chatbots y modelos LLM (GPT, Claude).
- Clasificacion de correos (spam vs no-spam).

#### El gran problema: el texto NO es un dato numerico

Los algoritmos de Machine Learning trabajan con **vectores de numeros**. El texto es una secuencia de caracteres ambigua, irregular y llena de excepciones. Por eso necesitamos un **pipeline** que transforme texto en numeros.

#### El pipeline clasico de NLP (lo que veras en este notebook)

```
TEXTO BRUTO
    |
    v
1) LIMPIEZA  (minusculas, quitar HTML, signos, numeros, urls)
    |
    v
2) TOKENIZACION  (partir en palabras o frases)
    |
    v
3) NORMALIZACION
   - Stopwords (quitar palabras vacias: de, la, el, and, the, ...)
   - Stemming    (reducir a la raiz: corriendo -> corr)
   - Lemmatization (reducir al lema del diccionario: corriendo -> correr)
    |
    v
4) VECTORIZACION  (texto -> numeros)
   - Bag of Words
   - TF-IDF
   - Embeddings (Word2Vec, BERT, ...)
    |
    v
5) MODELO  (clasificacion, clustering, generacion, ...)
```

Cada paso del pipeline aparece en este notebook. Veras la version clasica con **NLTK**. **spaCy** es la alternativa moderna que veremos al final."""
    )},
    {"type": "md", "src": dato(
        """**NLTK vs spaCy** (las dos librerias de NLP en Python que mas se usan):

| Aspecto | **NLTK** | **spaCy** |
|---|---|---|
| Anio nacimiento | 2001 | 2015 |
| Filosofia | Academica, modular, didactica | Industrial, rapida, lista para produccion |
| Velocidad | Lenta | Muy rapida (escrita en Cython) |
| Modelos pre-entrenados | Pocos | Muchos, multi-idioma |
| Tokenizacion espanol | Basica | Excelente |
| Aprender NLP desde 0 | **Recomendada** | Recomendada cuando ya sabes lo que haces |
| Uso en produccion | Raro | Muy comun |

> En este notebook aprenderas con **NLTK** porque te obliga a entender cada paso. En proyectos reales se suele saltar a **spaCy** o a Hugging Face Transformers."""
    )},
]))

# ============ NLTK introduccion ============
plan.append((ID_NLTK, [
    {"type": "md", "src": teoria(
        "NLTK y los corpus",
        """**NLTK** (*Natural Language Toolkit*) es la libreria veterana de NLP en Python. Tres ideas clave para empezar:

#### 1. Corpus

Un **corpus** (plural: corpora) es una **coleccion grande de textos** que sirve para investigar o entrenar modelos. NLTK trae corpus de ejemplo ya empaquetados:

| Corpus | Que contiene |
|---|---|
| `gutenberg` | Libros clasicos de dominio publico (Alicia, Moby Dick, ...) |
| `brown` | Primer corpus etiquetado de ingles americano |
| `reuters` | Noticias clasificadas por categoria |
| `movie_reviews` | Criticas de cine etiquetadas como pos/neg |
| `stopwords` | Listas de palabras vacias en varios idiomas |
| `wordnet` | Diccionario semantico de sinonimos/antonimos |

#### 2. Descargar antes de usar

NLTK descarga los corpus **bajo demanda**:

```python
import nltk
nltk.download('gutenberg')      # un corpus concreto
nltk.download('punkt')          # tokenizador de frases
nltk.download('stopwords')      # listas de stopwords
nltk.download('wordnet')        # wordnet (sinonimos)
nltk.download('all')            # TODO (varios GB, no recomendado)
```

#### 3. Acceder a los textos

```python
nltk.corpus.gutenberg.fileids()                          # lista de archivos
nltk.corpus.gutenberg.words('carroll-alice.txt')         # lista de palabras
nltk.corpus.gutenberg.sents('carroll-alice.txt')         # lista de frases
nltk.corpus.gutenberg.raw('carroll-alice.txt')           # texto crudo
```"""
    )},
]))

# ============ Tokenizacion ============
plan.append((ID_PUNKT, [
    {"type": "md", "src": teoria(
        "Tokenizacion: el primer paso real del pipeline",
        """**Tokenizar** = partir un texto en **unidades minimas** llamadas *tokens*. Normalmente palabras, pero pueden ser frases, sub-palabras o caracteres.

#### Por que no basta con `texto.split()`?

```python
"Hola, mundo! NLP es genial.".split()
# ['Hola,', 'mundo!', 'NLP', 'es', 'genial.']
```

Problemas:
- Pega los signos a la palabra: `'mundo!'` deberia ser `'mundo'` y `'!'`.
- No sabe que `Sr.` o `EE.UU.` no son finales de frase.
- En ingles, `don't` puede dividirse mejor como `do` + `n't`.
- Apostrofes, urls, hashtags, emojis... un lio.

Por eso usamos **tokenizadores especializados**.

#### Tokenizadores en NLTK

```python
from nltk.tokenize import word_tokenize, sent_tokenize

texto = "Hola Sr. Lopez. Bienvenido a NLP! Le va a gustar."

word_tokenize(texto)
# ['Hola', 'Sr.', 'Lopez', '.', 'Bienvenido', 'a', 'NLP', '!', 'Le', 'va', 'a', 'gustar', '.']

sent_tokenize(texto)
# ['Hola Sr. Lopez.', 'Bienvenido a NLP!', 'Le va a gustar.']
```

`punkt` es el modelo no supervisado entrenado para detectar fronteras de frase y palabra. Por eso hay que descargarlo (`nltk.download('punkt')`).

#### Tokenizar palabras vs tokenizar frases

| Tipo | Que devuelve | Cuando usar |
|---|---|---|
| `word_tokenize(texto)` | lista de palabras | Bag of Words, TF-IDF, frecuencias |
| `sent_tokenize(texto)` | lista de frases | Resumenes, analisis por frase |

#### Niveles de tokenizacion (modernos)

| Nivel | Ejemplo de "running" | Donde se usa |
|---|---|---|
| Palabra | `["running"]` | NLTK clasico |
| Subpalabra (BPE) | `["run", "##ning"]` | BERT, GPT |
| Caracter | `["r","u","n","n","i","n","g"]` | RNN antiguas |
| Byte | bytes UTF-8 | Algunos LLMs recientes |"""
    )},
    {"type": "md", "src": tu_turno(1,
        """Toma este texto en espanol:

```python
texto = "El Sr. Garcia compro 3 libros. Los leyo todos en una semana!"
```

1. Tokenizalo en **palabras** con `nltk.word_tokenize(texto)` y muestra el resultado.
2. Tokenizalo en **frases** con `nltk.sent_tokenize(texto)` y muestra el resultado.
3. Compara cuantos tokens hay en cada caso (`len`).

> Recuerda descargar `punkt` antes con `nltk.download('punkt')`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nimport nltk\n# nltk.download('punkt')\ntexto = \"El Sr. Garcia compro 3 libros. Los leyo todos en una semana!\"\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import nltk\n# # nltk.download('punkt')   # descarga necesaria la primera vez\n#\n# texto = \"El Sr. Garcia compro 3 libros. Los leyo todos en una semana!\"\n#\n# # 1) Tokenizar en palabras: parte el texto en unidades de palabra/signo\n# palabras = nltk.word_tokenize(texto)\n# print('Palabras:', palabras)\n# print('Numero de tokens-palabra:', len(palabras))\n#\n# # 2) Tokenizar en frases: detecta los puntos, signos de fin de frase\n# frases = nltk.sent_tokenize(texto)\n# print('Frases:', frases)\n# print('Numero de frases:', len(frases))\n#\n# # 3) Notese como word_tokenize separa el punto de 'libros' o 'semana'\n# #    pero MANTIENE 'Sr.' como un solo token (gracias al modelo punkt)\n"},
]))

# ============ Concordancia ============
plan.append((ID_CONCORDANCIA, [
    {"type": "md", "src": teoria(
        "Concordancia y exploracion del texto",
        """Antes de aplicar modelos, conviene **explorar** el texto. NLTK tiene la clase `nltk.Text` que ofrece herramientas rapidas para inspeccionar un corpus:

| Metodo | Que hace |
|---|---|
| `text.concordance(palabra)` | Muestra cada aparicion de la palabra con su contexto (linea de la izquierda y derecha). |
| `text.common_contexts([w1, w2])` | Contextos en que aparecen DOS palabras (palabra anterior y posterior). Util para detectar sinonimos. |
| `text.similar(palabra)` | Busca palabras que aparecen en contextos parecidos (sinonimos potenciales). |
| `text.dispersion_plot([w1, w2])` | Grafica donde aparece cada palabra a lo largo del texto. |
| `text.collocations()` | Imprime bigramas que coocurren mas de lo esperado. |

```python
alice_t = nltk.Text(alice)        # alice es una lista de palabras
alice_t.concordance('hatter')     # muestra contextos de la palabra
alice_t.similar('hatter')         # palabras con contexto similar
```

> Estas herramientas se llaman **estadistica descriptiva del texto**: no construyen un modelo, solo te ayudan a entender el corpus que tienes en las manos."""
    )},
]))

# ============ Frecuencia ============
plan.append((ID_FREQ, [
    {"type": "md", "src": teoria(
        "FreqDist: contar palabras",
        """`nltk.FreqDist` cuenta cuantas veces aparece cada token en una lista. Es una version especializada de `collections.Counter`.

```python
fd = nltk.FreqDist(lista_de_palabras)

fd['the']             # cuantas veces aparece 'the'
fd.most_common(10)    # top 10 mas frecuentes
fd.N()                # total de tokens
fd.B()                # numero de palabras distintas (vocabulario)
fd.hapaxes()          # palabras que aparecen una sola vez
fd.plot(20)            # grafica de las 20 mas frecuentes
```

#### Por que las palabras mas frecuentes son tan poco utiles?

Si haces `fd.most_common(10)` sobre un texto en ingles, casi seguro veras: `the`, `,`, `.`, `and`, `to`, `of`, `a`, ... Estas palabras son **stopwords**: aparecen en todos los textos, no aportan informacion sobre el TEMA. Por eso el siguiente paso del pipeline es **filtrarlas**."""
    )},
]))

# ============ Limpieza puntuacion + stopwords ============
plan.append((ID_PUNTUACION, [
    {"type": "md", "src": teoria(
        "Limpieza del texto: por que y como",
        """Antes de cualquier analisis serio, **limpiamos** el texto. La limpieza tipica incluye:

| Paso | Que hace | Codigo Python tipico |
|---|---|---|
| Minusculas | `Hola` y `hola` deben contar igual | `texto.lower()` |
| Quitar HTML | quitar `<p>`, `&nbsp;`, etc. | `BeautifulSoup(texto).get_text()` |
| Quitar URLs | quitar `http://...` | regex `r'https?://\\S+'` |
| Quitar signos | `.,;:!?\"'` | `string.punctuation` o regex |
| Quitar numeros | `2023`, `42` | regex `r'\\d+'` (depende del caso) |
| Quitar espacios extra | `'  hola   mundo'` -> `'hola mundo'` | `' '.join(texto.split())` |
| Quitar stopwords | `de, la, el, the, and, ...` | listas precargadas |

#### Filtrar puntuacion en Python

```python
import string
print(string.punctuation)
# !"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~

punctuation = set(string.punctuation)
limpio = [w for w in tokens if w not in punctuation]
```

#### Cuidado: NO siempre hay que limpiar TODO

| Tarea | Conviene...|
|---|---|
| Bag of Words / TF-IDF | Limpiar mucho (minusculas, sin signos, sin stopwords). |
| Analisis de sentimiento | NO quitar `!` ni `?` (son senal de emocion). |
| NER (entidades nombradas) | NO pasar a minusculas (las mayusculas son pista). |
| Modelos modernos (BERT) | Casi nada: el modelo aprende del texto crudo. |

La limpieza es una **decision de diseno**: depende de la tarea."""
    )},
]))

plan.append((ID_STOPWORDS, [
    {"type": "md", "src": teoria(
        "Stopwords: las palabras 'vacias'",
        """Las **stopwords** son palabras muy frecuentes que aparecen en cualquier texto y por eso aportan poco a la hora de **distinguir un texto de otro**. Ejemplos:

- Espanol: `de, la, el, los, las, y, o, en, a, un, una, que, es, ...`
- Ingles: `the, a, an, of, and, or, to, in, is, that, this, ...`

NLTK trae listas para muchos idiomas:

```python
from nltk.corpus import stopwords
sw_es = set(stopwords.words('spanish'))    # ~313 palabras
sw_en = set(stopwords.words('english'))    # ~179 palabras
```

#### Como filtrarlas

```python
tokens_limpios = [w for w in tokens if w.lower() not in sw_es]
```

#### Cuando NO quitar stopwords?

| Caso | Por que conservarlas |
|---|---|
| Analisis de sentimiento | `not good` cambia el significado completo. |
| Generacion de texto | Quitarlas rompe la gramatica. |
| Modelos pre-entrenados (BERT) | El modelo ya aprendio a manejarlas. |
| Deteccion de autoria / estilo | El estilo de un autor incluye las stopwords. |

#### Cuidado con los acentos

Las stopwords NLTK en espanol vienen sin acentos en algunos casos. Si tu texto SI los tiene, puede que filtres mal. Trucos:

```python
import unicodedata
def quitar_acentos(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
```"""
    )},
    {"type": "md", "src": tu_turno(2,
        """Tienes esta lista de tokens (ya tokenizados) en ingles, mezclados con signos:

```python
tokens = ['The', 'cat', 'sat', 'on', 'the', 'mat', '!', 'It', 'was', 'a', 'sunny', 'day', '.']
```

1. Pasa todos los tokens a **minusculas**.
2. Quita los **signos de puntuacion** usando `string.punctuation`.
3. Quita las **stopwords** en ingles (`stopwords.words('english')`).
4. Imprime la lista resultante.

> Resultado esperado parecido a: `['cat', 'sat', 'mat', 'sunny', 'day']`"""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nimport nltk, string\n# nltk.download('stopwords')\nfrom nltk.corpus import stopwords\n\ntokens = ['The', 'cat', 'sat', 'on', 'the', 'mat', '!', 'It', 'was', 'a', 'sunny', 'day', '.']\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import nltk, string\n# # nltk.download('stopwords')   # primera vez\n# from nltk.corpus import stopwords\n#\n# tokens = ['The', 'cat', 'sat', 'on', 'the', 'mat', '!', 'It', 'was', 'a', 'sunny', 'day', '.']\n#\n# # 1) Pasamos todo a minusculas para que 'The' y 'the' cuenten igual\n# tokens_lower = [t.lower() for t in tokens]\n#\n# # 2) Quitamos signos de puntuacion (string.punctuation -> '!\"#$%&...')\n# punct = set(string.punctuation)\n# sin_signos = [t for t in tokens_lower if t not in punct]\n#\n# # 3) Quitamos stopwords en ingles\n# sw_en = set(stopwords.words('english'))\n# limpio = [t for t in sin_signos if t not in sw_en]\n#\n# print(limpio)\n# # ['cat', 'sat', 'mat', 'sunny', 'day']\n"},
]))

# ============ Seleccionar palabras ============
plan.append((ID_SELECCION, [
    {"type": "md", "src": teoria(
        "Filtros utiles con list comprehensions",
        """Una vez tienes la lista de tokens, puedes filtrarla con condiciones tipicas:

```python
# Palabras largas (mas de N caracteres)
[w for w in alice if len(w) > 12]

# Palabras que terminan en algo
[w for w in alice if w.endswith('ious')]

# Palabras que empiezan por algo
[w for w in alice if w.startswith('un')]

# Solo alfabeticas (sin numeros ni signos)
[w for w in alice if w.isalpha()]

# Solo titulo (primera mayuscula)
[w for w in alice if w.istitle()]

# Quitar duplicados conservando el conjunto
sorted(set(alice))
```

Esto es solo Python plano (lo que ya viste en clases anteriores). NLP en NLTK consiste **mucho** en saber filtrar listas con `list comprehensions`."""
    )},
]))

# ============ N-gramas ============
plan.append((ID_COLOCACIONES, [
    {"type": "md", "src": teoria(
        "N-gramas: ventanas deslizantes de palabras",
        """Un **n-grama** es una secuencia contigua de **n tokens** dentro de un texto.

| n | Nombre | Ejemplo en "el gato negro come pescado" |
|---|---|---|
| 1 | unigrama | `el`, `gato`, `negro`, `come`, `pescado` |
| 2 | bigrama | `(el, gato)`, `(gato, negro)`, `(negro, come)`, `(come, pescado)` |
| 3 | trigrama | `(el, gato, negro)`, `(gato, negro, come)`, `(negro, come, pescado)` |
| n | n-grama | secuencia de n palabras consecutivas |

#### Para que sirven?

1. **Contexto**: las unigramas pierden orden. Bigramas y trigramas conservan algo de contexto local.
2. **Colocaciones**: pares de palabras que aparecen juntas mas de lo esperado: `New York`, `buenos dias`, `inteligencia artificial`. Detectarlas mejora la calidad del modelo.
3. **Modelos de lenguaje clasicos**: predecir la siguiente palabra a partir de las n-1 anteriores (antes de los Transformers).
4. **TF-IDF avanzado**: vectorizar usando bigramas/trigramas en lugar de solo palabras sueltas.

#### En NLTK

```python
list(nltk.bigrams(['el','gato','negro','come']))
# [('el','gato'), ('gato','negro'), ('negro','come')]

list(nltk.trigrams(['el','gato','negro','come']))
# [('el','gato','negro'), ('gato','negro','come')]

list(nltk.ngrams(['a','b','c','d'], n=4))
# [('a','b','c','d')]

# Frecuencia de bigramas
nltk.FreqDist(nltk.bigrams(tokens)).most_common(5)
```

#### Trade-off de elegir n

- **n pequeno (1-2)**: vocabulario pequeno, mucho recuento, generaliza bien.
- **n grande (3+)**: muchos n-gramas posibles, la mayoria con cuenta 0 o 1 (esparsidad). Necesitas MUCHO texto."""
    )},
    {"type": "md", "src": tu_turno(3,
        """Tienes esta frase ya tokenizada:

```python
tokens = ['en', 'un', 'lugar', 'de', 'la', 'mancha', 'de', 'cuyo', 'nombre',
          'no', 'quiero', 'acordarme']
```

1. Genera **todos los bigramas** con `nltk.bigrams(tokens)` y muestralos en una lista.
2. Genera **todos los trigramas** con `nltk.trigrams(tokens)`.
3. Calcula la **frecuencia de los bigramas** con `FreqDist` y muestra los **3 mas comunes** (pista: hay un bigrama repetido).

> Recuerda envolver `nltk.bigrams(...)` en `list(...)` para verlo, porque devuelve un iterador."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nimport nltk\n\ntokens = ['en', 'un', 'lugar', 'de', 'la', 'mancha', 'de', 'cuyo', 'nombre',\n          'no', 'quiero', 'acordarme']\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import nltk\n#\n# tokens = ['en', 'un', 'lugar', 'de', 'la', 'mancha', 'de', 'cuyo', 'nombre',\n#           'no', 'quiero', 'acordarme']\n#\n# # 1) Bigramas: pares de palabras consecutivas. Hay len(tokens)-1 bigramas.\n# bigramas = list(nltk.bigrams(tokens))\n# print('Bigramas:', bigramas)\n# print('Total:', len(bigramas))\n#\n# # 2) Trigramas: triples de palabras consecutivas. Hay len(tokens)-2.\n# trigramas = list(nltk.trigrams(tokens))\n# print('Trigramas:', trigramas)\n#\n# # 3) Frecuencia de bigramas. ('de','la') o ('de','cuyo') aparecen.\n# fd = nltk.FreqDist(bigramas)\n# print('Top 3:', fd.most_common(3))\n"},
]))

# ============ Wordnet ============
plan.append((ID_SINONIMOS, [
    {"type": "md", "src": teoria(
        "WordNet: el diccionario semantico",
        """**WordNet** es una base de datos lexica que agrupa palabras con significados parecidos en **synsets** (conjuntos de sinonimos). Para cada synset puedes obtener:

- **Definicion** (`syn.definition()`).
- **Ejemplos de uso** (`syn.examples()`).
- **Lemas / sinonimos** (`syn.lemmas()`).
- **Antonimos** (`lemma.antonyms()`).
- **Relaciones**: hiperonimo (genero superior), hiponimo (genero inferior), meronimo (parte de), etc.

```python
from nltk.corpus import wordnet
syns = wordnet.synsets('car')
syns[0].definition()        # 'a motor vehicle with four wheels'
syns[0].lemma_names()       # ['car', 'auto', 'automobile', 'machine', ...]
syns[0].hypernyms()         # [Synset('motor_vehicle.n.01')]
```

#### Por que importa para NLP?

WordNet permite **expansion semantica**: si buscas `car`, tambien quieres encontrar textos que digan `auto` o `automobile`. Sin WordNet, dos palabras sinonimas son tokens distintos sin relacion.

> Nota: en la era de los **embeddings** (Word2Vec, GloVe, BERT) WordNet ha perdido peso, porque los embeddings aprenden la similitud automaticamente desde grandes corpus. Pero WordNet sigue siendo util para datos pequenos y para tareas donde queremos **reglas explicitas**."""
    )},
]))

# ============ Stemming + Lemmatization ============
plan.append((ID_STEMMING, [
    {"type": "md", "src": teoria(
        "Stemming vs Lemmatization: la diferencia clave",
        """Despues de tokenizar y limpiar, queremos que palabras como **correr, corriendo, corro, corres** se traten **igual**, porque comparten significado. Hay dos formas:

#### Stemming = "podar" la palabra

Aplica reglas heuristicas para **cortar sufijos**. El resultado puede no ser una palabra real del idioma.

```python
from nltk.stem import PorterStemmer
ps = PorterStemmer()
ps.stem('running')     # 'run'
ps.stem('runs')        # 'run'
ps.stem('easily')      # 'easili'   <- ojo, no es palabra real
ps.stem('flies')       # 'fli'      <- otra rara
```

Stemmers populares en NLTK:
- `PorterStemmer` (ingles, clasico, agresivo).
- `LancasterStemmer` (ingles, MUY agresivo).
- `SnowballStemmer('spanish')` (multi-idioma, mejor para espanol).

#### Lemmatization = ir al **lema** del diccionario

Devuelve la **forma de diccionario** (infinitivo de un verbo, singular masculino de un sustantivo, ...). Necesita conocer la categoria gramatical (POS):

```python
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()
wnl.lemmatize('running', pos='v')   # 'run'    (verbo)
wnl.lemmatize('better', pos='a')    # 'good'   (adjetivo)
wnl.lemmatize('mice')               # 'mouse'
wnl.lemmatize('feet')               # 'foot'
```

#### Tabla comparativa

| Aspecto | Stemming | Lemmatization |
|---|---|---|
| Velocidad | Muy rapido | Mas lento |
| Resultado | Puede no ser palabra real | Siempre palabra real |
| Necesita POS? | No | Si (para resultados buenos) |
| Calidad | Aproximada | Mas precisa |
| Idiomas soportados (NLTK) | Muchos | Sobre todo ingles (`WordNetLemmatizer`) |
| Uso tipico | Buscadores, recuperacion de informacion | Analisis linguistico, chatbots |

> **Regla practica**: si solo te importa **agrupar variantes** (buscador, TF-IDF), un stemmer basta. Si te importa **el significado preciso**, usa lematizacion (mejor con spaCy en idiomas distintos al ingles)."""
    )},
    {"type": "md", "src": tu_turno(4,
        """Aplica stemming a estas palabras en ingles con `PorterStemmer`:

```python
palabras_en = ['running', 'runs', 'ran', 'easily', 'fairly', 'studies', 'studying']
```

Y a estas palabras en espanol con `SnowballStemmer('spanish')`:

```python
palabras_es = ['corriendo', 'corro', 'corres', 'amigos', 'amigas', 'rapidamente']
```

Imprime para cada palabra: `palabra -> raiz`.

> Veras que algunas raices son raras (ej: `easili`, `fairli`). Esto es normal en stemming."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nfrom nltk.stem import PorterStemmer, SnowballStemmer\n\npalabras_en = ['running', 'runs', 'ran', 'easily', 'fairly', 'studies', 'studying']\npalabras_es = ['corriendo', 'corro', 'corres', 'amigos', 'amigas', 'rapidamente']\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# from nltk.stem import PorterStemmer, SnowballStemmer\n#\n# # PorterStemmer es el stemmer clasico de ingles\n# ps = PorterStemmer()\n# # SnowballStemmer es multi-idioma. Lo creamos para espanol.\n# ss = SnowballStemmer('spanish')\n#\n# palabras_en = ['running', 'runs', 'ran', 'easily', 'fairly', 'studies', 'studying']\n# palabras_es = ['corriendo', 'corro', 'corres', 'amigos', 'amigas', 'rapidamente']\n#\n# print('--- Ingles (Porter) ---')\n# for w in palabras_en:\n#     print(f'{w} -> {ps.stem(w)}')\n#\n# print('--- Espanol (Snowball) ---')\n# for w in palabras_es:\n#     print(f'{w} -> {ss.stem(w)}')\n#\n# # Notese:\n# #   running -> run, runs -> run, pero ran -> ran (Porter no detecta verbos irregulares)\n# #   easily -> easili (raiz no real, pero CONSISTENTE)\n# #   amigos / amigas -> amig (mismas formas reducidas)\n"},
]))

plan.append((ID_LEMA, [
    {"type": "md", "src": tu_turno(5,
        """Compara stemming y lemmatization sobre la **misma** lista de palabras en ingles:

```python
palabras = ['running', 'runs', 'better', 'mice', 'studies', 'wolves']
```

Para cada palabra imprime una linea con tres columnas: `palabra`, `Porter.stem(palabra)`, `WordNetLemmatizer.lemmatize(palabra)`.

**Bonus:** repite la lematizacion pasando `pos='v'` (verbo) para `running` y `studies`. Veras que cambia el resultado.

> Recuerda: para `WordNetLemmatizer` debes haber descargado wordnet (`nltk.download('wordnet')`)."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nimport nltk\n# nltk.download('wordnet')\nfrom nltk.stem import PorterStemmer, WordNetLemmatizer\n\npalabras = ['running', 'runs', 'better', 'mice', 'studies', 'wolves']\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import nltk\n# # nltk.download('wordnet')\n# from nltk.stem import PorterStemmer, WordNetLemmatizer\n#\n# ps = PorterStemmer()           # stemmer (corta sufijos)\n# wnl = WordNetLemmatizer()       # lematizador (usa wordnet)\n#\n# palabras = ['running', 'runs', 'better', 'mice', 'studies', 'wolves']\n#\n# # Cabecera\n# print(f'{\"palabra\":<12}{\"stem\":<12}{\"lemma\":<12}')\n# print('-' * 36)\n# for w in palabras:\n#     stem = ps.stem(w)               # raiz heuristica\n#     lemma = wnl.lemmatize(w)        # por defecto pos='n' (sustantivo)\n#     print(f'{w:<12}{stem:<12}{lemma:<12}')\n#\n# # Bonus: lematizando como verbos\n# print()\n# print('Como VERBOS:')\n# print('running ->', wnl.lemmatize('running', pos='v'))   # run\n# print('studies ->', wnl.lemmatize('studies', pos='v'))    # study\n#\n# # OBSERVACION:\n# #  - mice -> mouse: lemmatization conoce el plural irregular. Stemming, no.\n# #  - better -> better (pos='n') o good (pos='a'). Stemming siempre 'better'.\n# #  - Lemmatization es mas precisa pero necesita la pista 'pos' para verbos/adj.\n"},
]))

# ============ Texto online + BoW + TF-IDF ============
plan.append((ID_TEXTO_ONLINE, [
    {"type": "md", "src": teoria(
        "Bag of Words y TF-IDF: convertir texto en numeros",
        """Hasta ahora tenemos **listas de tokens limpios**. Para alimentar un modelo de Machine Learning necesitamos **vectores numericos**. Las dos tecnicas clasicas:

#### 1. Bag of Words (BoW): contar palabras

Cada documento se representa como un **vector de cuentas**: cuantas veces aparece cada palabra del vocabulario.

```
Documento 1: "el gato come pescado"
Documento 2: "el perro come carne"

Vocabulario: [el, gato, perro, come, pescado, carne]

Doc1 -> [1, 1, 0, 1, 1, 0]
Doc2 -> [1, 0, 1, 1, 0, 1]
```

Caracteristicas:
- **Ignora el orden** (por eso "bolsa": como si volcaras las palabras y contaras sin mirar el orden).
- Vocabulario fijo: si aparece una palabra nueva, hay que reentrenar.
- Vectores **muy esparsos** (la mayoria de ceros).

#### 2. TF-IDF: contar **ponderando** por rareza

BoW da el mismo peso a "the" que a "leukemia". TF-IDF arregla esto multiplicando dos factores:

```
TF-IDF(palabra, doc) = TF(palabra, doc) * IDF(palabra)

TF  = frecuencia de la palabra en ESE documento
IDF = log(N / df)
      donde N = total documentos
            df = documentos en los que aparece la palabra
```

Resultado:
- Una palabra que aparece en TODOS los documentos -> IDF cercano a 0 -> peso bajo.
- Una palabra que aparece solo en un par de documentos -> IDF alto -> peso alto.

Asi, **TF-IDF da mas peso a las palabras "discriminativas"**, que distinguen unos documentos de otros.

#### En sklearn (la libreria que se suele usar)

```python
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

textos = ["el gato come pescado", "el perro come carne"]

# Bag of Words
cv = CountVectorizer()
X = cv.fit_transform(textos)
print(cv.get_feature_names_out())   # ['carne','come','el','gato','pescado','perro']
print(X.toarray())

# TF-IDF
tv = TfidfVectorizer()
X = tv.fit_transform(textos)
print(X.toarray())
```

| Parametro util | Que hace |
|---|---|
| `lowercase=True` | minusculas automaticas |
| `stop_words='english'` | aplica stopwords del idioma |
| `ngram_range=(1,2)` | usa unigramas Y bigramas |
| `max_df=0.95` | ignora palabras en >95% de los docs |
| `min_df=2` | ignora palabras en <2 docs |
| `max_features=10000` | limita el vocabulario |

#### Limitaciones (porque existen los embeddings)

- Sigue ignorando el orden.
- No detecta sinonimos: `coche` y `auto` son tokens distintos.
- Dimension explota con vocabularios grandes.

Por eso desde 2013 se popularizaron **Word2Vec, GloVe, fastText** y desde 2018 los **embeddings contextuales (BERT, GPT)**, que aprenden una representacion **densa y semantica** de cada palabra. Pero para tareas pequenas y como baseline, TF-IDF sigue siendo competitivo y rapidisimo."""
    )},
]))

# ============ Beautiful Soup ============
plan.append((ID_BS4, [
    {"type": "md", "src": dato(
        """**BeautifulSoup** es la libreria estandar para extraer texto de HTML. Tiene un parser que entiende las etiquetas y separa el contenido visible.

```python
from bs4 import BeautifulSoup
texto = BeautifulSoup(html, "html.parser").get_text()
```

Otras funciones utiles para limpiar texto online (web scraping):

- `re.sub(r'<[^>]+>', '', texto)` - quita etiquetas con regex (fragil, mejor BS4).
- `re.sub(r'https?://\\S+', '', texto)` - quita URLs.
- `re.sub(r'\\s+', ' ', texto)` - colapsa espacios multiples y saltos de linea.
- `texto.strip()` - quita espacios de los extremos.

Pipeline tipico de preprocesado de una pagina web:

```
HTML crudo
  -> BeautifulSoup.get_text()
  -> minusculas
  -> regex para urls / numeros / emails
  -> word_tokenize
  -> filtrar stopwords + signos
  -> stemming/lemmatization
  -> TF-IDF
```"""
    )},
]))

# ============ Sentimiento + ejercicio integrador ============
plan.append((ID_SENTIMIENTO, [
    {"type": "md", "src": teoria(
        "Analisis de sentimiento: clasificar texto",
        """**Analisis de sentimiento** = decidir si un texto expresa una **opinion positiva, negativa o neutra**. Es un **problema de clasificacion**.

#### Pipeline tipico (lo que hace el resto del notebook)

1. Recoger un corpus etiquetado (`movie_reviews` ya tiene cada critica como `pos` o `neg`).
2. Tokenizar y limpiar.
3. **Vectorizar** los textos: en este notebook con un truco simple (vector binario de presencia de las 2000 palabras mas frecuentes).
4. Entrenar un clasificador (Naive Bayes en este caso).
5. Evaluar con un conjunto de test.

#### Naive Bayes para texto

Naive Bayes asume que cada palabra contribuye **de forma independiente** a la probabilidad de la clase. Es naive (ingenuo) porque obviamente las palabras NO son independientes en un texto, pero funciona muy bien para clasificacion de texto y es **rapido**.

```
P(positivo | texto) ~ P(positivo) * PRODUCTO_de P(palabra_i | positivo)
```

#### Alternativas modernas

- **Regresion logistica** sobre TF-IDF (suele superar a Naive Bayes).
- **SVM lineal** (clasico fuerte para clasificacion de texto).
- **LSTM/CNN** sobre embeddings.
- **BERT fine-tuned**: estado del arte para sentimiento desde 2018."""
    )},
]))

plan.append((ID_ENTRENAMIENTO, [
    {"type": "md", "src": tu_turno(6,
        """**Ejercicio integrador**: vas a aplicar el pipeline COMPLETO sobre un mini-corpus de 4 textos.

```python
textos = [
    "I love this movie, it was fantastic and exciting!",
    "Worst film ever. I hated every minute, boring and slow.",
    "An amazing experience. The acting was great and the story was lovely.",
    "Terrible. Bad acting, awful story, total waste of time."
]
```

Pasos a hacer:

1. **Tokenizar** cada texto con `word_tokenize` (en minusculas).
2. **Filtrar** signos de puntuacion (`string.punctuation`) y **stopwords en ingles**.
3. **Lematizar** cada token con `WordNetLemmatizer()`.
4. Reconstruir cada texto como un string limpio (`' '.join(...)`).
5. Aplicar `TfidfVectorizer` de sklearn a los 4 textos limpios.
6. Imprimir:
   - El **vocabulario** (`get_feature_names_out()`).
   - La **matriz TF-IDF** como array (`X.toarray()`).
   - La **forma** de la matriz (`X.shape`): debe ser (4, vocab_size).

> Pista: importa `from sklearn.feature_extraction.text import TfidfVectorizer`."""
    )},
    {"type": "code", "src": "# Escribe aqui tu codigo:\nimport nltk, string\n# nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')\nfrom nltk.tokenize import word_tokenize\nfrom nltk.corpus import stopwords\nfrom nltk.stem import WordNetLemmatizer\nfrom sklearn.feature_extraction.text import TfidfVectorizer\n\ntextos = [\n    \"I love this movie, it was fantastic and exciting!\",\n    \"Worst film ever. I hated every minute, boring and slow.\",\n    \"An amazing experience. The acting was great and the story was lovely.\",\n    \"Terrible. Bad acting, awful story, total waste of time.\"\n]\n\n"},
    {"type": "code", "src": "# === Solucion sugerida ===\n# import nltk, string\n# # nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')\n# from nltk.tokenize import word_tokenize\n# from nltk.corpus import stopwords\n# from nltk.stem import WordNetLemmatizer\n# from sklearn.feature_extraction.text import TfidfVectorizer\n#\n# textos = [\n#     \"I love this movie, it was fantastic and exciting!\",\n#     \"Worst film ever. I hated every minute, boring and slow.\",\n#     \"An amazing experience. The acting was great and the story was lovely.\",\n#     \"Terrible. Bad acting, awful story, total waste of time.\"\n# ]\n#\n# # 1) Recursos para la limpieza\n# punct = set(string.punctuation)                 # signos de puntuacion\n# sw_en = set(stopwords.words('english'))         # stopwords ingles\n# wnl = WordNetLemmatizer()                       # lematizador\n#\n# # 2) Pipeline de limpieza por texto\n# def limpiar(t):\n#     # 2.1) tokenizar en minusculas\n#     tokens = word_tokenize(t.lower())\n#     # 2.2) quitar signos de puntuacion\n#     tokens = [w for w in tokens if w not in punct]\n#     # 2.3) quitar stopwords\n#     tokens = [w for w in tokens if w not in sw_en]\n#     # 2.4) lematizar (por defecto sustantivo; podriamos pasar pos='v' para verbos)\n#     tokens = [wnl.lemmatize(w) for w in tokens]\n#     return ' '.join(tokens)\n#\n# textos_limpios = [limpiar(t) for t in textos]\n# print('Textos limpios:')\n# for t in textos_limpios:\n#     print(' -', t)\n#\n# # 3) Vectorizamos con TF-IDF\n# vec = TfidfVectorizer()\n# X = vec.fit_transform(textos_limpios)\n#\n# print('\\nVocabulario:', vec.get_feature_names_out())\n# print('\\nForma de la matriz:', X.shape)        # (4 docs, N palabras)\n# print('\\nMatriz TF-IDF (densa):')\n# print(X.toarray().round(3))\n#\n# # NOTAS:\n# #  - Cada fila es un texto, cada columna una palabra del vocabulario.\n# #  - Las palabras que aparecen en muchos textos pesan menos (IDF bajo).\n# #  - Si hubieramos usado CountVectorizer en lugar de TfidfVectorizer,\n# #    veriamos cuentas enteras (Bag of Words puro).\n"},
    {"type": "md", "src": teoria(
        "Y ahora? spaCy, embeddings y modelos modernos",
        """Ya conoces el **pipeline clasico de NLP** con NLTK:

```
texto -> tokenize -> stopwords -> stem/lemma -> n-gramas -> BoW / TF-IDF -> modelo
```

Para ir mas alla:

#### spaCy: la alternativa industrial

```python
# pip install spacy
# python -m spacy download es_core_news_sm
import spacy
nlp = spacy.load('es_core_news_sm')
doc = nlp("Manuel vive en Madrid y trabaja en Telefonica.")

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.is_stop)

# Entidades nombradas (NER) gratis
for ent in doc.ents:
    print(ent.text, ent.label_)   # 'Manuel' PER, 'Madrid' LOC, 'Telefonica' ORG
```

spaCy hace en una sola llamada: tokenize + lemma + POS + NER + dependencias. Y es **mucho mas rapido** que NLTK.

#### Word Embeddings (Word2Vec, GloVe, fastText)

Cada palabra se convierte en un vector denso de 100-300 dimensiones que captura **significado**:

```
vector(rey) - vector(hombre) + vector(mujer) ~ vector(reina)
```

#### Transformers (BERT, GPT, ...) -- estado del arte

Modelos pre-entrenados con miles de millones de palabras. Generan **embeddings contextuales**: el vector de "banco" cambia segun el contexto (banco de plaza vs banco financiero). Se usan via **Hugging Face Transformers**.

```python
# pip install transformers
from transformers import pipeline
clf = pipeline("sentiment-analysis")
clf("I love NLP!")
# [{'label': 'POSITIVE', 'score': 0.9998}]
```

> En la practica industrial actual, casi nadie escribe TF-IDF + Naive Bayes desde cero. Pero conocer el pipeline clasico te permite **entender que esta haciendo** un modelo moderno y **debuguearlo** cuando falla."""
    )},
]))


enhance(NB, plan)
print("Done.")
