import traceback
import urllib.request
import hashlib
import threading


def csv_format( data:list):
  return ','.join([ str(i) for i in data])

# Obtiene url de los cases
def get_case_path(preg):
  global PATH_CASES
  cases = {}
  f = urllib.request.urlopen(PATH_CASES)
  for l in f.readlines():
    l = l.decode("utf-8")
    l = l.strip().split(',')
    cases[l[0]] = l[1]
  if preg in cases:
    return cases[preg]
  return None

# Lee un archivo de case y retorna case en formato de diccionario
def read_cases(fileurl):
  cases = []
  if fileurl:
    try:
      f = urllib.request.urlopen(fileurl)
      lineas = []
      for l in f.readlines():
        l = l.decode("utf-8")
        lineas.append(l)
      cases = parse_case(lineas)
    except Exception as e:
      print(traceback.format_exc())
  return cases

# Limpia caracteres unicode
def clean_code(student_code):
  to_clean = [
    ['\xa0',' '],
  ]
  for row in to_clean:
    student_code = student_code.replace(row[0], row[1])
  return student_code

# Obtiene parse de un archivo de cases
def parse_case(lineas):
  data = {'PREG':'', 'CASES':[]}
  template = {'NAME':'', 'TYPE':'', 'PRECODE': '', 'INPUT': '', 'CODE': '', 'OUTPUT': ''}
  caso_actual  = None
  for linea in lineas:
    if linea.startswith('%'):
      clave_actual = linea[1:].strip()
      if clave_actual == 'NAME':
        if caso_actual is not None:
          data['CASES'].append(caso_actual)
        caso_actual = template.copy()
    else:
      if clave_actual == 'PREG':
        data['PREG'] += linea
      else:
        caso_actual[clave_actual] += linea
  if caso_actual is not None:
    data['CASES'].append(caso_actual)
  data['PREG'] = data['PREG'].strip()
  for case in data['CASES']:
    case['NAME'] = case['NAME'].strip()
    case['TYPE'] = case['TYPE'].strip()
  return data

# Nueva funcion de print que reemplaza a la de los alumnos
def new_print(*args, sep = " ", end = "\n"):
  global STUDENT_OUTPUT_CONTROL
  output = sep.join([ push_str(val) for val in args]) + end
  STUDENT_OUTPUT_CONTROL += output

# Conversor dinamico a formato str
def push_str(val):
  if type(val) == type(1):
    return str(val)
  if type(val) == type(0.5):
    return str(val)
  if type(val) == type([]):
    return '[' + ', '.join([ push_str2(i) for i in val ]) + ']'
  if type(val) == type(True):
    return str(val)
  if val == None:
    return 'None'
  return val

#conversor interno para listas
def push_str2(val):
  if type(val) == type(1):
    return str(val)
  if type(val) == type(0.5):
    return str(val)
  if type(val) == type([]):
    return '[' + ', '.join([ push_str2(i) for i in val ]) + ']'
  if type(val) == type(True):
    return str(val)
  if val == None:
    return 'None'
  return repr(val)

# Reemplaza funciones IO base
def redirect_io(code):
  return code.replace('input','new_input').replace('print','new_print')

# Obtener codigo del estudiante desde archivo ipynb
def get_student_code_from_file(pregunta, raw_student_code):
  all_cells = raw_student_code
  for cell in all_cells[::-1]:
    if cell.strip().startswith(f'# <{pregunta}>') or cell.strip().startswith(f'#<{pregunta}>'):
      return clean_code(redirect_io(cell))
  return ''


# @timeout(30)
def ejecutar_codigo(precode, student_code, code):
  exec(precode)
  exec(student_code)
  exec(code)


def run_case_with_timeout(precode, student_code, code, timeout):
  def run_with_timeout():
    try:
      exec(precode)
      exec(student_code)
      exec(code)
    except Exception as e:
      pass

  thread = threading.Thread(target=run_with_timeout)
  thread.start()
  thread.join(timeout=timeout)

  if thread.is_alive():
    thread._stop()
    return 0


def eval_case(case, student_code):
  global INTERNAL_INPUT_CONTROL
  global INTERNAL_COUNTER_INPUT
  global STUDENT_OUTPUT_CONTROL
  #################################################################
  INTERNAL_INPUT_CONTROL = case['INPUT'].split(',')
  INTERNAL_COUNTER_INPUT = 0
  STUDENT_OUTPUT_CONTROL = ''

  case['OUTPUT'] = case['OUTPUT'].replace('\r', '')

  estado = 0
  estado_msg = 'ERROR'

  try:
    run_case_with_timeout( redirect_io(case['PRECODE']), student_code, redirect_io(case['CODE']), 3 )
  except Exception as e:
    print('TimeOut' , case['NAME'], case['TYPE'].upper())


  if case['TYPE'].lower() == 'secreto':
    STUDENT_OUTPUT_CONTROL = hashlib.md5( STUDENT_OUTPUT_CONTROL.strip().encode()).hexdigest()
    case['OUTPUT'] = case['OUTPUT'].strip()

  estado, estado_msg = [1 ,'CORRECTO'] if STUDENT_OUTPUT_CONTROL == case['OUTPUT'] else [0 , 'INCORRECTO']

  return estado

def eval_test(preg, raw_student_code):
  try:
    global SYSTEM_OUTPUT_CONTROL
    ##############################################################################

    cases = read_cases(get_case_path(preg))
    assert len(cases) > 0, "Error al cargar los cases.\nFAVOR CONTACTAR A COORDINACION"

    pub = 0
    t_pub = 0
    sec = 0
    t_sec = 0
    student_code = get_student_code_from_file(preg, raw_student_code)
    
    if cases['CASES']:
      for case in cases['CASES']:
        if case['TYPE'].lower() == 'publico':
          pub += eval_case(case, student_code)
          t_pub += 1
        if case['TYPE'].lower() == 'secreto':
          sec += eval_case(case, student_code)
          t_sec += 1

      return (pub, t_pub, sec, t_sec )

  except Exception as e:
    print(traceback.format_exc())
