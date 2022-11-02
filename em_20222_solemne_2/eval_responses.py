import glob

from json import load
from datetime import datetime
debug = True
protected = ['In', 'Out', 'get_ipython', 'exit', 'quit', 'glob', 'i', 'io', 'sys', 'traceback', 'hashlib',
             'urllib', 'get_case', 'run_case', 'read_cases', 'run_test', 'clean_exec', 'eval_preg',
             'get_variables', 'eval_case', 'get_preg', 'protected', 'clean_globals',
             'load', 'filename', 'fp', 'nb', 'cell', 'cell_code', 'student_code',
             'data', 'detail_res', 'resume', 'pub', 't_pub', 'sec', 't_sec', 'res_file', 'csv_format', 'debug',
             'evaluation_variables', 'header','filepath','datetime','globales']

exec(open('colab_lms.py').read())
exec(open('colab_lms_eval.py').read())

with open('res/results '+ (str(datetime.now()).replace('-','_').replace(':','')[:15]) +'.csv', 'w') as res_file:
    header = ['path', 'filename'] + evaluation_variables() + ['pub_ok', 'pub_total', 'sec_ok', 'sec_total']
    print(csv_format(header), file=res_file)
    ##############################################################################
    for filepath in glob.glob('**/*.ipynb', recursive=True):

        with open(filepath) as fp:
            nb = load(fp)
            student_code = ''
            for cell in nb['cells']:
                if cell['cell_type'] == 'code':
                    cell_code = ''.join(line for line in cell['source'])
                    if '# NO MODIFICAR ESTA CELDA' not in cell_code:
                        student_code += cell_code + '\n'
        ############################################################################
        if debug:
            print('ARCHIVO', filepath)
            print('-' * 100)

        filename = filepath.split('\\')[-1]

        if debug:
            print('VARIABLES GLOBALES NONEADAS', flush=True)
        globales = list(globals().keys())
        for i in globales:
            if i[0] != '_' and i not in protected:
                if debug:
                    print(i)
                exec(i + ' = None')

        if debug:
            print('', flush=True)
            print('-' * 100, flush=True)
        ############################################################################
        exec(student_code)
        exec(get_variables())

        detail_res = []

        for i in get_preg():
            detail_res.append([i] + eval_preg(i))

        data['results'] = detail_res

        if debug:
            print('DETALLE', flush=True)
            print('-' * 100, flush=True)
            print(data, flush=True)
            print('', flush=True)
            print('-' * 100, flush=True)
        ############################################################################
        resume = [filepath, filename] + data['vars']
        pub = t_pub = sec = t_sec = 0
        for i in data['results']:
            pub += i[1]
            t_pub += i[2]
            sec += i[3]
            t_sec += i[4]

        resume += [pub, t_pub, sec, t_sec]
        if debug:
            print('TOTAL', flush=True)
            print('-' * 100, flush=True)

            print(resume)
            print('', flush=True)
            print('=' * 100, flush=True)
            print('', flush=True)
        print(csv_format(resume), file=res_file)
