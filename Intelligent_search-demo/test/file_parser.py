from pptx import Presentation
from docx import Document
import fitz  # PyMuPDF
from docx import *
from pathlib import Path
import glob
from tika import parser
from pptx import Presentation

def get_data_tikka(file_path):

    parsed = parser.from_file(file_path)
    #print(parsed["metadata"]) 
    return parsed["content"] # To get the content of the file



file_path = "Resp Tract Inf TBL_Students.ppt"  
#file_path  = Path(file_path)
print(file_path)
print(get_data_tikka(file_path))
