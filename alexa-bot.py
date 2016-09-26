#!/usr/bin/env python
''' 
Copyright (C) 2016  QuantiKa14 Servicios Integrales S.L
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
#############################################
#AUTHOR: JORGE WEBSEC                      ##
#TWITTER: @JORGEWEBSEC                     ##
#BLOG: BOTENTRIANA.WORDPRESS.COM           ##
#EMAIL: JORGE@QUANTIKA14.COM               ##
#############################################
#***********BOT PRINCIPAL******************##
#BOT NAME: ALEXA                           ##
#BOT ENCARGADO DE DETECTAR WORDPRESS       ## 
#Y VERSIONES EN ALEXA RANKING              ##
#############################################
import re, csv, socket,time, httplib
from bs4 import BeautifulSoup
from socket import error as SocketError
import errno
import mechanize, cookielib

br = mechanize.Browser()
cj = cookielib.LWPCookieJar() 
br.set_cookiejar(cj) 
br.set_handle_equiv( True ) 
br.set_handle_gzip( True ) 
br.set_handle_redirect( True ) 
br.set_handle_referer( True ) 
br.set_handle_robots( False ) 
br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1 ) 
br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' ) ] 

class colores:
    HEADER = '\033[95m'
    azul = '\033[94m'
    verde = '\033[92m'
    alerta = '\033[93m'
    FAIL = '\033[91m'
    normal = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

def detect_wp(html, dominio):
	soup = BeautifulSoup(html, "html.parser")
	#Buscamos wp-content en el html
	try:
		if html.find("/wp-content/")>0:
			return True
		else:
	#Buscamos links con xmlrpc.php
			links = soup.findAll("link")
			for l in links:
				if "xmlrpc.php" in str(l):
					return True
				else:
					continue
	except:
		pass

def get_Version(url):
	url = url + "/readme.html"
	tried = 0
	try:
		html = br.open(url, timeout=20).read()
		soup = BeautifulSoup(html, "html.parser")
		v = soup.find_all('h1', {'id':"logo"})
		v = remove_tags(str(v))
		return v
	except (mechanize.HTTPError,mechanize.URLError) as e:
		if isinstance(e,mechanize.HTTPError):
			print e
			tried += 1
			time.sleep(30)
		if tried > 4:
			exit()
		else:
			print e
			tried += 1
			time.sleep(30)
		if tried > 4:
			exit()
	except httplib.BadStatusLine as e:
		print e

def main():
	reader = csv.reader(open('top-1m.csv', 'rb'))
	for index,row in enumerate(reader):
		url = "http://" + row[1]
		tried = 0
		try:
			html = br.open(url,timeout=20).read()
		except (mechanize.HTTPError,mechanize.URLError) as e:
			if isinstance(e,mechanize.HTTPError):
				print e
				tried += 1
				time.sleep(30)
			if tried > 4:
				exit()
			else:
				print e
				tried += 1
				time.sleep(30)
			if tried > 4:
				exit()
		except httplib.BadStatusLine as e:
			print e
		if detect_wp(html, row[1]):
			print colores.verde + "[+][INFO]{WP DETECT} -> " + row[1] + " [I]: " + row[0] + colores.normal
			version = get_Version(url)
			if version:
				print colores.verde + "    [!][version]" + version + colores.normal
				f = open("wps.txt", "a")
				f.write(url + "," + version + "\n")
				f.close()
			else:
				print colores.alerta + "    [!][WARNING] NO FOUND VERSION" + colores.normal
		else:
			print colores.azul + "[-][INFO] NO WP -> " + row[1] + " [I]: " + row[0] + colores.normal
      
if __name__ == '__main__':  
	main()
