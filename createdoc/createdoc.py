import os
import sys
import json
import jinja2
import subprocess
import pdflatex
from pdflatex import PDFLaTeX

#os.chdir('pyt')
jinja_args = json.loads(open(sys.argv[1], encoding='utf-8').read())
template_filename = sys.argv[2]
output_filename = sys.argv[3]
if output_filename.endswith('.pdf'):
    output_filename = output_filename[:-4]


latex_jinja_env = jinja2.Environment(
    block_start_string=r'\BLOCK{',
    block_end_string='}',
    variable_start_string=r'\VAR{',
    variable_end_string='}',
    comment_start_string=r'\#{',
    comment_end_string='}',
    line_statement_prefix='%-',
    line_comment_prefix='%#',
    trim_blocks=True,
    autoescape=False,
    loader=jinja2.FileSystemLoader(os.path.abspath('.'))
)

template = latex_jinja_env.get_template(template_filename)

doc = template.render(jinja_args)

with open(f'{output_filename}.tex', 'w', encoding='utf-8') as output:
    output.write(doc)

'''subprocess.check_call([
    'latexmk',
    '-xelatex',
    '-halt-on-error',
    '-synctex=0',
    #'-quiet'
    '-interaction=batchmode',
    f'{output_filename}.tex'
], shell=True)
subprocess.check_call([
    'latexmk',
    '-c',
    f'{output_filename}.tex'
], shell=True)'''

