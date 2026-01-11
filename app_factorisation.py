import streamlit as st
import random
import sympy as sp
import re
import random
import math
from datetime import datetime
import pandas as pd

### Score sur 8 ou 10 questions, et faire en sorte d'éviter d'avoir plusieurs fois 
### le même type de questions (du style A^2 - B^2 trois fois de suite...) 
### ==> limiter l'usage de "random" en sauvegardant les valeurs précédentes, ou alors en imposant un choix, cf app_fractions.py : ops = ["*", "*", ":", ":"] + random.choices(["+", "-"], k = NB_QUESTIONS - 4) 

### Problème : (w^2(4w-5) - 3(4w-5))*2/2 est accepté comme bonne réponse ...
        ###    factors_user [w**2*(4*w - 1*5) - 3*(4*w - 1*5), 2]   true_factors [4*w - 5, w**2 - 3]


# Initialisation
x = sp.symbols("x")
y = sp.symbols("y")
z = sp.symbols("z")
w = sp.symbols("w")
t = sp.symbols("t")
u = sp.symbols("u")

st.set_page_config(page_title="Factorisation", page_icon="")
#st.subheader("")
st.markdown(
    "<div style='text-align: center; font-size: 24px; font-weight: bold; color: DarkOrange;'>"
    "Entraînement à la factorisation !"
    "</div>",
    unsafe_allow_html=True
)


if "tentatives" not in st.session_state:
    st.session_state["tentatives"] = 0

# # Choix du degré
# degre = st.radio(
#     "Choisissez le degré du polynôme :",
#     [2, 3],
#     horizontal=True
# )



# --- Niveaux disponibles ---
NIVEAUX = {
    "1 — Mise en évidence":1,
    "2 — Méthode somme-produit":2,
    "3 — Identités remarquables de degré 2":3,
    "4 — Identités remarquables de degré 3":4,
    "5 — Méthode des groupements":5,
    "6 — Factorisation par la formule du discriminant":6,
    "7 — Mélange (niveau facile)":7, #uniquement 1,2,3,5
    "8 — Mélange (niveau moyen)":8,      #uniquement 1,2,3,5  mais non-unitaire
    "9 — Mélange (niveau difficile)":9
}




# Génération du polynôme factorisable
def generer_polynome(niveau):
    L = [x, y, z, t, w]
    X = random.choice(L)
    a = 0; r1 = 0; r2 = 0
    if niveau == 1:#"1 — Mise en évidence":
        while r1 == 0 or a == 0:
            a  = random.randint(-5, 5)
            d  = random.randint(1, 8)
            r1 = random.randint(-5, 5)
            e  = random.randint(0, 3)
            if e <= 1:
                poly = a * (X - r1) * X**d 
            if e == 2:
                poly = a * (X**2 + X + abs(r1)) * X**d #X**2 + X + abs(r1) is irred. over Z
            if e == 3:
                poly = a * (X**2 - X + 1) * X #X**2 - X + 1 is irred. over Z
        return sp.expand(poly)

    if niveau == 2:#"2 — Méthode somme-produit":
        a1 = 0
        while a1 == 0:
            a1 = random.randint(-5, 20)
        a  = math.floor(a1/abs(a1)) # = \pm 1 avec ~80 % de chance d'être positif
        while r1 == 0 or r2 == 0 or r1 == -r2:
            r1 = random.randint(-7, 7)
            r2 = random.randint(-7, 7)
            poly = a * (X - r1) * (X - r2)
        return sp.expand(poly)

    if niveau == 3:#"3 — Identités remarquables de degré 2":
        while r1 == 0 or math.gcd(a, r1) != 1 or a == 0:
            r1 = random.randint(-6, 6)
            a = random.randint(-5, 5)
            e  = random.randint(1, 7)
            if e in [1]:
                poly = r1**2 - X**2
            if e in [2]:
                poly = X**2 - r1**2
            if e in [3, 4]:
                poly = (X - r1)**2
            if e in [5, 6]:
                poly = (a*X - r1)**2
            if e in [7]:
                poly = X**2 + r1**2
        return sp.expand(poly)

    if niveau == 4:#"4 — Identités remarquables de degré 3":
        while r1 == 0 or math.gcd(a, r1) != 1 or a == 0:
            r1 = random.randint(-5, 5)
            a = random.randint(1, 5)
            e  = random.randint(1, 6)
            if e in [1]:
                poly = abs(r1)**3 - X**3
            if e in [2]:
                poly = X**3 - r1**3
            if e in [3, 4]:
                poly = (X - r1)**3
            if e in [5, 6]:
                poly = (a*X - r1)**3
        return sp.expand(poly)

    if niveau == 5:#"5 — Méthode des groupements":
        while r1*r2*a == 0 or math.gcd(a,r1) != 1:
            r1 = random.randint(-5, 5)
            r2 = random.randint(-4, 9)
            a  = random.randint(1, 5)
            poly = (a*X - r1) * (X**2 - r2)
        return sp.expand(poly)

    if niveau == 6:#"6 — Factorisation par la formule du discriminant":
        ### *** mettre des cas où Delta < 0... 
        while r1*r2*a == 0 or math.gcd(a,r1) != 1:
            a  = random.randint(2, 5)
            r1 = random.randint(-6, 6)
            r2 = random.randint(-6, 6)
            poly = (a*X - r1) * (X - r2)
        return sp.expand(poly)

    if niveau == 7:#"7 — Mélange (niveau facile)":
        random_niv = random.choice( [1,2,3,5] )#[NIVEAUX[i-1] for i in 
        return generer_polynome(random_niv)

    if niveau == 8:#"8 — Mélange (niveau moyen)":
        random_niv = random.choice( [1,2,3,5] )
        while a == 0:
            a = random.randint(-3, 3)
        return a * generer_polynome(random_niv)

    if niveau == 9:#"9 — Mélange (niveau difficile)":
        random_niv = random.choice( [1,2,3,4,5,6] )
        while a == 0:
            a = random.randint(-7, 7)
        return a * generer_polynome(random_niv)














