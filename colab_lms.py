import diff_match_patch as dmp_module
global DEBUG_LOCAL
DEBUG_LOCAL = False
PATH_CASES = 'https://raw.githubusercontent.com/rilopez3/colab_lms/solemne1_2023/cases_urls.txt'

###################################################################################################################################
import io, sys, traceback, hashlib, urllib.request
from IPython.core.display import display, HTML

# Obtiene url de los cases
def get_case_path(preg):
  global DEBUG_LOCAL
  global PATH_CASES
  cases = {}
  if DEBUG_LOCAL:
    f = open('cases_urls.txt','r')
  else:
    f = urllib.request.urlopen(PATH_CASES)
  for l in f.readlines():
    if not DEBUG_LOCAL:
      l = l.decode("utf-8")
    l = l.strip().split(',')
    cases[l[0]] = l[1]
  if preg in cases:
    return cases[preg]
  return None

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

# Lee un archivo de case y retorna case en formato de diccionario
def read_cases(fileurl):
  global DEBUG_LOCAL
  cases = []
  if fileurl:
    try:
      if DEBUG_LOCAL:
        f = open(fileurl,'r')
      else:
        f = urllib.request.urlopen(fileurl)
      if DEBUG_LOCAL:
        lineas = f.readlines()
      else:
        lineas = []
        for l in f.readlines():
          l = l.decode("utf-8")
          lineas.append(l)
      cases = parse_case(lineas)
    except Exception as e:
      print(traceback.format_exc())
  return cases

# Corre el test de una pregunta
def run_test(preg):
  try:
    global SYSTEM_OUTPUT_CONTROL
    ##############################################################################
    SYSTEM_OUTPUT_CONTROL = '<div class="output_cont">'
    print_system('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"/>')
    print_system('<script src="https://code.jquery.com/jquery-3.7.0.slim.min.js"></script>')

    cases = read_cases(get_case_path(preg))
    assert len(cases) > 0, "Error al cargar los cases.\nFAVOR CONTACTAR A COORDINACION"

    pub = 0
    t_pub = 0
    sec = 0
    t_sec = 0
    student_code = get_student_code(preg)

    assert student_code, "Error al cargar la respuesta del estudiante.\nVERIFICA QUE LA PRIMERA LINEA DE LA CELDA DONDE SE ENCUENTRA TU RESPUESTA ES "# <P$>", DONDE $ ES EL NUMERO DE LA PREGUNTA. \nFAVOR CONTACTAR A COORDINACION"

    if cases['PREG']:
      print_system('<div class="title_preg">'+cases['PREG']+'</div>')
    if cases['CASES']:
      for case in cases['CASES']:
        if case['TYPE'].lower() == 'publico':
          pub += run_case(case, student_code)
          t_pub += 1
        elif case['TYPE'].lower() == 'secreto':
          sec += run_case(case, student_code)
          t_sec += 1

      total_pub = 'PUBLICOS = '+str(pub)+'/'+str(t_pub)
      total_sec = 'SECRETOS = '+str(sec)+'/'+str(t_sec)

      print_system('''<div class="res_preg"><p>RESULTADO</p>
        <li>''' + total_pub + '''</li>
        <li>''' + total_sec + '''</li></div>''')
    else:
      print_system('<div class="error"><p>Error en archivo de cases, informar a soporte.</p></div>')

    print_system('''<style>
      .output_cont{
        width:600px;
        background:white;
        padding: 10px;
      }
      .title_preg{
        font-weight: bold;
        font-size: 20px;
        text-align: center;
        padding: 20px;
        border-bottom: 1px solid black;
        color: #1e1e1e;
      }
      .section_case {
        border-bottom: 1px solid black;
        padding: 5px 20px;
        color: #1e1e1e;
      }
      .section_case p{
        font-size: 14px;
        font-weight: bold;
        color: #1e1e1e;
      }
      .section_case li{
        font-size: 12px;
        list-style-type: disclosure-closed;
        padding-left: 10px;
      }
      .res_preg{
        padding: 5px 20px;
        font-size: 15px;
        color: #1e1e1e;
      }
      .res_preg p{
        font-weight: bold;
        text-align: center;
      }
      .res_preg li{
        list-style-type: none;
        padding-left: 10px;
        text-align: center;
        font-weight: bold;
      }
      .mode_hidden{
        display: none;
      }
      .cluster_title{
        font-size: 16px;
        font-weight: bold;
        padding: 7px;
        font-style: italic;
        border-bottom: 1px solid black;
        cursor: pointer;
        user-select: none;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        display: flex;
        justify-content: space-between;
        color: #1e1e1e;
      }
      .cluster_title span:first-child {
          align-self: flex-start;
      }
      .cluster_title span:last-child {
          align-self: flex-end;
      }
      .raw_case{
        cursor:pointer;
        font-weight: bold;
        margin: 5px 0;
        font-size: 12px;
      }
      .raw_text{
        word-wrap: break-word;
        font-weight: lighter;
      }
      .raw_hidden{
        display: none;
        overflow: hidden;
        word-wrap: unset;
      }
      .missing_text{
        background: #70da7075;
        color: darkgreen;
      }
      .extra_text{
        background: #da707075;
        color: #5e0000;
      }
          </style>
          <script>

      $(".raw_case").click(function() {
          $(this).find(".raw_text").toggleClass('raw_hidden')
      });

      $(".cluster_title").click(function() {
        let $nextElement = $(this).next();
        if($nextElement && $nextElement.hasClass('case_cluster')) {
            $nextElement.toggleClass('mode_hidden');
        }
        let $iconElement = $(this).find("#toggleIcon");
        $iconElement.toggleClass('fa-chevron-down fa-chevron-up');
      });

      </script>''')
    print_system('</div>')
    display(HTML(SYSTEM_OUTPUT_CONTROL))
  except Exception as e:
    print(traceback.format_exc())

