import os
import subprocess
import requests
import json
import re

# === CONFIGS ===

API_KEY = os.getenv("GEMINI_API_KEY")
BOT_API_KEY = os.getenv("BOT_API_KEY")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

GEMINI_API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent"
DOCS_FOLDER = "docs/"
SRC_FOLDER = "src/"
GIT_BOT_EMAIL = "actions-bot@github.com"
GIT_BOT_NAME = "GitHub Actions Bot"

DEBUG = os.getenv("DEBUG_MODE", "false").lower() == "true"
ALLOWED_EXTENSIONS_ENV = os.getenv("ALLOWED_EXTENSIONS", ".js,.jsx,.ts,.tsx,.json,.scss,.css,.java,.cs,.php,.py,.go,.rb,.cpp,.c,.h").lower()
ALLOWED_EXTENSIONS = set([ext.strip() for ext in ALLOWED_EXTENSIONS_ENV.split(",") if ext.strip()])

# Tipi di documentazione da generare e relative cartelle
DOCS_CATEGORIES = {
    "architettura": {
        "folder": "architettura",
        "filename": "sistema-architettura",
        "role": "Sei un Senior Software Architect. Analizza il seguente codice sorgente e scrivi una documentazione architetturale dettagliata di questo progetto in Markdown. Concentrati sui pattern architetturali utilizzati, su come comunicano i moduli principali, la gestione dello stato globale (es. Redux), e il routing. Ignora lo stile UI specifico e produci un documento di alto livello per gli sviluppatori senior."
    },
    "funzionale": {
        "folder": "funzionale",
        "filename": "panoramica-funzionale",
        "role": "Sei un Product Manager IT. Scrivi una panoramica funzionale (in formato Markdown) del prodotto in base al codice sorgente fornito. Spiega le feature disponibili per l'utente, come funziona il prodotto e cosa permette di fare. Evita del tutto i dettagli del codice (es. nomi dei file, funzioni hook, variabili), ma concentrati sull'esperienza finale e i flussi utente."
    },
    "sviluppo": {
        "folder": "sviluppo",
        "filename": "linee-guida-dev",
        "role": "Sei il Tech Lead del progetto. Scrivi una guida rapida allo sviluppo (in Markdown) in base alla codebase fornita. La documentazione aiuterà i nuovi sviluppatori a capire le convenzioni usate (es. Typescript vs JS, uso di scss, come avviene il fetch dei dati dalle API). Includi un glossario dei componenti React più importanti e la loro locazione."
    }
}

# === TELEGRAM UTILS ===

def send_telegram_message(message):
    """Invia un messaggio a un chat di Telegram e lo tronca se troppo lungo."""
    if not BOT_API_KEY or not TELEGRAM_CHAT_ID:
        return

    max_length = 4096
    truncated_message = (message[:max_length - 4] + '...') if len(message) > max_length else message
    
    url = f"https://api.telegram.org/bot{BOT_API_KEY}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': truncated_message,
        'parse_mode': 'Markdown'
    }
    
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"[ERRORE TELEGRAM] {e}")


# === REPOSITORY SCRAPING ===

def gather_repository_content():
    """Legge tutti i file sorgente principali nella cartella src/"""
    print(f"-> Analisi dell'intero repository nella directory {SRC_FOLDER}...")
    full_content = []
    
    for root, _, files in os.walk(SRC_FOLDER):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        full_content.append(f"### FILE: {file_path} ###\n{content}\n")
                except Exception as e:
                    print(f"Errore lettura file {file_path}: {e}")
                    
    return "\n".join(full_content)


# === GIT OPS ===

def commit_and_push_changes(updated_docs):
    send_telegram_message("📦 Preparazione per il commit delle modifiche Globali...")
    subprocess.run(["git", "config", "--global", "user.name", GIT_BOT_NAME])
    subprocess.run(["git", "config", "--global", "user.email", GIT_BOT_EMAIL])

    for doc_file in updated_docs:
        subprocess.run(["git", "add", doc_file])
    
    commit_message = f"docs: :robot: Aggiornamento globale architettura e funnel IA"
    print(f"  -> Messaggio: {commit_message}")
    
    subprocess.run(["git", "commit", "-m", commit_message])
    subprocess.run(["git", "push"])
    
    success_msg = "🚀 Tutta la documentazione è stata inviata con successo!"
    print(success_msg)
    send_telegram_message(success_msg)

# === AI DOCUMENTATION GENERATOR ===

def generate_doc_category(category_key, repo_context):
    category_config = DOCS_CATEGORIES[category_key]
    role = category_config["role"]
    
    prompt = f"""
    {role}
    
    Di seguito c'è il codice corrente ('source code dump') dell'intero progetto:
    
    ```
    {repo_context}
    ```
    
    Restituisci ESCLUSIVAMENTE il contenuto della documentazione in Markdown per la tua richiesta. Non aggiungere alcun tag iniziale ```markdown o finali.
    """

    print(f"[IA] Generando il file: {category_key}...")
    send_telegram_message(f"🧠 Richiesta Gemini per: *{category_key}*")

    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.2
        }
    }

    try:
        url_with_key = f"{GEMINI_API_ENDPOINT}?key={API_KEY}"
        response = requests.post(url_with_key, headers=headers, json=data, timeout=300)
        response.raise_for_status()
        
        generated_text = response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        
        # Pulizia AI block tags (```markdown)
        code_block_match = re.search(r'^```(?:markdown|md)?\s*([\s\S]*?)\s*```$', generated_text, flags=re.IGNORECASE)
        if code_block_match:
            generated_text = code_block_match.group(1).strip()
            
        print(f"[IA] Completato {category_key}!")
        return generated_text
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ ERRORE HTTP generazione {category_key}: {e.response.status_code}")
        print(f"  -> Dettaglio Gemini API: {e.response.text}")
        send_telegram_message(f"❌ Errore HTTP generazione documentazione: {category_key}")
        return None
    except Exception as e:
        print(f"❌ ERRORE generazione {category_key}: {e}")
        send_telegram_message(f"❌ Errore generazione documentazione: {category_key}")
        return None

# === MAIN WORKFLOW ===

if __name__ == "__main__":
    send_telegram_message("🤖 ===== AVVIO RIGENERAZIONE GLOBALE WIKI =====")
    
    # Optional: Controllare se c'è un file modificato
    try:
        diff_output = subprocess.run(["git", "diff", "HEAD~1", "HEAD", "--name-only"], capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        diff_output = ""
        
    if "src/" not in diff_output and not DEBUG:
        print("Nessuna modifica rilevata in src/. Salto.")
        exit()
        
    repo_context = gather_repository_content()
    
    updated_files = []
    
    for cat_key, cat_data in DOCS_CATEGORIES.items():
        doc_content = generate_doc_category(cat_key, repo_context)
        if doc_content:
            cat_folder = os.path.join(DOCS_FOLDER, cat_data["folder"])
            os.makedirs(cat_folder, exist_ok=True)
            
            file_path = os.path.join(cat_folder, f'{cat_data["filename"]}.md')
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(doc_content)
                
            updated_files.append(file_path)
            
    if updated_files:
        commit_and_push_changes(updated_files)
        
    send_telegram_message("🏁 ===== FINE RIGENERAZIONE GLOBALE =====")
