
from PIL.ExifTags import TAGS
from PIL import Image
from io import StringIO
from PyPDF2 import PdfFileReader
import re
import os
import glob

path_img = "/home/shanks/Documentos/AppZurich/Docs/Traducir/IMG_Traducir/preview.jpg"

path_pdf = '/home/shanks/Documentos/CHV_Consulting/ReadingTextEcuador/data_pdf/data'
image_list = []

def funcion_contar_pdfs(path):
  '''
  @path este es el atributo de la ruta a leer pdf
  Esta funcion devuelve el numero total de ficheros en una ruta
  '''
  contador = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
  return print('El total de archivos pdfs es de: '+str(contador)+ ' en la ruta : ' + path )

def reading_etl_text(path):
    lista_add_text = []
    str_clean = str
    for file in glob.glob(path + "/*.pdf"):
        # print(file)
        if file.endswith('.pdf'):
            fileReader = PdfFileReader(open(file, "rb"))
            count = 0
            count = fileReader.numPages
            print('Paginas TOTALES en el PDF :' + str(count) + ' en el fichero: ' + file)
            while count >= 0:
                count -= 1
                pageObj = fileReader.getPage(count)
                text = pageObj.extractText()
                text = text.lstrip('\r\n') \
                    .replace('\n', ' ') \
                    .replace('  ', '') \
                    .replace('COMPROBANTE DE RETENCIÓN No', 'COMPROBANTE_DE_RETENCIÓN_Nro:') \
                    .replace('Contribuyente Especial Nro ', 'Contribuyente_Especial_Nro:') \
                    .replace('-', '') \
                    .replace(': ', ':')
                # .replace('/','')#corta las fechas sin formato
                text = re.sub('[-.]', '', text) \
                    .replace(': ', ':').split(' ')
                str_clean = text
                cabeceras = ['Comprobante','Numero','Fecha_emision','Ejercicio_fiscal','Base_retencion','Impuesto',
                             'Porcentaje_retencion','valor_retenido']
                indices = all_indices('FACTURA',str_clean)
                dict_facturas = create_dict_list(cabeceras,indices)
                # añadimos a lista_add el texto
                lista_add_text.append(str_clean+indices)
                data_clean = re.findall(r'[\w\.-]+:[\w]+', str_clean)

                print(data_clean)
            num = re.findall(r'[0-9]+', text)
            print(num)
        else:
            print("not in format")

    return lista_add_text,data_clean

def all_indices(value, qlist):
    indices = [i for i in range(len(qlist)) if qlist[i] == value]
    list_ouput = []
    for cont in indices:
        cont+=7
        list_ouput.append(qlist[indices[0]:cont],)
        count=0
    return list_ouput

def create_dict_list(alist,blist):
    for i in blist:
        zip_iterator = zip(alist,i)
        a_dictionary = dict(zip_iterator)
    return a_dictionary


def load_data_img(path_img):
    '''Metodo de carga de IMG para extraer datos de una IMG
    @path_img : parametro de entrada de la img.
    '''
    image = Image.open(path_img)
    exifdata = image.getexif()
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        print(tag_id)
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes
        if isinstance(data, bytes):
            data = data.decode()
        print(f"{tag:25}: {data}")



def convert_title_to_filename(title):
    filename = title.lower()
    filename = filename.replace(' ', '_')
    return filename


def split_to_title_and_pagenum(table_of_contents_entry):
    title_and_pagenum = table_of_contents_entry.strip()

    title = None
    pagenum = None

    if len(title_and_pagenum) > 0:
        if title_and_pagenum[-1].isdigit():
            i = -2
            while title_and_pagenum[i].isdigit():
                i -= 1

            title = title_and_pagenum[:i].strip()
            pagenum = int(title_and_pagenum[i:].strip())

    return title, pagenum



reading_etl_text(path_pdf)
funcion_contar_pdfs(path_pdf)
#print(pytesseract.image_to_string(r'/home/shanks/Documentos/AppZurich/Docs/Traducir/IMG_Traducir/preview.jpg'))


