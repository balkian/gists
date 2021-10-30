from __future__ import print_function
import csv
from jinja2 import Template

with open('PC Members.tsv') as f:
    contacts = csv.DictReader(f, delimiter='\t')

    with open('index.j2') as templatefile:
        template = Template(templatefile.read())

    with open('web/index.html', 'w') as web:
        web.write(template.render(contacts=contacts))
