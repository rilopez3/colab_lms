import io, sys, traceback, hashlib, urllib.request

def get_case(preg):
  cases = {}
  f = urllib.request.urlopen('https://raw.githubusercontent.com/rilopez3/colab_lms/feat/set0_2023/guia1_2023/cases_urls.txt')
  for l in f.readlines():
    l = l.decode("utf-8")
    l = l.strip().split(',')
    cases[l[0]] = l[1]
  if preg in cases:
    return cases[preg]
  return None

def run_case(subname, tipo, code, expected):

  print(subname.upper() + ' ' + tipo.upper() )
  print('-' * 75)
  if tipo == 'Publico':
    print('INPUT')
    print(code)
    print('-' * 75)

  old_stdout = sys.stdout 
  new_stdout = io.StringIO() 
  sys.stdout = new_stdout
  estado = 0
  try:
    exec(code)
    res = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout

    if tipo == 'Secreto':
      res = hashlib.md5( res.encode()).hexdigest() 

    print('ESTADO - ', 'OK' if res == expected else 'Incorrecto' )
    if tipo == 'Publico':  
      print('-' * 75)
      print('RECIBIDO')
      print(res)
      
    estado = 1 if res == expected else 0 

  except Exception as e:
    sys.stdout = old_stdout
    print('ESTADO - ERROR' )
    print('-' * 75)
    print('ERROR')
    print(e)

  if tipo == 'Publico':
    print('-' * 75)
    print('ESPERADO')
    print(expected)
  print()
  print('=' * 75)
  print()

  return estado

def read_cases(fileurl):
  cases = []
  nombre = ''
  if fileurl:
    try:
      f = urllib.request.urlopen(fileurl)
      case = []
      temp = ''
      for l in f.readlines():
        l = l.decode("utf-8") 
        if l[:2] == '#F':
          nombre = l[2:].strip()
        elif l[:2] == '#P':
          if case:
            case.append(temp.strip())
            cases.append(case)
          case = [ l[2:].strip(), 'Publico' ]
        elif l[:2] == '#S':
          if case:
            case.append(temp.strip())
            cases.append(case)
          case = [ l[2:].strip(), 'Secreto' ]
        elif l.strip() == '%CODE':
          temp = ''
        elif l.strip() == '%OUTPUT':
          case.append(temp.strip())
          temp = ''
        else:
          temp += l
      if case:
        case.append(temp.strip())
        cases.append(case)

    except Exception as e:
      print(e)
  return nombre, cases

def run_test(preg):
  nombre, cases = read_cases(get_case(preg))
  pub = 0
  t_pub = 0
  sec = 0
  t_sec = 0
  if nombre:
    print('*'*75)
    print()
    print(nombre.upper().center(75,' '))
    print()
    print('*'*75)
    print()
  if cases:
    for i, val in enumerate(cases):
      subname, tipo, code, res = val
      if tipo == 'Publico':
        pub += run_case(subname, tipo, code, res)
        t_pub += 1
      elif tipo == 'Secreto':
        sec += run_case(subname, tipo, code, res)
        t_sec += 1
    
    total_pub = 'PUBLICOS = '+str(pub)+'/'+str(t_pub)
    total_sec = 'SECRETOS = '+str(sec)+'/'+str(t_sec)

    print('RESULTADO'.center(75,' '))
    print(total_pub.center(75,' '))
    print(total_sec.center(75,' '))
    
    print()
    print('*'*75)
  else:
    print('Error en archivo de cases, informar a soporte')
