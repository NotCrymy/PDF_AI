# PDF AI

Application locale permettant d'extraire le contenu de fichiers PDF puis, à terme, d'utiliser un LLM local pour analyser les documents, répondre à des questions et extraire des informations.

L'objectif principal du projet est de conserver l'ensemble du traitement en local afin de ne pas envoyer les documents à une API distante.

## État actuel

Le projet possède actuellement deux parties fonctionnelles :

* extraction du texte des PDF avec PyMuPDF ;
* exécution d'un modèle LLM local avec Ollama.

Le modèle actuellement utilisé est **LFM2.5 1.2B Instruct**, au format GGUF.

Le modèle a été téléchargé dans le projet puis importé dans Ollama.

Le fonctionnement suivant a été testé avec succès :

```text
PDF
 ↓
PyMuPDF
 ↓
texte extrait
 ↓
Ollama
 ↓
LFM2.5 local
 ↓
réponse
```

L'intégration complète PDF → LLM n'est pas encore faite.

---

## Architecture actuelle

Structure approximative du projet :

```text
PDF_AI/
│
├── Modelfile
├── main.py
├── ai.py
│
├── models/
│   └── lfm2.5/
│       └── model.gguf
│
└── python_core/
    │
    └── pdf/
        ├── PdfDocument.py
        ├── PdfList.py
        └── PdfManager.py
```

L'architecture va évoluer lorsque la partie IA sera intégrée au reste du projet.

---

## Extraction PDF

L'extraction est actuellement réalisée avec `PyMuPDF`.

Le `PdfManager` ouvre chaque PDF et extrait le texte page par page.

Le texte est actuellement nettoyé directement pendant le parsing :

```python
text = page.get_text()
text = text.replace('\n', ' ').replace('\r', ' ').strip()
```

Chaque page est ensuite ajoutée au `PdfDocument`.

Un document ressemble actuellement à ceci :

```json
{
    "path": "Compte_rendu_reunion_Maki.pdf",
    "pages": [
        {
            "page": 1,
            "text": "Compte rendu de réunion Équipe Maki ..."
        }
    ]
}
```

Le document peut ensuite être exporté en JSON.

L'écriture JSON utilise :

```python
json.dump(
    json_data,
    f,
    ensure_ascii=False,
    indent=4
)
```

et le fichier est ouvert avec un encodage UTF-8 afin de conserver correctement les caractères Unicode.

---

## Modèle local

Le modèle utilisé actuellement est :

```text
LFM2.5-1.2B-Instruct-Q4_K_M.gguf
```

Il est stocké dans :

```text
models/lfm2.5/model.gguf
```

Le fichier GGUF est ensuite importé dans Ollama.

### Modelfile

Le fichier `Modelfile` situé à la racine du projet contient actuellement :

```text
FROM ./models/lfm2.5/model.gguf
```

Pour créer le modèle Ollama :

```powershell
ollama create lfm2.5-local -f Modelfile
```

Cette commande a été testée avec succès.

Résultat actuel :

```text
NAME                   ID              SIZE
lfm2.5-local:latest    9e61ec6139cd    730 MB
```

Il ne faut donc pas utiliser :

```powershell
ollama pull lfm2.5
```

pour l'installation actuelle : le fichier GGUF est déjà fourni localement dans `models/`.

---

## Confidentialité

L'objectif du projet est de faire fonctionner l'analyse des documents entièrement en local.

Le principe recherché est :

```text
PDF
 ↓
Extraction locale
 ↓
Traitement local
 ↓
LLM local
 ↓
Réponse
```

Aucune API cloud de LLM n'est nécessaire pour le fonctionnement actuel.

Ollama sert uniquement de moteur local pour exécuter le modèle.

---

# Commandes utiles

Vérifier la version d'Ollama :

```powershell
ollama --version
```

Voir les modèles disponibles :

```powershell
ollama list
```

Créer le modèle à partir du GGUF :

```powershell
ollama create lfm2.5-local -f Modelfile
```

Tester directement le modèle avec Ollama :

```powershell
ollama run lfm2.5-local
```

Installer la librairie Python :

```powershell
python -m pip install ollama
```

Tester le script Python :

```powershell
python ai.py
```
