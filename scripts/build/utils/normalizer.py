# ----------------------------
# NORMALIZER
# ----------------------------
def normalize(s):
    return (
        s.lower()
        .strip()
        .replace(" ", "_")
        .replace("á", "a")
        .replace("à", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ç", "c")
    )
