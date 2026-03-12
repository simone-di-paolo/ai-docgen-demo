import os
import subprocess
import requests
import json
import re
import time
from datetime import datetime


# === CONFIGS ===

# TOKEN per Gemini API
GEMINI_API_KEY = (os.getenv("GEMINI_API_KEY") or "").strip()
MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash-lite")
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"

BOT_API_KEY = os.getenv("BOT_API_KEY")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if GEMINI_API_KEY:
    print(f"-> GEMINI_API_KEY caricato correttamente (Lunghezza: {len(GEMINI_API_KEY)})")
else:
    print("-> ERRORE: GEMINI_API_KEY è vuoto o non trovato!")
DOCS_FOLDER = "docs/"
SRC_FOLDER = "src/"
GIT_BOT_EMAIL = "actions-bot@github.com"
GIT_BOT_NAME = "GitHub Actions Bot"

DEBUG = os.getenv("DEBUG_MODE", "false").lower() == "true"
ALLOWED_EXTENSIONS_ENV = os.getenv("ALLOWED_EXTENSIONS", ".js,.jsx,.ts,.tsx,.json,.scss,.css,.java,.cs,.php,.py,.go,.rb,.cpp,.c,.h").lower()
ALLOWED_EXTENSIONS = set([ext.strip() for ext in ALLOWED_EXTENSIONS_ENV.split(",") if ext.strip()])

# File per salvare l'ultimo commit processato
LAST_COMMIT_FILE = ".last_doc_commit"

