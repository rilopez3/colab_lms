import io, sys, traceback, hashlib, urllib.request

def get_case(preg):
  cases = {}
  with open('cases_urls.txt','r') as f:
    for l in f.readlines():
      l = l.strip().split(',')
      cases[l[0]] = l[1]
  if preg in cases:
    return cases[preg]
  return None

def clean_exec():
  var_clean = ['nombre','correo_escuela_militar','crear_tropas','agregar_unidades','mover_unidades','total_unidades','reasignar_unidades']
  clean_text = ''
  for i in var_clean:
    clean_text += i + '= None\n'
  return clean_text

def eval_preg(preg):
  nombre, cases = read_cases(get_case(preg))
  pub = 0
  t_pub = 0
  sec = 0
  t_sec = 0
  obs = ''
  if cases:
    for i, val in enumerate(cases):
      subname, tipo, code, res = val
      if tipo == 'Publico':
        point, comentario = eval_case(subname, tipo, code, res)
        pub += point
        if comentario not in obs:
          obs += comentario
        t_pub += 1
      elif tipo == 'Secreto':
        point, comentario = eval_case(subname, tipo, code, res)
        sec += point
        if comentario not in obs:
          obs += comentario
        t_sec += 1
    return [pub, t_pub, sec, t_sec, obs]
  return None

def evaluation_variables():
  return ['nombre','correo_escuela_militar']

def get_variables():
  var_to_get = evaluation_variables()
  
  var_code = 'data = {\'vars\':['
  for i in var_to_get:
    var_code += str(i) + ','
  var_code += ']}'

  return var_code

def eval_case(subname, tipo, code, expected):
  old_stdout = sys.stdout 
  new_stdout = io.StringIO() 
  sys.stdout = new_stdout
  estado = 0
  comentario = ''
  try:
    exec(code)
    res = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout

    if tipo == 'Secreto':
      res = hashlib.md5( res.encode()).hexdigest() 
   
    estado = 1 if res == expected else 0 

  except Exception as e:
    sys.stdout = old_stdout
    comentario = 'ERROR ' + str(e) + '\n' 

  return estado, comentario

def get_preg():
  preg = []
  with open('cases_urls.txt','r') as f:
    for l in f.readlines():
      l = l.strip().split(',')
      preg.append( l[0] )
  return preg

def csv_format( data:list):
  return ','.join([ str(i) for i in data])