# Conversor dinamico a formato str
def push_str(val):
  if type(val) == type(1):
    return str(val)
  if type(val) == type(0.5):
    return str(val)
  if type(val) == type([]):
    return '[' + ', '.join([ push_str(i) for i in val ]) + ']'
  if type(val) == type(True):
    return str(val)
  if val == None:
    return 'None'
  return val

# Nueva funcion de input que reemplaza a la de los alumnos
def new_input(*args):
  global INTERNAL_COUNTER_INPUT
  global STUDENT_OUTPUT_CONTROL
  global INTERNAL_INPUT_CONTROL
  if args:
    new_print(args[0])
  if INTERNAL_COUNTER_INPUT >= len(INTERNAL_INPUT_CONTROL):
    return None
  INTERNAL_COUNTER_INPUT += 1
  return INTERNAL_INPUT_CONTROL[INTERNAL_COUNTER_INPUT - 1]

# Nueva funcion de print que reemplaza a la de los alumnos
def new_print(*args, sep = ' ', end = '\n'):
  global STUDENT_OUTPUT_CONTROL
  output = sep.join([ push_str(val) for val in args]) + end
  STUDENT_OUTPUT_CONTROL += output

# Nueva funcion de print para el print de systema a formato html
def print_system(*args, sep = ' ', end = ''):
  global SYSTEM_OUTPUT_CONTROL
  output = sep.join([ push_str(val) for val in args]) + end
  SYSTEM_OUTPUT_CONTROL += output

# Reemplaza funciones IO base
def redirect_io(code):
  return code.replace('input','new_input').replace('print','new_print')

# Obtener codigo del estudiante
def get_student_code(pregunta):
  all_cells = list(get_ipython().history_manager.get_range())
  for cell in all_cells[::-1]:
    if cell[2].strip().startswith(f'# <{pregunta}>') or cell[2].strip().startswith(f'#<{pregunta}>'):
      return clean_code(redirect_io(cell[2]))
  return None

# Limpia caracteres unicode
def clean_code(student_code):
  to_clean = [
    ['\xa0',' '],
  ]
  for row in to_clean:
    student_code = student_code.replace(row[0], row[1])
  return student_code

