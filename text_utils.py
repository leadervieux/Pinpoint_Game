import re
import unicodedata

from nltk.stem.snowball import SnowballStemmer

# Load the French Snowball stemmer from NLTK
stemmer = SnowballStemmer("french")


def strip_accents(text: str) -> str:
  # Quick trick with NFKD to decouple letters and accents, then ditch the marks
  nfkd = unicodedata.normalize("NFKD", text)
  return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalize_text(text: str) -> str:
  # Standard cleanup: lowercase, strip edge spaces, and drop accents
  text = text.lower().strip()
  text = strip_accents(text)

  # Replace punctuation and special characters with a single space
  text = re.sub(r"[^a-z0-9\s]", " ", text)

  # Collapse any consecutive spaces left behind
  text = re.sub(r"\s+", " ", text).strip()
  return text


def stem_word(word: str) -> str:
  # Run the standard stemmer first
  stemmed = stemmer.stem(word)

  # Fallback: manually strip a trailing 's' if the stemmer missed a basic plural
  if stemmed == word and word.endswith("s") and len(word) > 3:
    stemmed = word[:-1]
  return stemmed


def lemmatize_words(text: str) -> str:
  # Tokenize by whitespace, stem each word, and put the sentence back together
  tokens = text.split()
  return " ".join(stem_word(tok) for tok in tokens)


def answers_match(player_answer: str, expected_answer: str) -> bool:
  # Process both strings through the exact same pipeline before comparing
  a = lemmatize_words(normalize_text(player_answer))
  b = lemmatize_words(normalize_text(expected_answer))

  # Make sure we don't accidentally match two empty strings
  return a == b and a != ""