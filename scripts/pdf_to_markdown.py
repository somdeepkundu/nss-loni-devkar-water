"""
Extract PDFs and convert to markdown for documentation
"""

import pdfplumber
from pathlib import Path
from datetime import datetime

def extract_pdf_to_markdown(pdf_path, output_path):
    """Extract text from PDF and save as markdown"""

    pdf_name = Path(pdf_path).stem

    try:
        with pdfplumber.open(pdf_path) as pdf:
            markdown_content = []
            markdown_content.append(f"# {pdf_name}\n")
            markdown_content.append(f"*Extracted from: {Path(pdf_path).name}*\n")
            markdown_content.append(f"*Date extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            markdown_content.append("---\n\n")

            for i, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    markdown_content.append(f"## Page {i}\n\n")
                    markdown_content.append(text)
                    markdown_content.append("\n\n---\n\n")

            # Write to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.writelines(markdown_content)

            print(f"[OK] {pdf_name} -> {output_path}")
            return True
    except Exception as e:
        print(f"[ERROR] {pdf_name}: {e}")
        return False

def main():
    pdf_files = [
        "C:\\Users\\Somdeep Kundu\\Downloads\\README77331_V2m.pdf",
        "C:\\Users\\Somdeep Kundu\\Downloads\\README77331_V1m.pdf",
        "C:\\Users\\Somdeep Kundu\\Downloads\\TP_ Sch.33.1 NSS 77th round_final_26.09.2019.pdf",
        "C:\\Users\\Somdeep Kundu\\Downloads\\nic_amendment_2008.pdf",
        "C:\\Users\\Somdeep Kundu\\Downloads\\Estimation_procedure_NSS77_DPD.pdf",
        "C:\\Users\\Somdeep Kundu\\Downloads\\77th_V_I_Final.pdf",
        "C:\\Users\\Somdeep Kundu\\Downloads\\77th_V_IIFinal.pdf",
    ]

    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)

    print("\n" + "="*70)
    print("CONVERTING PDFs TO MARKDOWN")
    print("="*70)

    success_count = 0
    for pdf_file in pdf_files:
        if Path(pdf_file).exists():
            md_file = docs_dir / f"{Path(pdf_file).stem}.md"
            if extract_pdf_to_markdown(pdf_file, md_file):
                success_count += 1
        else:
            print(f"[SKIP] File not found: {pdf_file}")

    print("\n" + "="*70)
    print(f"COMPLETED: {success_count}/{len(pdf_files)} PDFs converted")
    print("="*70)
    print(f"\nMarkdown files saved in: docs/")

if __name__ == "__main__":
    main()