# Tipi di documentazione da generare e relative cartelle
DOCS_CATEGORIES = {
    "architettura": {
        "folder": "architettura",
        "filename": "sistema-architettura",
        "role": "You are a Senior Software Architect. Analyze the provided codebase or code changes, and write/update a high-level architectural documentation in Markdown. Focus on architectural patterns, module combinations, global state management, and routing. IMPORTANT: Output MUST be exclusively in English. ANY diagram must be written using standard Mermaid.js syntax block (```mermaid ... ```). DO NOT USE ASCII art diagrams."
    },
    "funzionale": {
        "folder": "funzionale",
        "filename": "panoramica-funzionale",
        "role": "You are an IT Product Manager. Write/update a functional overview in Markdown based on the provided code features. Explain the available user features, how the product works, and user flows. Avoid low-level code details (e.g., function names). IMPORTANT: Output MUST be exclusively in English. If flows are needed, use standard Mermaid.js flowchart syntax (```mermaid ... ```). DO NOT USE ASCII art diagrams."
    },
    "sviluppo": {
        "folder": "sviluppo",
        "filename": "linee-guida-dev",
        "role": "You are the Tech Lead. Write/update a quick developer guideline (in Markdown) based on the codebase. Explain conventions, tech stack usage, and data fetching strategies. IMPORTANT: Output MUST be exclusively in English. Use standard Markdown tables for component glossaries. No ASCII art."
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

def get_last_processed_commit():
    if os.path.exists(LAST_COMMIT_FILE):
        with open(LAST_COMMIT_FILE, "r") as f:
            return f.read().strip()
    return None

def set_last_processed_commit(commit_hash):
    with open(LAST_COMMIT_FILE, "w") as f:
        f.write(commit_hash)

def get_current_commit():
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    except:
        return None

def get_changed_files(last_commit, current_commit):
    if not last_commit:
        return None # Indica che dobbiamo analizzare tutto
    try:
        output = subprocess.run(["git", "diff", "--name-only", f"{last_commit}..{current_commit}"], capture_output=True, text=True, check=True).stdout
        return [f.strip() for f in output.split('\n') if f.strip() and f.strip().startswith(SRC_FOLDER)]
    except Exception as e:
        print(f"Errore git diff: {e}")
        return None

def gather_repository_content(changed_files=None):
    """Legge i file sorgente. Se changed_files è None, legge tutto. Altrimenti solo i modificati."""
    full_content = []
    
    if changed_files is not None:
        print(f"-> Analisi Incrementale (letti {len(changed_files)} file modificati)...")
        files_to_read = changed_files
    else:
        print(f"-> Analisi FULL Repository nella directory {SRC_FOLDER}...")
        files_to_read = []
        for root, _, files in os.walk(SRC_FOLDER):
            for file in files:
                file_path = os.path.join(root, file).replace("\\", "/")
                files_to_read.append(file_path)
                
    for file_path in files_to_read:
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ALLOWED_EXTENSIONS and os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    full_content.append(f"### FILE: {file_path} ###\n{content}\n")
            except Exception as e:
                print(f"  Errore lettura file {file_path}: {e}")
                
    return "\n".join(full_content)



# === GIT OPS ===

def backup_existing_doc(cat_folder, filename, current_commit):
    """Crea una copia di backup prima della sovrascrittura, salvandola in una sottocartella history/."""
    file_path = os.path.join(cat_folder, f"{filename}.md")
    if not os.path.exists(file_path):
        return None
        
    history_folder = os.path.join(cat_folder, "history")
    os.makedirs(history_folder, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    backup_filename = f"{filename}_old_{timestamp}_{current_commit[:7]}.md"
    backup_path = os.path.join(history_folder, backup_filename)
    
    try:
        with open(file_path, "r", encoding="utf-8") as f_in:
            with open(backup_path, "w", encoding="utf-8") as f_out:
                f_out.write(f_in.read())
        print(f"  [BACKUP] Creato backup storico: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"  Errore creazione backup {file_path}: {e}")
        return None

def commit_and_push_changes(updated_files):
    send_telegram_message("📦 Preparazione per il commit delle modifiche Globali (e Backup)...")
    subprocess.run(["git", "config", "--global", "user.name", GIT_BOT_NAME])
    subprocess.run(["git", "config", "--global", "user.email", GIT_BOT_EMAIL])

    for f in updated_files:
        subprocess.run(["git", "add", f])
    
    # Aggiungi esplicitamente anche il file di stato
    subprocess.run(["git", "add", LAST_COMMIT_FILE])
    
    commit_message = f"docs: :robot: Aggiornamento Incrementale Documentazione (con versionamento)"
    print(f"  -> Messaggio: {commit_message}")
    
    subprocess.run(["git", "commit", "-m", commit_message])
    subprocess.run(["git", "push"])
    
    success_msg = "🚀 Documentazione (e storico) aggiornata con successo!"
    print(success_msg)
    send_telegram_message(success_msg)


# === AI DOCUMENTATION GENERATOR ===

def generate_doc_category(category_key, repo_context, is_incremental, existing_doc_content=None):
    category_config = DOCS_CATEGORIES[category_key]
    role = category_config["role"]
    
    if is_incremental and existing_doc_content:
        prompt_instruction = "This is an INCREMENTAL UPDATE. Below is the EXISTING documentation. Update it intelligently based ONLY on the provided code changes (diff/modified files). DO NOT generate a completely new document, but integrate the new features, fix outdated parts, and keep the existing style. Ensure the entire final output is in ENGLISH.\n\n=== EXISTING DOC ===\n" + existing_doc_content + "\n\n=== MODIFIED/NEW CODE ===\n"
    else:
        prompt_instruction = "This is a FULL GENERATION. Read the following source code dump and generate the comprehensive documentation from scratch. Ensure the output is in ENGLISH.\n\n=== FULL SOURCE CODE ===\n"

    prompt_text = f"{role}\n\n{prompt_instruction}\n```\n{repo_context}\n```\n\nOutput ONLY the final Markdown content. Do not add starting or concluding conversational text."

    print(f"[IA] Generando il file: {category_key} usando {MODEL_NAME} (Gemini)...")
    send_telegram_message(f"🧠 Richiesta Gemini ({MODEL_NAME}) per: *{category_key}*")

    # Formato Gemini API (REST)
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_text}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "topP": 0.8,
            "topK": 40,
            "maxOutputTokens": 8192,
        }
    }

    try:
        response = requests.post(ENDPOINT, json=payload, timeout=300)
        response.raise_for_status()
        
        result = response.json()
        
        # Estrazione testo da struttura Gemini
        if "candidates" in result and len(result["candidates"]) > 0:
            generated_text = result["candidates"][0]["content"]["parts"][0]["text"].strip()
            
            # Pulizia AI block tags (```markdown)
            code_block_match = re.search(r'^```(?:markdown|md)?\s*([\s\S]*?)\s*```$', generated_text, flags=re.IGNORECASE)
            if code_block_match:
                generated_text = code_block_match.group(1).strip()
                
            print(f"[IA] Completato {category_key}!")
            return generated_text
        else:
            print(f"❌ Risposta Gemini vuota o non valida: {result}")
            return None
            
    except requests.exceptions.HTTPError as e:
        print(f"❌ ERRORE HTTP Gemini {category_key}: {e.response.status_code}")
        print(f"  -> Dettaglio API: {e.response.text}")
        send_telegram_message(f"❌ Errore HTTP Gemini: {category_key}")
        return None
    except Exception as e:
        print(f"❌ ERRORE Gemini {category_key}: {e}")
        send_telegram_message(f"❌ Errore Gemini: {category_key}")
        return None


# === MAIN WORKFLOW ===

if __name__ == "__main__":
    send_telegram_message("🤖 ===== AVVIO RIGENERAZIONE INCREMENTALE WIKI =====")
    
    current_commit = get_current_commit()
    if not current_commit:
        print("Errore: impossibile determinare il commit corrente.")
        exit(1)
        
    last_commit = get_last_processed_commit()
    changed_files = None
    is_incremental = False
    
    if last_commit and last_commit != current_commit:
        changed_files = get_changed_files(last_commit, current_commit)
        if changed_files is not None:
            if len(changed_files) == 0 and not DEBUG:
                print("Nessun file modificato in src/. Salto la generazione.")
                set_last_processed_commit(current_commit)
                exit(0)
            is_incremental = True
            print(f"Modalità: INCREMENTALE (da {last_commit[:7]} a {current_commit[:7]})")
    
    if not is_incremental:
        print("Modalità: FULL RANGE (Nessun commit precedente valido o prima esecuzione)")
        
    repo_context = gather_repository_content(changed_files)
    if not repo_context.strip():
        print("Nessun contenuto sorgente trovato. Salto.")
        exit(0)
    
    updated_files_list = []
    
    for cat_key, cat_data in DOCS_CATEGORIES.items():
        cat_folder = os.path.join(DOCS_FOLDER, cat_data["folder"])
        os.makedirs(cat_folder, exist_ok=True)
        file_path = os.path.join(cat_folder, f'{cat_data["filename"]}.md')
        
        # Leggi contenuto esistente per il contesto (necessario per incremental)
        existing_content = None
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                existing_content = f.read()
                
        # Ai Call
        doc_content = generate_doc_category(cat_key, repo_context, is_incremental, existing_content)
        
        if doc_content:
            # Esegui il backup del file ATTUALE solo se l'AI ha generato un nuovo contenuto valido
            backup_path = backup_existing_doc(cat_folder, cat_data["filename"], current_commit)
            if backup_path:
                updated_files_list.append(backup_path)
            
            # Sovrascrivi il file principale con la nuova doc
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(doc_content)
            updated_files_list.append(file_path)
            
        print("Attendo 5 secondi prima della prossima categoria API...")
        time.sleep(5)
            
    if updated_files_list:
        set_last_processed_commit(current_commit)
        commit_and_push_changes(updated_files_list)
        
    send_telegram_message("🏁 ===== FINE RIGENERAZIONE WIKI (Gemini API) =====")

