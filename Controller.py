import streamlit as st
from strsimpy.jaro_winkler import JaroWinkler
from pathlib import Path
import docx
import yaml
import re
import numpy as np
from streamlit_tags import st_tags
from annotated_text import annotated_text
from colorsys import rgb_to_hsv, hsv_to_rgb


colors = 3*['#a1c9f4', '#ffb482', '#8de5a1', '#ff9f9b', '#d0bbff', '#debb9b', '#fab0e4', '#cfcfcf', '#fffea3', '#b9f2f0']


def get_color(score, fixed_color=True):
    if fixed_color: return colors[score.argmax()]
    h = colors[score.argmax()].lstrip("#")

    c = rgb_to_hsv(*tuple(int(h[i:i+2], 16) for i in (0, 2, 4)))
    c = [c[0], c[1], 255-((255 - c[2]) * (score.max()))]
    c = [int(ch) for ch in hsv_to_rgb(*c)]

    return '#%02x%02x%02x' % tuple(c)

with open(Path(__file__).parent / "hotwords.yaml", "r") as f:
    hotwords = yaml.load(f, yaml.SafeLoader)
    abbreviazioni = hotwords["abbreviazioni"]
    preposizioni = hotwords["preposizioni"]

def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return fullText

jr = JaroWinkler()
def similarity(word, w):
    # sym = jr.similarity(word.lower(), w.lower())
    sym = jr.similarity(word.title(), w.title())
    if abs(len(word) - len(w)) > .5*len(word) or len(w) < 3 or w in preposizioni:
        sym = 0
    return sym


def filtered_doc(color_document, w_keys, words):
    for i in range(len(color_document)):
        s = color_document[i]
        if type(s) == tuple:
            if not w_keys[words.index(s[1])]:
                st.write(s)
                color_document[i] = s[1]
    return color_document


def main():
    st.title("Controllo nomi")
    data = st.file_uploader("Carica il file", type=["doc", "docx"])
    document = getText(data)
    
    # words = st.text_input("Parole da controllare",
    #                       help="Inserire tutti gli elementi da controllare, separati da spazio. Poi premere invio.").split()
    words = st_tags(
            label='Parole da controllare:',
            text='Premi invio per inserire',
            suggestions=[],
            )
    words = list(set(words))

    threshold = st.slider("Inserisci la precisione", .5, 1., .75, help="Una precisione maggiore farà trovare meno parole")

    # TODO: implement multiple words control
    # care_spaces = np.array([" " in w for w in words])
    w_keys = np.zeros_like(words)

#    cols = st.columns(len(words)) if len(words) else None
#    for i, word in enumerate(words):
#        cols[i].checkbox(word, value=True, key=w_keys[i],
#                # on_change=st.experimental_rerun()
#                )
    color_document = []
    for paragraph in document:
        paragraph = re.split("\s+|'|’", paragraph)
        last_found = -1
        for i in range(len(paragraph)):
            w = re.sub(r"[^a-zA-Z.\-\d\s:]", "", paragraph[i])

            # if [similarity(word.split()[0], w) for word in words[care_spaces]]

            if len(w) < 1: continue
            if (w[-1] == "." and w.count(".")<=1 and w not in abbreviazioni):
                w = w[:-1]

            score = np.array([similarity(word, w) for word in words])
            if (score > threshold).any() and (score != 1).all():
                sym_word = words[score.argmax()]
                
                color_document.append(" ".join(paragraph[last_found+1:i]))
                color_document.append((w, sym_word, get_color(score)))
                last_found = i

        if last_found != len(paragraph):
            color_document.append(f"{' '.join(paragraph[last_found+1:])}")
        # tmp = filtered_doc(color_document, w_keys, words)
        # annotated_text(*tmp)
        annotated_text(*color_document)
        color_document = []


# if __name__ == "__main__":
main()
