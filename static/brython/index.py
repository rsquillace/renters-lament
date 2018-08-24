from browser import document, html, ajax
industry_name = document['industry_name']
year = document['year']
table = document['table']

from urllib.parse import quote

def update_table(req):
   if req.status==200 or req.status==0:
       table.html = req.text
   else:
       table.html = "error "+req.text

def get_table(ev):
    req = ajax.ajax()
    req.bind('complete', update_table)
    # send a POST request to the url
    url = f'/table/{get_selected(industry_name)}/{get_selected(year)}'
    url = quote(url)
    req.open('GET', url, True)
    #req.set_header('content-type','application/x-www-form-urlencoded')
    # send data as a dictionary
    req.send()

def get_selected(sel):
    return next(option.value for option in sel if option.selected)


industry_name.bind("change", get_table)
year.bind("change", get_table)
