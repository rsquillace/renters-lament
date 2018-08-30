from browser import document, html, ajax, window
import json
industry_name = document['industry_name']
year = document['year']
bedroom = document['bedroom']
table = document['table']

from urllib.parse import quote

def update_table(req):
   if req.status==200: #or req.status==0:
       table.html = req.text
   else:
       print (req.text)

def get_table(ev):
    req = ajax.ajax()
    req.bind('complete', update_table)
    # send a POST request to the url
    url = f'/table/{get_selected(industry_name)}/{get_selected(year)}/{get_selected(bedroom)}'
    url = quote(url)
    req.open('GET', url, True)
    #req.set_header('content-type','application/x-www-form-urlencoded')
    # send data as a dictionary
    req.send()

def update_map(req):
    if req.status==200: #or req.status==0:
        zipcode_shapes = window.get_zipcode_shapes()
        zipcode_colors = json.loads(req.text)
        for zipcode_shape in zipcode_shapes:
            zipcode = window.get_zipcode(zipcode_shape)
            zipcode_color = zipcode_colors.get(str(zipcode))
            if zipcode_color:
                zipcode_shape.setStyle({'color': zipcode_color})
            else:
                zipcode_shape.setStyle({'color': 'black'})
    else:
        print(req.text)

def get_map_data(ev):
    req = ajax.ajax()
    req.bind("complete", update_map)
    url = f'map_data/{get_selected(industry_name)}/{get_selected(year)}/{get_selected(bedroom)}'
    url = quote(url)
    req.open('GET', url, True)
    req.send()

def get_selected(sel):
    return next(option.value for option in sel if option.selected)

industry_name.bind("change", get_table)
year.bind("change", get_table)
bedroom.bind("change", get_table)
industry_name.bind("change", get_map_data)
year.bind("change", get_map_data)
bedroom.bind("change", get_map_data)
