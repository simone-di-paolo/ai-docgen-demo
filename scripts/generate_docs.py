
import os
import subprocess
import requests
import json
import re
import shutil

# === CONFIGS ===

API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
DOCS_FOLDER = "docs/"
SRC_FOLDER = "src/"
GIT_BOT_EMAIL = "actions-bot@github.com"
GIT_BOT_NAME = "GitHub Actions Bot"

DEBUG = os.getenv("DEBUG_MODE", "false").lower() == "true"


# === UTILS ===

def get_changed_files():
    """Get the list of edited file during in the last commit"""
    try:
        diff_output = subprocess.run(
            ["git", "diff", "HEAD~1", "HEAD", "--name-only", "--", SRC_FOLDER],
            capture_output=True, text=True, check=True
        ).stdout.strip()
        return diff_output.split('\n') if diff_output else []
    except subprocess.CalledProcessError as e:
        print(f"[ERRORE] Durante l'esecuzione di git diff: {e}")
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
        print(f"  -> Backup creato: {backup_path}")

def get_component_name_from_path(filepath):
    """Extract the name of the component based on the file name"""
    return os.path.splitext(os.path.basename(filepath))[0]

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

    if DEBUG:
        print("\n" + "="*20 + " DEBUG: PROMPT PER L'IA " + "="*20)
        print(prompt)
        print("="*60 + "\n")

    # Aggiornato: La chiave API viene passata nell'header per maggiore sicurezza.
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(GEMINI_API_ENDPOINT, headers=headers, data=json.dumps(data), timeout=180)
        response.raise_for_status()

        if DEBUG:
            print("\n" + "="*20 + " DEBUG: RISPOSTA RAW DALL'IA " + "="*20)
            print(response.text)
            print("="*60 + "\n")

        return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    except requests.exceptions.HTTPError as e:
        print(f"[ERRORE] Errore HTTP dall'API Gemini per {component_name}: {e}")
        print(f"  -> Status Code: {e.response.status_code}")
        print(f"  -> Response Body: {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[ERRORE] Errore di connessione all'API Gemini per {component_name}: {e}")
        return None

def commit_and_push_changes(updated_docs):
    """Commit and send all the updated docs to the repo"""
    subprocess.run(["git", "config", "--global", "user.name", GIT_BOT_NAME])
    subprocess.run(["git", "config", "--global", "user.email", GIT_BOT_EMAIL])

    for doc_file in updated_docs:
        subprocess.run(["git", "add", doc_file])
    
    commit_message = f"docs: :robot: Aggiornamento automatico per {', '.join([get_component_name_from_path(f) for f in updated_docs])}"
    print(f"  -> Messaggio di commit: {commit_message}")
    subprocess.run(["git", "commit", "-m", commit_message])
    subprocess.run(["git", "push"])
    print("\n>>> Documentazione inviata con successo! <<<")

# --- 3. Flusso Principale ---

if __name__ == "__main__":
    print("="*20 + " AVVIO SCRIPT DOCUMENTAZIONE " + "="*20)
    
    print("\n--- FASE 1: Rilevamento Modifiche ---")
    changed_files = get_changed_files()
    if not changed_files:
        print("Nessun file sorgente modificato. Uscita.")
        exit()
    print(f"File modificati rilevati: {', '.join(changed_files)}")

    print("\n--- FASE 2: Raggruppamento Diff per Componente ---")
    component_diffs = {}
    for file_path in changed_files:
        if not (file_path.endswith(".jsx") or file_path.endswith(".css")):
            continue
        
        component_name = get_component_name_from_path(file_path)
        if component_name == "App" and "components" in file_path:
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
    print("Diff raggruppati con successo.")

    print("\n--- FASE 3: Elaborazione e Generazione Documentazione ---")
    updated_doc_files = []
    for component_name, diffs in component_diffs.items():
        doc_path = os.path.join(DOCS_FOLDER, f"{component_name}.md")
        full_diff = "\n".join(diffs)

        print(f"\n-> Elaborazione Componente: {component_name}")
        current_documentation = get_file_content(doc_path)
        
        new_documentation = generate_new_documentation(component_name, full_diff, current_documentation)

        if new_documentation and new_documentation.strip() != current_documentation.strip():
            print(f"  -> Documentazione per {component_name} aggiornata dall'IA.")
            create_backup(doc_path)
            with open(doc_path, "w", encoding="utf-8") as f:
                f.write(new_documentation)
            updated_doc_files.append(doc_path)
        else:
            print(f"  -> Nessun aggiornamento significativo per la documentazione di {component_name}.")

    print("\n--- FASE 4: Finalizzazione ---")
    if updated_doc_files:
        print("Rilevati aggiornamenti alla documentazione. Invio delle modifiche...")
        commit_and_push_changes(updated_doc_files)
    else:
        print("Nessun file di documentazione è stato modificato. Nessun commit necessario.")

