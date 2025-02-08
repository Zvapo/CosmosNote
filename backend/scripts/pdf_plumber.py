import requests
import fitz  # pymupdf (faster than pdfplumber)
import os
from tqdm import tqdm

# --- CONFIGURATION ---
PDF_LINKS_FILE = "arxiv_references.txt"
SAVE_DIR = "downloaded_pdfs"

# --- CREATE SAVE DIRECTORY ---
os.makedirs(SAVE_DIR, exist_ok=True)

def download_pdf(pdf_url, save_path):
    """Download PDF in chunks with tqdm progress bar."""
    try:
        with requests.get(pdf_url, stream=True, timeout=60) as response:
            response.raise_for_status()
            total_size = int(response.headers.get("content-length", 0))

            with open(save_path, "wb") as f, tqdm(
                total=total_size, unit="B", unit_scale=True, desc=f"📥 {os.path.basename(save_path)}"
            ) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))

        print(f"✅ Downloaded: {pdf_url}")
        return True
    except requests.RequestException as e:
        print(f"❌ Download error {pdf_url}: {e}")
        return False

def pdf_to_text(pdf_path):
    """Extracts text from a PDF using pymupdf (ignores images) with tqdm progress bar."""
    try:
        text = []
        doc = fitz.open(pdf_path)
        
        for i in tqdm(range(len(doc)), desc=f"📖 Processing {os.path.basename(pdf_path)}", unit="page"):
            try:
                extracted_text = doc[i].get_text("text")  # Only extract text, ignore images
                if extracted_text:
                    text.append(extracted_text)
                else:
                    print(f"⚠️ No text on page {i+1}, possibly only images.")
            except Exception as e:
                print(f"⚠️ Error processing page {i+1} in {pdf_path}: {e}")

        return "\n".join(text) if text else None
    except Exception as e:
        print(f"❌ PDF conversion error: {pdf_path} - {e}")
        return None

def process_pdf_links(file_path):
    """Reads the file with links, downloads PDFs, extracts text, and deletes the PDFs with tqdm progress bar."""
    with open(file_path, "r") as f:
        pdf_links = [line.strip() for line in f if line.strip()]

    for pdf_url in tqdm(pdf_links, desc="📂 Processing PDFs", unit="file"):
        pdf_name = pdf_url.split("/")[-1] + ".pdf"
        pdf_path = os.path.join(SAVE_DIR, pdf_name)
        txt_path = pdf_path.replace(".pdf", ".txt")

        if os.path.exists(txt_path):
            print(f"⏭️ Skipping (already processed): {txt_path}")
            continue

        if download_pdf(pdf_url, pdf_path):
            text = pdf_to_text(pdf_path)
            if text:
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"✅ Saved TXT: {txt_path}")
            else:
                print(f"⚠️ No text found in PDF: {pdf_path}")

            # Delete the PDF after processing
            try:
                os.remove(pdf_path)
                print(f"🗑️ Deleted PDF: {pdf_path}")
            except Exception as e:
                print(f"❌ Error deleting PDF: {pdf_path} - {e}")

# --- RUN SCRIPT ---
if __name__ == "__main__":
    process_pdf_links(PDF_LINKS_FILE)
    print("\n🎉 Processing complete!")