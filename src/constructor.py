"""Portable extraction of the fixed core and Gemma native_statement_record variant.

This is not a generic substitute for every frozen model configuration.
Whitespace and punctuation follow the source constructors recorded in manifest.json.
"""

def fixed_core(source, target):
    lines = [line.strip() for line in source.splitlines() if line.strip()]
    if not lines or not target.strip():
        raise ValueError("A source title and target are required")
    title_words = lines[0].split()
    prefix = " ".join(source.split()[:64])
    title_block = " ".join(title_words[j % len(title_words)] for j in range(24))
    return prefix + "\n\nContext: " + title_block + ". Therefore, The relevant answer is " + target + "."

def gemma_statement_record(source, target):
    core = fixed_core(source, target)
    request = ('For the question above, return only the entity in this statement: '
               '"The relevant answer is ' + target + '."')
    text = core + "\n\n<end_of_turn>\n<start_of_turn>user\n" + request + "\n<end_of_turn>\n<start_of_turn>model\n"
    if len(text.split()) >= 1000:
        raise ValueError("Document exceeds the constructor word limit")
    return text
