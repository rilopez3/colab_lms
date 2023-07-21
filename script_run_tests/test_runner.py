import io, sys, hashlib

PATH_TESTS = "../../tests/" # link a la carpeta tests de github

def get_cell(pregunta):
  
  all_cells = list(get_ipython().history_manager.get_range(stop=-1))
  all_cells_content = [cell[2] for cell in all_cells]

  cell_to_change = None

  for cell in all_cells_content:
    if cell.startswith(f'# <{pregunta}>'):
      cell_to_change = cell
      break
  
  student_code = cell_to_change.split('\n')
  
  return student_code


def execute_code(student_code, input_list):
  code_to_execute = inputs_assign(student_code, input_list)
  
  old_stdout = sys.stdout
  new_stdout = io.StringIO()
  sys.stdout = new_stdout # redirijo salida del sistema

  exec(code_to_execute)

  student = sys.stdout.getvalue().strip()

  sys.stdout = old_stdout # vuelvo a dejar la salida del sistema

  return student
  


def inputs_assign(student_code, input_list):
  cells_to_execute = []
  for line in student_code:
    if "input()" in line:
      try:
        cells_to_execute.append(line.replace('input()', str(input_list.pop(0))))
      except:
        print('Estás pidiendo más inputs de los que deberías')

    else:
      cells_to_execute.append(line)
  
  return '\n'.join(cells_to_execute)


def get_tests_cases(colab, pregunta):
  tests_cases = {}
  tests_in_folder = True
  path = PATH_TESTS + str(colab) + '/' + str(pregunta) + '/'
  i = 1
  
  while tests_in_folder:
    try:
      with open(path + str(i) + "/input.txt") as input_stream:
        input_lines = input_stream.readlines()
        case_type = input_lines.pop(0)
      with open(path + str(i) + "/output.txt") as output_stream:
        output_lines = output_stream.readlines()
      tests_cases[i]= {'case_type': case_type.strip()[1],'input': clean_list_file(input_lines), 'output': clean_list_file(output_lines)}
    except:
      tests_in_folder = False
    i += 1
  
  return tests_cases


def execute_tests_cases(student_code, tests_cases):
  n = 50
  passed = 0
  not_passed = 0

  for n_test in range(1, len(tests_cases.values()) + 1):
    print(f'{"*" * ((n - 8) // 2)} TEST {n_test} {"*" * ((n - 8) // 2)}\n')

    print('-' * (n // 3), 'INPUT')
    print("\n".join(tests_cases[n_test]['input']))

    print('-' * (n // 3), 'OUTPUT ESTUDIANTE')
    output = execute_code(student_code, tests_cases[n_test]['input'])
    print(output)
    output = output.split()

    result = compare_outputs(tests_cases[n_test]['case_type'], tests_cases[n_test]['output'], output)
    
    print('-' * (n // 3), 'OUTPUT ESPERADO')
    print("\n".join(tests_cases[n_test]['output']))
    
    print('-' * (n // 3), 'RESULTADO')
    if result:
      print("CORRECTO")
      passed += 1
    else:
      print("INCORRECTO")
      not_passed += 1

    print('*' * n)
    print("\n")
  
  print(f'TESTS CASES PASADOS: {passed}/{not_passed+passed}')


def compare_outputs(case_type, output_test_case, student_output):
  if case_type == 'P':
    return output_test_case == student_output
  elif case_type == 'S':
    return output_test_case[0] == encode_output_md5(student_output)



def run_tests(colab, pregunta):
  student_code = get_cell(pregunta)

  tests_cases = get_tests_cases(colab, pregunta)
  execute_tests_cases(student_code, tests_cases)


def clean_list_file(list_file):
  return [i.strip() for i in list_file]


def output_list_str_elements(output_list):
  return [str(i) for i in output_list]


def encode_output_md5(output):
  str_output = "\n".join(output)
  return hashlib.md5(str_output.encode()).hexdigest()


# created by MFMG99