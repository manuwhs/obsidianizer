from typing import Any

import contextualSpellCheck
import spacy


def create_contextual_spell_check(language: str = "en") -> Any:
    """Returns contextual spell checker. The attributes are:
    print(doc._.outcome_spellCheck)
    print(doc._.suggestions_spellCheck)
    print(doc._.score_spellCheck)
    """
    nlp = spacy.load(language)
    contextualSpellCheck.add_to_pipe(nlp)
    return nlp
