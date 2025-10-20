
import os
import subprocess
import requests
import json
import re
import shutil

# === CONFIGS ===

API_KEY = os.getenv("GEMINI_API_KEY")
BOT_API_KEY = os.getenv("BOT_API_KEY")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

GEMINI_API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
DOCS_FOLDER = "docs/"
SRC_FOLDER = "src/"
GIT_BOT_EMAIL = "actions-bot@github.com"
GIT_BOT_NAME = "GitHub Actions Bot"

DEBUG = os.getenv("DEBUG_MODE", "false").lower() == "true"

# === TELEGRAM UTILS ===

def send_telegram_message(message):
    """Invia un messaggio a un chat di Telegram e lo tronca se troppo lungo."""
    if not BOT_API_KEY or not TELEGRAM_CHAT_ID:
        if DEBUG:
            print("[DEBUG TELEGRAM] BOT_API_KEY o TELEGRAM_CHAT_ID non impostati. Salto l'invio.")
        return

    max_length = 4096  # Limite di Telegram per messaggio
    truncated_message = (message[:max_length - 4] + '...') if len(message) > max_length else message
    
    url = f"https://api.telegram.org/bot{BOT_API_KEY}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': truncated_message,
        'parse_mode': 'Markdown'
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        if DEBUG:
            print(f"[DEBUG TELEGRAM] Messaggio inviato con successo.")
    except requests.exceptions.RequestException as e:
        # Non bloccare lo script se Telegram non funziona
        print(f"[ERRORE TELEGRAM] Impossibile inviare il messaggio: {e}")

# === GIT & FILE UTILS ===

def get_changed_files():
    """Get the list of edited file during in the last commit"""
    try:
        diff_output = subprocess.run(
            ["git", "diff", "HEAD~1", "HEAD", "--name-only", "--", SRC_FOLDER],
            capture_output=True, text=True, check=True
        ).stdout.strip()
        return diff_output.split('\n') if diff_output else []
    except subprocess.CalledProcessError as e:
        error_msg = f"[ERRORE] Durante l'esecuzione di git diff: {e}"
        print(error_msg)
        send_telegram_message(f"❌ ERRORE: Fallita l'esecuzione di `git diff`. Impossibile continuare.")
        return []

