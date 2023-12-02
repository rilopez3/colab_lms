
# LOS ARCHIVOS A EVALUAR DEBEN ESTAR EN EL SIGUIENTE DIRECTORIO
# ./res/seccion/[ alumno_1.ipynb, alumno_2.ipynb, alumno_3.ipynb ... ]
global PATH_CASES
PATH_CASES = 'https://raw.githubusercontent.com/rilopez3/colab_lms/examen_2023/cases_urls.txt'

import glob
from json import load
from datetime import datetime
import urllib.request
import csv
import os

exec(open('colab_lms_eval.py').read())

cases = {}
f = urllib.request.urlopen(PATH_CASES)
for l in f.readlines():
  l = l.decode("utf-8")
  l = l.strip().split(',')
  cases[l[0]] = l[1]


protected = [
  'get_ipython', 'exit', 'quit', 'glob', 'i', 'io', 'sys', 'traceback', 'hashlib',
  'urllib', 'load', 'filename', 'fp', 'nb', 
  'data', 'csv_format', 'filepath','datetime','globales','cases','PATH_CASES',
  'get_case_path','protected','header',
  'read_cases','clean_code','parse_case','new_print','push_str','push_str2','redirect_io','get_student_code_from_file',
  'eval_case','eval_test','res_file',
  'threading','run_case_with_timeout','archivos_listos','os'
]

if os.path.exists('res/results.csv'):
  with open('res/results.csv', 'r') as res_file:
    csv_reader = csv.reader(res_file)
    archivos_listos = [row[0] for row in csv_reader]
else:
      archivos_listos = []

with open('res/results.csv', 'a') as res_file:
  if len( archivos_listos) == 0:
    header = ['path', 'filename','name','seccion'] + [ preg + i for preg in cases.keys() for i in ['_pub','_t_pub','_sec','_t_sec']   ] + ['TOTAL_pub', 'TOTAL_cases_pub', 'total_sec', 'total_cases_sec']    
    print(csv_format(header), file=res_file, flush=True)
    ##############################################################################

  for filepath in glob.glob('**/*.ipynb', recursive=True):

    if filepath not in archivos_listos:
      with open(filepath, encoding="utf8") as fp:
          globales = [i for i in globals().keys() if not i.startswith('_') and not i in protected]
          for i in globales:
            exec(i + ' = None')
          name = ' '.join(filepath.split('\\')[2].split('_')[:2]).upper() 
          seccion = filepath.split('\\')[1]

          data = [ filepath, filepath.split('\\')[2], name , seccion ]
          print(name,'('+seccion+')','->')
          nb = load(fp)
          student_code = []
          final_pub = 0
          final_total_pub = 0
          final_sec = 0
          final_total_sec = 0
          
          for cell in nb['cells']:
              if cell['cell_type'] == 'code':
                  cell_code = ''.join(line for line in cell['source'])
                  if '# NO MODIFICAR ESTA CELDA' not in cell_code:
                    #print(''.join(cell['source']))
                    student_code.append(''.join(cell['source']))
          
          for preg in cases.keys():
            p, tp,s,ts = eval_test(preg, student_code)
            final_pub += p
            final_total_pub += tp
            final_sec += s
            final_total_sec += ts

            data += [p, tp,s,ts]
          
          data += [final_pub,final_total_pub,final_sec,final_total_sec]
          # print(data)
          print(csv_format(data), file = res_file, flush=True)
