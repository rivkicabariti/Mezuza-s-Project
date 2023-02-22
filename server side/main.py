from PIL import Image
import os
import image_quality as iqc
import cleanNoise as c
import Separation_of_letters as s
import To_classify
import Proofreading_a_mezuza as p
from fpdf import FPDF
import codecs



def SaveAsPdf(path,mezuza_name):
    # save FPDF() class into a variable pdf
    pdf = FPDF()
    # Add a page
    pdf.add_page()
    # set style and size of font that you want in the pdf
    #https://stackoverflow.com/questions/68807685/writing-hebrew-words-to-pdf-file
    #pdf.add_font("DeJaVu",'',r'C:\Users\1\PycharmProjects\MyFinalProject\venv\Lib\site-packages\ttf\DejaVuSans.ttf',uni=True)  #בבית
    pdf.add_font("DeJaVu", '', r'C:\Users\328905559\PycharmProjects\Rivki_Final_Progect\venv\Lib\site-packages\pygame\tests\fixtures\fonts\dejavu-fonts-ttf-2.37\ttf\DejaVuSans.ttf',
           uni=True)
    pdf.set_font("DeJaVu", size=13)
    # open the text file in read mode

    #f = codecs.open(f"{path}", "r", encoding="UTF-8")
    f = codecs.open(f"images/results/{mezuza_name}t.txt", "r", encoding="UTF-8")
    # insert the texts in pdf
    for x in f:
        pdf.cell(200, 10, txt=x, ln=1, align='L')
    # save the pdf with name .pdf
    # mezuza_name = os.path.splitext(path)[0]
    # mezuza_name = os.path.basename(mezuza_name)
    pdf.output(fr"images/results/{mezuza_name}.pdf")



def MainFunc(path):
    image_mezuza = Image.open(path)
    path = iqc.main_image_quality(path)  # הכנת המזוזה לחיתוך שורות ואותיות
    print('חותך לשורות')
    path_to_my_lines = s.main_separation_to_lines(path)  # חיתוך ל22 שורות
    print('מנקה את השורות')
    c.main_cleaner(path_to_my_lines)  # על מנת לנקות את השורות
    print('חותך לאותיות')
    path_to_my_letters = s.main_separation_to_letters(path_to_my_lines)  # שליחת השורות הנקיות לחיתוך אותיות
    print('מסווג')
    dict = To_classify.MainClassification(path_to_my_letters)  # שליחת האותיות לזיהוי
    mezuza_name = os.path.splitext(path)[0]
    mezuza_name = os.path.basename(mezuza_name)
    print('מגיה '+mezuza_name)
    path_to_result_in_txt=p.MainChecker(mezuza_name,dict)  # שליחת האותיות להגהה
    SaveAsPdf(path_to_result_in_txt,mezuza_name)
    print('גמר')

#MainFunc('images/source_mezuzot/mezuzac.png')
#SaveAsPdf(r'images/results/mezuza1.txt')