def get_file_content(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def create_backup(filepath):
    """Create a backup file of the original documentation"""
    if os.path.exists(filepath):
        backup_path = f"{filepath}.bak"
        shutil.copy2(filepath, backup_path)
        msg = f"  -> Backup creato: {backup_path}"
        print(msg)
        send_telegram_message(f"📑 Creato backup della documentazione precedente: `{os.path.basename(backup_path)}`")


def get_component_name_from_path(filepath):
    """Extract the name of the component based on the file name"""
    return os.path.splitext(os.path.basename(filepath))[0]

# === AI DOCUMENTATION GENERATOR ===

def generate_new_documentation(component_name, file_diff, current_docs):
    """Make a call to Gemini API to generate new documentation."""
    prompt = f"""
    Sei un ingegnere software che scrive documentazione per un team aziendale.
    Il tuo compito è aggiornare la documentazione per uno specifico componente React chiamato '{component_name}'.

    **DOCUMENTAZIONE ATTUALE DEL COMPONENTE:**
    ```markdown
    {current_docs}
    ```

    **MODIFICHE APPORTATE AL CODICE (GIT DIFF):**
    ```diff
    {file_diff}
    ```

    **ISTRUZIONI:**
    1. Analizza il git diff per capire le modifiche funzionali e stilistiche.
    2. Aggiorna la documentazione attuale per riflettere accuratamente queste modifiche. Se la documentazione non esiste, creala da zero.
    3. Mantieni lo stile esistente. Sii chiaro, tecnico e conciso. Scrivi in italiano.
    4. Restituisci **SOLO** il contenuto Markdown completo e aggiornato per il componente '{component_name}'. Non includere titoli o commenti extra.

    **NUOVA DOCUMENTAZIONE PER {component_name}:**
    """

    send_telegram_message(f"🧠 Sto chiamando l'IA per aggiornare `{component_name}`...")

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(GEMINI_API_ENDPOINT, headers=headers, data=json.dumps(data), timeout=180)
        response.raise_for_status()
        
        generated_text = response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        send_telegram_message(f"✅ IA ha risposto per `{component_name}`. Risposta (troncata):```{generated_text[:800]}...```")
        
        return generated_text
        
    except requests.exceptions.HTTPError as e:
        error_text = f"❌ ERRORE HTTP dall'API Gemini per `{component_name}`: {e.response.status_code}"
        print(error_text)
        print(f"  -> Response Body: {e.response.text}")
        send_telegram_message(error_text)
        return None
    except requests.exceptions.RequestException as e:
        error_text = f"❌ ERRORE di connessione all'API Gemini per `{component_name}`: {e}"
        print(error_text)
        send_telegram_message(error_text)
        return None

# === GIT OPS ===

def commit_and_push_changes(updated_docs):
    """Commit and send all the updated docs to the repo"""
    send_telegram_message("📦 Preparazione per il commit delle modifiche...")
    subprocess.run(["git", "config", "--global", "user.name", GIT_BOT_NAME])
    subprocess.run(["git", "config", "--global", "user.email", GIT_BOT_EMAIL])

    for doc_file in updated_docs:
        subprocess.run(["git", "add", doc_file])
    
    component_names = ', '.join([get_component_name_from_path(f) for f in updated_docs])
    commit_message = f"docs: :robot: Aggiornamento automatico per {component_names}"
    
    print(f"  -> Messaggio di commit: {commit_message}")
    send_telegram_message(f"📝 Messaggio di commit:`{commit_message}`")
    
    subprocess.run(["git", "commit", "-m", commit_message])
    subprocess.run(["git", "push"])
    
    success_msg = "🚀 Documentazione inviata con successo!"
    print(f"\n>>> {success_msg} <<<")
    send_telegram_message(success_msg)

# === MAIN WORKFLOW ===

if __name__ == "__main__":
    send_telegram_message("🤖 ===== INIZIO SCRIPT DOCUMENTAZIONE =====")
    print("="*20 + " AVVIO SCRIPT DOCUMENTAZIONE " + "="*20)
    
    print("\n--- FASE 1: Rilevamento Modifiche ---")
    changed_files = get_changed_files()
    if not changed_files or all(f == '' for f in changed_files):
        msg = "✅ Nessun file sorgente modificato nell'ultimo commit. Uscita."
        print(msg)
        send_telegram_message(msg)
        send_telegram_message("🤖 ===== FINE SCRIPT DOCUMENTAZIONE =====")
        exit()
        
    msg = f"🔍 File modificati rilevati: `{'`, `'.join(changed_files)}`"
    print(msg)
    send_telegram_message(msg)

    print("\n--- FASE 2: Raggruppamento Diff per Componente ---")
    component_diffs = {}
    for file_path in changed_files:
        if not (file_path.endswith(".jsx") or file_path.endswith(".css")):
            continue
        
        component_name = get_component_name_from_path(file_path)
        if component_name in ["App", "main"] and "components" in file_path:
             path_parts = file_path.split(os.sep)
             try:
                 components_index = path_parts.index("components")
                 if components_index + 1 < len(path_parts):
                     component_name = path_parts[components_index + 1]
             except ValueError:
                 pass

        if component_name not in component_diffs:
            component_diffs[component_name] = []
        
        file_diff_output = subprocess.run(
            ["git", "diff", "HEAD~1", "HEAD", "--", file_path],
            capture_output=True, text=True
        ).stdout
        component_diffs[component_name].append(file_diff_output)
    
    send_telegram_message(f"📊 Diff raggruppati per i seguenti componenti: `{'`, `'.join(component_diffs.keys())}`")
    print("Diff raggruppati con successo.")

    print("\n--- FASE 3: Elaborazione e Generazione Documentazione ---")
    updated_doc_files = []
    for component_name, diffs in component_diffs.items():
        doc_path = os.path.join(DOCS_FOLDER, f"{component_name}.md")
        full_diff = "\n".join(diffs)

        print(f"\n-> Elaborazione Componente: {component_name}")
        send_telegram_message(f"⚙️ Elaborazione componente: *{component_name}*")
        
        current_documentation = get_file_content(doc_path)
        
        new_documentation = generate_new_documentation(component_name, full_diff, current_documentation)

        if new_documentation and new_documentation.strip() != current_documentation.strip():
            msg = f"  -> Documentazione per {component_name} aggiornata dall'IA."
            print(msg)
            send_telegram_message(f"✍️ Documentazione per `{component_name}` aggiornata.")
            
            create_backup(doc_path)
            
            with open(doc_path, "w", encoding="utf-8") as f:
                f.write(new_documentation)
            updated_doc_files.append(doc_path)
        else:
            msg = f"  -> Nessun aggiornamento significativo per la documentazione di {component_name}."
            print(msg)
            send_telegram_message(f"🤷‍♂️ Nessun aggiornamento per la doc di `{component_name}`.")

    print("\n--- FASE 4: Finalizzazione ---")
    if updated_doc_files:
        print("Rilevati aggiornamenti alla documentazione. Invio delle modifiche...")
        commit_and_push_changes(updated_doc_files)
    else:
        msg = "✅ Nessun file di documentazione è stato modificato. Nessun commit necessario."
        print(msg)
        send_telegram_message(msg)
        
    send_telegram_message("🤖 ===== FINE SCRIPT DOCUMENTAZIONE =====")
