from docxtpl import DocxTemplate, InlineImage
from . import data_format


def contract_generate(data):
    obj = data_format.format(data)
    print(obj)

    # sourcePath = 'rezal/apps/main/templates/docx/entity_contract_template.docx'
    # filename = obj['path'].replace('entity_contract_db/', '')
    # exitPath = f'media/{obj["path"]}/{filename}.docx'

    sourcePath = 'static/doc/travel_template.docx'
    filename = obj['path']
    exitPath = f'media/contracts/{filename}.docx'

    doc = DocxTemplate(sourcePath)

    # out_str = ''
    # for item in obj['order_name']:
    #     out_str = out_str + item + ', '
    # obj['order_name'] = out_str[:-2]

    context = {'id': obj['id'],
               'cr_d': obj['creation_date_word'][0],
               'cr_m': obj['creation_date_word'][1],
               'cr_y': obj['creation_date_word'][2],
               'country': obj['country'],
               'document': obj['document'],
               'serial': obj['serial'],
               'number': obj['number'],
               'client_name': obj['client_name'],
               'client_name_output': obj['client_name_output'],
               'towns': obj['towns'],
               'dateStart': obj['dateStart'],
               'dateStop': obj['dateStop'],
               'comments': obj['comments'],
               'amount': obj['amount'],
               'worker_name': obj['worker_name'],
               'hotels': obj['hotels'],
               }
    doc.render(context)
    doc.save(exitPath)

    return exitPath
