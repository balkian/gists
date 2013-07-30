import mechanize, cookielib
from BeautifulSoup import BeautifulSoup
import re, os

def get_image(tag, folder):
    if not os.path.isdir(folder):
        os.makedirs(folder)
    print image
    filename = os.path.join(folder+'/'+url.split('/')[-1])
    data = br.open(url).read()
    br.back()
    save = open(filename, 'wb')
    save.write(data)
    save.close()

br=mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#Individuales
r = br.open('http://www.etsit.upm.es/fotospromo85.html')
br.select_form(nr=0)
br.form['user']='entregadiplomas'
br.form['pass']='entrega2013'
r = br.submit()
r_tags = BeautifulSoup(r)
link = r_tags(text=re.compile(r'individual'))[0].parent['href']
galery = BeautifulSoup(br.open(link))
images_tags = galery(href=re.compile(r'pics/.{10}.jpg'))
folder = 'individuales'
for image in images_tags:
    url = image['href']
    get_image(url, folder)

# Ahora las de grupo
link=r_tags(text=re.compile(r'grupo'))[0].parent['href']
galery = BeautifulSoup(br.open(link))
images_tags = galery(href=re.compile(r'pics/.{10}.jpg'))
folder = 'grupo'
for image in images_tags:
    url = image['href']
    get_image(url, folder)