from PyPDF2 import PdfReader, PdfWriter
import os

def clean_pdf_for_github(input_path, output_path):
    """
    Clean PDF to make it more compatible with GitHub viewer
    """
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        writer.add_metadata({})
        
        with open(output_path, "wb") as f_out:
            writer.write(f_out)
        
        print(f"PDF cleaned successfully! Output: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error cleaning PDF: {e}")
        return False

if __name__ == "__main__":
    input_path = "Informe_Sintetizacion_Fonemas_Modelo_AR.pdf"
    output_path = "Informe_Modelo_AR_GitHub_Compatible.pdf"
    
    if os.path.exists(input_path):
        success = clean_pdf_for_github(input_path, output_path)
        if success:
            print("\nNow you can:")
            print("1. Remove the original: git rm Informe_Sintetizacion_Fonemas_Modelo_AR.pdf")
            print("2. Add the cleaned version: git add Informe_Modelo_AR_GitHub_Compatible.pdf")
            print("3. Commit and push")
    else:
        print(f"File {input_path} not found!") 