def run_case(case, student_code):
  global INTERNAL_INPUT_CONTROL
  global INTERNAL_COUNTER_INPUT
  global STUDENT_OUTPUT_CONTROL
  global SYSTEM_OUTPUT_CONTROL
  #################################################################
  INTERNAL_INPUT_CONTROL = case['INPUT'].split(',')
  INTERNAL_COUNTER_INPUT = 0
  STUDENT_OUTPUT_CONTROL = ''

  print_system('<div class="cluster_title">')
  print_system('<span>'+case['NAME'].upper() + ' ' + case['TYPE'].upper()+'</span>')

  estado = 0
  estado_msg = 'ERROR'
  error_message = None
  try:
    exec(redirect_io(case['PRECODE']))
    exec(student_code)
    exec(redirect_io(case['CODE']))

    if case['TYPE'].lower() == 'secreto':
      STUDENT_OUTPUT_CONTROL = hashlib.md5( STUDENT_OUTPUT_CONTROL.encode()).hexdigest()
      case['OUTPUT'] = case['OUTPUT'].strip()

    estado, estado_msg = [1 ,'CORRECTO'] if STUDENT_OUTPUT_CONTROL == case['OUTPUT'] else [0 , 'INCORRECTO']

  except Exception as e:
    error_message = traceback.format_exc()

  print_system('<span>ESTADO - ', estado_msg,'</span>')

  if case['TYPE'].lower() == 'publico':
    print_system('<i id="toggleIcon" class="fas fa-chevron-down"></i>')
  else:
    print_system('<i class="fas fa-chevron-down"></i>')

  print_system('</div>')

  if error_message:
    print_system('<div class="case_cluster mode_hidden">')
    print_system('<div class="section_case"><p>ERROR</p>')
    print_system('<span>', error_message,'</span>')
    print_system('</div>')
    print_system('</div>')


  if case['TYPE'].lower() == 'publico':
    print_system('<div class="case_cluster mode_hidden">')

    if( case['INPUT'].strip() != '' ):
      print_system('<div class="section_case"><p>INPUT</p>')
      for i in case['INPUT'].strip().split(','):
        print_system('<li>', i,'</li>')
      print_system('</div>')

    if( case['CODE'].strip() != '' ):
      print_system('<div class="section_case"><p>CODE</p>')
      for i in case['CODE'].strip().split('\n'):
        print_system('<li>', i,'</li>')
      print_system('</div>')

    print_system('<div class="section_case"><p>RECIBIDO</p>')
    for i in STUDENT_OUTPUT_CONTROL.split('\n'):
      print_system('<li>', i,'</li>')
    print_system('<div class="raw_case">Texto sin formato:<div class="raw_text raw_hidden">',repr(STUDENT_OUTPUT_CONTROL),'</div></div>')
    print_system('</div>')

    print_system('<div class="section_case"><p>ESPERADO</p>')
    for i in case['OUTPUT'].split('\n'):
      print_system('<li>', i,'</li>')
    print_system('<div class="raw_case">Texto sin formato:<div class="raw_text raw_hidden">',repr(case['OUTPUT']),'</div></div>')
    print_system('</div>')

    if not estado:
      diferencias = char_diff_checker(STUDENT_OUTPUT_CONTROL, case['OUTPUT'])
      print_system('<div class="section_case"><p>DIFERENCIAS</p>')
      print_system('<div>Los caracteres en color rojo corresponden a los que sobran en tu respuesta, mientras que los caracteres en las zonas verdes son aquellos que faltan.</div><hr>')
      print_system(diferencias.replace('\n','<br>'))
      print_system('<br></div>')


    print_system('</div>')

  if case['TYPE'].lower() == 'secreto':
    print_system('<div class="case_cluster mode_hidden">')

    if( case['INPUT'].strip() != '' ):
      print_system('<div class="section_case"><p>INPUT</p>')
      for i in case['INPUT'].strip().split(','):
        print_system('<li>', i,'</li>')
      print_system('</div>')

    print_system('</div>')

  return estado

def char_diff_checker(student_code, esperado):
    dmp = dmp_module.diff_match_patch()

    diffs = dmp.diff_main(student_code, esperado)
    dmp.diff_cleanupSemantic(diffs)

    diff_result = ''
    for op, data in diffs:
        if op == dmp.DIFF_EQUAL:
            diff_result += data
        elif op == dmp.DIFF_DELETE:
            diff_result += f'<span class="extra_text">{data}</span>'
        elif op == dmp.DIFF_INSERT:
            diff_result += f'<span class="missing_text">{data}</span>'

    return diff_result