st.markdown(
    """
    <style>
    div[data-baseweb="select"] {
        margin-top: -35px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1.1, 2.6, 1.3]) 
with col1:
    st.markdown("**Choisissez un niveau**")
with col2:
    niveau = st.selectbox(" ", list(NIVEAUX.keys()))
    niveau_nombre = NIVEAUX[niveau]

    if "niveau_precedent" not in st.session_state:
        st.session_state["niveau_precedent"] = niveau

    if niveau != st.session_state["niveau_precedent"]:
        st.session_state["polynome"] = generer_polynome(niveau_nombre)
        st.session_state["tentatives"] = 0
        st.session_state["feedback"] = ""
        st.session_state["niveau_precedent"] = niveau

    if "polynome" not in st.session_state:
        st.session_state["polynome"] = generer_polynome(niveau_nombre)



if niveau_nombre <= 6:
    NB_QUESTIONS = 10
else:
    NB_QUESTIONS = 10


previous_level = st.session_state.get("niveau_selectionne", None)
st.session_state.niveau_selectionne = niveau

# --- Initialisation ---
if "question" not in st.session_state:
    st.session_state["question"] = True  #<-- sinon cliquer "Vérifier" va remettre une nouvelle question !
    st.session_state["polynome"] = generer_polynome(niveau_nombre)
if "question_num" not in st.session_state:
    st.session_state.question_num = 1
if "nb_questions" not in st.session_state:
    st.session_state.nb_questions = NB_QUESTIONS
if "score" not in st.session_state:
    st.session_state.score = 0
if "historique" not in st.session_state:
    st.session_state.historique = []
if "correction_validee" not in st.session_state:
    st.session_state.correction_validee = False


if previous_level and niveau != previous_level:
    st.session_state.question_num = 1
    st.session_state.score = 0
    st.session_state.historique = []
    st.session_state.correction_validee = False
    #st.session_state.deja_eu = []
    st.session_state.nb_questions = NB_QUESTIONS
    #st.session_state.question = generer_question()
    st.rerun()




# Générer nouvel exercice
with col3:
    if st.button("➡️ Nouvelle question", disabled=st.session_state["question_num"] > NB_QUESTIONS):#question suivante
        st.session_state["tentatives"] = 0
        st.session_state["polynome"] = generer_polynome(niveau_nombre)
        st.session_state["feedback"] = ""
        st.session_state["reponse"] = ""
        st.session_state.question_num += 1
        st.session_state.correction_validee = False
        st.rerun()









def preprocess_user_input(user_str):
    """
    Prétraite la saisie utilisateur pour :
    - enlever les espaces
    - remplacer ^ par **
    - ajouter * entre nombres et parenthèses ou variables
    - ajouter * entre parenthèses consécutives
    - gérer le signe négatif au début
    """
    user_str = user_str.replace(" ", "").replace("^", "**")

    # Si la chaîne commence par "-", on remplace par "-1*" devant la parenthèse
    if user_str.startswith("-") and len(user_str) > 1 and user_str[1] == "(":
        user_str = "-1*" + user_str[1:]

    # Ajouter * entre un nombre (positif ou négatif) et une parenthèse
    user_str = re.sub(r'(\d+)\(', r'\1*(', user_str)
    user_str = re.sub(r'(-\d+)\(', r'\1*(', user_str)

    # Ajouter * entre un nombre et une variable : 3x -> 3*x
    user_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', user_str)

    # Ajouter * entre une variable et une parenthèse : x( -> x*(
    user_str = re.sub(r'([a-zA-Z])\(', r'\1*(', user_str)

    # Ajouter * entre parenthèses consécutives : )( -> )*(
    user_str = re.sub(r'\)\(', r')*(', user_str)

    return user_str





# Fonction de vérification
def get_factors(expr):
    """
    Retourne une liste de tous les facteurs multiplicatifs,
    en répétant les facteurs selon leur exposant.
    Coefficients numériques inclus.
    """
    factors = []

    # Si c'est un Mul, déplier tous les arguments
    if expr.is_Mul:
        # Séparer le coefficient numérique
        coef, rest = expr.as_coeff_Mul()
        if coef != 1 and coef != -1:#éviter le cas où   -z^6*(z^2+z) est considéré comme bonne réponse
            factors.append(coef)

        # Déplier les facteurs restants (rest peut être Mul, Pow, Symbol, Add)
        for f in rest.args if rest.is_Mul else [rest]:
            factors.extend(get_factors(f))

    # Si c'est un Pow, répéter la base autant de fois que l'exposant
    elif expr.is_Pow:
        base, exp = expr.args
        factors.extend([base] * int(exp))

    # Sinon, c'est un facteur simple (Sym, Add, nombre)
    else:
        factors.append(expr)

    return factors



def verifier_factorisation(poly, user_str):
    user_str = preprocess_user_input(user_str)
    try:
        user_str = user_str.replace(" ", "").replace("^", "**")
        #expr_user = sp.parse_expr(user_str, local_dict={"x": x})
        expr_user = sp.sympify(user_str, evaluate=False)
    except:
        return "invalid"

    # Vérifier équivalence globale
    if sp.expand(expr_user) != sp.expand(poly):
        return "incorrect"

    factors_user = get_factors(expr_user)
 
    # Compter facteurs du polynôme correctement factorisé
    factors_dict = sp.factor(poly).as_powers_dict()
    true_factors = []
    for base, exp in factors_dict.items():
        if base != -1 and base != 1:
            true_factors.extend([base]*exp)

    print("factors_user", factors_user, "\t", "true_factors", true_factors)
    if len(factors_user) < len(true_factors):
        return "incomplete"
    if len(factors_user) > len(true_factors) and not factors_user[0].is_integer:
        return "incorrect"
    if factors_user[0].is_integer and true_factors[0].is_integer and abs(factors_user[0]) != abs(true_factors[0]) and len(factors_user) == len(true_factors):
        return "incomplete"
    ### if faudrait vérifier je pense que    abs(factors_user[0]) != abs(true_factors[0])
    ### cela permet d'exclure un cas comme    3x*(2x+8)    d'être vu comme correctement factorisé...

    return "correct"







# --- Fin de quiz ---
if st.session_state.question_num > st.session_state.nb_questions:
    st.markdown("#### 🎉 Exercice terminé !")
    st.success(f"🏁 Score final : **{st.session_state.score} / {st.session_state.nb_questions}**")
    df = pd.DataFrame(st.session_state.historique)
    st.dataframe(df)
    col1, col2 = st.columns([3, 1])

    with col1:
        now = datetime.now().strftime("%Y-%m-%d_%Hh%M")
        nom_fichier = f"resultats_factorisation_{niveau}_{now}.csv"
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Télécharger les résultats", csv, nom_fichier, "text/csv")


    with col2:
        if st.button("🔄 Recommencer"):
            # Réinitialiser tous les éléments de session
            st.session_state.question_num = 1
            st.session_state.score = 0
            st.session_state.historique = []
            st.session_state.correction_validee = False
            st.session_state.deja_eu = []
            st.rerun()

    st.stop()




progress = (st.session_state.question_num - 1) / st.session_state.nb_questions * 100

col1, col2 = st.columns([3, 1.2])
with col1:
    st.markdown(
        f"""
        <div style='display: flex; align-items: center; gap: 1em;'>
            <div style='font-size: 1rem; white-space: nowrap; margin-top: 30px;'>
                Question {st.session_state.question_num} sur {st.session_state.nb_questions}
            </div>
            <div style='flex-grow: 1; background: #eee; height: 10px; border-radius: 5px; margin-top: 30px;'>
                <div style='width: {progress}%; background: #2b8fe5; height: 100%; border-radius: 5px;'></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown("<div style='margin-top: 0px;'></div>", unsafe_allow_html=True)
    st.info(f"Score actuel : {st.session_state.score} sur {st.session_state.question_num - 1}")










already_corrected = st.session_state.correction_validee
def sympy_to_csv(expr):
    s = str(expr)
    s = s.replace("**", "^")
    s = s.replace("*", "")
    return s


# Affichage du polynôme
if "polynome" in st.session_state:
    poly = st.session_state["polynome"]
    st.markdown(f"##### Factorisez au maximum sur $\\footnotesize\\mathbb{{Z}} : \\;\\;\\;{sp.latex(poly)}$")
    # pas de factorisation sur \mathbb{R} du style  x^2 - 5 = (x - √5)(x + √5)

    with st.form("verification_form"):
        # Saisie utilisateur (dans le form !)
        reponse = st.text_input(
            "Entrez la factorisation, par exemple : (x-2)(x+3)",
            key="reponse",
            label_visibility="collapsed",
            disabled=already_corrected
        )

        verifier = st.form_submit_button("✅ Vérifier", disabled=st.session_state["tentatives"] >= 2)

    if verifier and not already_corrected:
        resultat = verifier_factorisation(poly, reponse)
        if resultat == "correct":
            st.session_state["feedback"] = "✅ **Bonne réponse !**"
            st.session_state["tentatives"] = 0
            st.session_state.score += 1
        elif resultat == "incomplete":
            st.session_state["feedback"] = (
                f"⚠️ **Factorisation incomplète. On peut factoriser davantage** "
                f"(tentative {st.session_state['tentatives'] + 1} sur 3). "
            )
            st.session_state["tentatives"] += 1
        elif resultat == "incorrect":
            reponse = preprocess_user_input(reponse)
            expr_user = sp.sympify(reponse)#, locals={"x": x}
            polynome_developpe = sp.expand(expr_user)
            st.session_state["feedback"] = (
                f"❌ **Factorisation incorrecte** "
                f"(tentative {st.session_state['tentatives'] + 1} sur 3). "
                f" Votre polynôme développé est : "
                f"${sp.latex(polynome_developpe)}$"
            )
            st.session_state["tentatives"] += 1
        else:
            st.session_state["feedback"] = "⚠️ **Expression mathématique invalide.**"

        st.session_state.historique.append({
            #"Niveau": niveau,
            "Question": sympy_to_csv(poly),#f"${sp.latex(poly)}$",
            "Réponse élève": sympy_to_csv(reponse),
            "Bonne réponse": sympy_to_csv(sp.factor(poly)),#f"${sp.latex(sp.factor(poly))}$",
            "Correct": "✅" if resultat == "correct" else "❌"
        })

    if st.session_state.get("feedback"):
        st.write(st.session_state["feedback"])

    # Solution complète
    if st.session_state["tentatives"] >= 3:
        #with st.expander("📌 Voir la solution"):
        st.write(f"Solution : $\\;\\; {sp.latex(poly)}\\;$ = $\\;{sp.latex(sp.factor(poly))}$")
        
    
 





# --- Nombre de visites ---
def get_visite_count():
    try:
        with open("visites.txt", "r") as f:
            count = int(f.read())
    except:
        count = 0
    return count

def increment_visite_count():
    count = get_visite_count() + 1
    with open("visites.txt", "w") as f:
        f.write(str(count))
    return count

if "visite_enregistree" not in st.session_state:
    total = increment_visite_count()
    st.session_state.visite_enregistree = True
else:
    total = get_visite_count()

st.markdown(
    f"<div style='text-align: right; font-size: 0.2em; color: grey; margin-top: 4em;'>"
    rf"Développé par G. Leterrier (Gymnase de Bussigny, 2026)   <span style='display:inline-block; width:20px;'></span>    Nombre de visites : {total}"
    f"</div>",
    unsafe_allow_html=True
)

