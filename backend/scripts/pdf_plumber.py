import requests
import pdfplumber
import os

# --- CONFIGURATION ---
PDF_LINKS_FILE = "arxiv_references.txt"  # Plik z listą linków do PDF-ów
SAVE_DIR = "downloaded_pdfs"  # Katalog do zapisu plików PDF i TXT

# --- CREATE SAVE DIRECTORY ---
os.makedirs(SAVE_DIR, exist_ok=True)

def download_pdf(pdf_url, save_path):
    """Pobiera PDF z podanego URL-a i zapisuje go na dysku."""
    try:
        response = requests.get(pdf_url, timeout=20)
        response.raise_for_status()
        
        with open(save_path, "wb") as f:
            f.write(response.content)
        
        print(f"✅ Pobrano: {pdf_url}")
        return True
    except requests.RequestException as e:
        print(f"❌ Błąd pobierania {pdf_url}: {e}")
        return False

def pdf_to_text(pdf_path):
    """Konwertuje PDF na tekst, ignorując obrazy."""
    try:
        text = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # Usuwamy tekst osadzony w obrazach
                extracted_text = page.extract_text()
                if extracted_text:
                    text.append(extracted_text)
        return "\n".join(text)
    except Exception as e:
        print(f"❌ Błąd konwersji PDF na tekst: {pdf_path} - {e}")
        return None

def process_pdf_links(file_path):
    """Czyta plik z linkami, pobiera PDF-y, konwertuje je do TXT i usuwa PDF-y."""
    with open(file_path, "r") as f:
        pdf_links = [line.strip() for line in f if line.strip()]
    
    for pdf_url in pdf_links:
        pdf_name = pdf_url.split("/")[-1] + ".pdf"  # np. "2301.08162.pdf"
        pdf_path = os.path.join(SAVE_DIR, pdf_name)
        txt_path = pdf_path.replace(".pdf", ".txt")

        if download_pdf(pdf_url, pdf_path):
            text = pdf_to_text(pdf_path)
            if text:
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"✅ Zapisano TXT: {txt_path}")
            else:
                print(f"⚠️ Brak tekstu w PDF: {pdf_path}")

            # Usuwanie PDF po przetworzeniu
            try:
                os.remove(pdf_path)
                print(f"🗑️ Usunięto PDF: {pdf_path}")
            except Exception as e:
                print(f"❌ Błąd usuwania PDF: {pdf_path} - {e}")

# --- RUN SCRIPT ---
if __name__ == "__main__":
    process_pdf_links(PDF_LINKS_FILE)
    print("\n🎉 Proces zakończony!")