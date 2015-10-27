###
#Funciones
###
import re, math, os
import numpy
import matplotlib.pyplot as plt
from optparse import OptionParser, OptionGroup


###Expresiones Regulares###
VERSION = "0.0.1"
num = ".*[0-9]"
abc = ".*[a-z]"
ABC = ".*[A-Z]"
esp = ".*[^0-9a-zA-Z]"
AbC = "(.*[a-z]+?.*[A-Z]|.*[A-Z].*[a-z])"
abnum = "(.*[0-9].*[a-z]|.*[a-z].*[0-9])"
ABnum = "(.*[0-9].*[A-Z]|.*[A-Z].*[0-9])"
espnum = "(.*[^0-9a-zA-Z].*[0-9]|.*[0-9].*[^0-9a-zA-Z])"
###END###


def load(lfile, ltype, lfile2=None ):
	###
	#REVISAR NONE PARA ENTRADA TIPO4
	#AGREGAR EXCEPCION DE ABRIR DOCUMENTO
	###
	archivo = open(lfile, "r")
	datos = archivo.readlines()
	if (datos[0].count(":")!=0 or ltype=="tp3"):
		if (ltype == "tp1"):	#User:pass
			usr, psw = [],[]
			for x in datos: 
				temp1, temp2 = x.replace("\n","").replace("\r","").split(":")
				usr.append(temp1)
				psw.append(temp2)
			return usr, psw
		elif (ltype == "tp2"):	#user:hash:pass
			usr, hsh, psw = [], [], []
			for x in datos: 
				temp1, temp2, temp3 = x.replace("\n","").replace("\r","").split(":")
				usr.append(temp1)
				hsh.append(temp2)
				psw.append(temp3)
			return usr, hsh, psw
		elif (ltype == "tp3"):	#pass
			psw = []
			for x in datos: 
				psw.append(x.replace("\n","").replace("\r",""))
			return psw
		else:
			print "[+] ERROR LOAD - NOT TYPE [+]"
	else: 
		print "[+] ERROR ESTRUCTURA DE ARCHIVO NO VALIDA [+]"

def siznumbers(lpassword):	#mayusculas, minusculas y numeros
	datos = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	#mns - Mns - mMs - Mmn - Mm - Mn - Ms - mn - ms - sn - M - m - n -s
	for x in lpassword:
		#x = x.replace("\n","")
		if re.match(abnum,x) and re.match(esp,x):
			datos[0] += 1	#mns
		elif(re.match(ABnum,x) and re.match(esp,x)):
			datos[1] += 1	#Mns
		elif re.match(AbC,x) and re.match(esp,x):
			datos[2] += 1	#mMs
		elif re.match(AbC,x) and re.match(num,x):
			datos[3] += 1	#Mmn 
		elif re.match(AbC,x):
			datos[4] += 1	#Mm
		elif re.match(ABnum,x):
			datos[5] += 1	#Mn
		elif re.match(ABC,x) and re.match(esp,x):
			datos[6] += 1	#Ms
		elif re.match(abnum,x):
			datos[7] += 1	#mn
		elif re.match(abc,x) and re.match(esp,x):
			datos[8] += 1	#ms
		elif re.match(espnum,x):
			datos[9] += 1	#sn
		elif re.match(ABC,x):
			datos[10] += 1	#M
		elif re.match(abc,x):
			datos[11] += 1	#m
		elif re.match(num,x):
			datos[12] += 1	#n
		elif re.match(esp,x):
			datos[13] += 1	#s
	return datos
	
def ordlen(lpassword):	#FUNCION DE LONGITUDES
	ordlpassword = sorted(lpassword, key = len)
	temp1 = len(ordlpassword[-1])
	listas = {}
	for x in ordlpassword:
		if (listas.keys().count(len(x))!=0): 
			listas[len(x)].append(x)
		else:
			listas[len(x)] = [x]
	return listas 	#retorna diccionario con longitudes

def repeat(lpassword):	#retorna una lista bidimensional con la password y su repeticion global
	repetidos = {}
	for x in lpassword:
		repetidos[x] = lpassword.count(x)
	datos = repetidos.items()
	datos.sort(key=lambda x: x[1], reverse = True)
	return datos 

def matchperce(luser, lpassword):	#Busca dentro de los datos(luser) coincidencias >=4 con las password
	temp1, temp2 = len(luser), len(lpassword)
	temp3 = min(temp1,temp2)
	h = temp3	#h
	result = []
	while h < temp3+1 and h >= 4:
		for x in range(0, (temp3+1)-h): 
			sbstr = luser[x:h+x]
			if (sbstr in lpassword):
				result.append([sbstr, lpassword, 0])
				h =temp3 + 2
				break
			elif (sbstr.lower() in lpassword.lower()):
				result.append([sbstr, lpassword, 1])
				h =temp3 + 2
				break
			elif (sbstr[::-1] in lpassword):
				result.append([sbstr, lpassword, 2])
				h =temp3 + 2
				break
			elif (sbstr[::-1].lower() in lpassword.lower()):
				result.append([sbstr, lpassword, 3])
				h =temp3 + 2
				break
		h = h-1
	return result 	#retornamos una lista bidimensional con las coincidencias

def savefile(name,path,datos):
	archivo = open(path+name,"w")
	for x in datos:
		archivo.write(x+"\n")
	archivo.close()

def graph1(datos): 	#Genera los graficos de la estructura de las password, grafico de torta
	labels = 'Min/Num/Esp', 'May/Num/Esp', 'May/Min/Esp', 'May/Min/Num', 'May/Min', 'May/Num', 'May/Esp', 'Min/Num', 'Min/Esp', 'Esp/Num', 'Mayuscula', 'Minuscula', 'Numerica', 'Especial'
	colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral','yellowgreen', 'gold', 'lightskyblue', 'lightcoral','yellowgreen', 'gold', 'lightskyblue', 'lightcoral','yellowgreen', 'gold', 'lightskyblue', 'lightcoral','yellowgreen', 'gold', 'lightskyblue', 'lightcoral','yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
	catshow = []
	f = []
	for x in range(0,len(datos)):
		if datos[x]!=0:
			catshow.append(labels[x])
			f.append(datos[x])
	part, pospart = max(f), f.index(max(f))
	f[pospart] = 0
	d, e = max(f), f.index(max(f))
	f[pospart] = part 
	zeros = numpy.zeros([len(f)], dtype="int").tolist()
	perce, suma = [], sum(f)
	
	for x in range(0,len(f)):
		if float(f[x]*100)/suma <4.0:
			zeros[x] = 0.7
	print zeros
	
	plt.pie(f, explode=zeros, labels=catshow, autopct='%1.1f%%', colors=colors, shadow=True, startangle=30)
	plt.axis('equal')
	plt.savefig('fig1.jpg', dpi = 100)
	plt.close()
	
def graph2(datos):	#Realiza el histograma de longitudes
	
	import numpy as np
	import matplotlib.patches as patches
	import matplotlib.path as path
	
	c = datos.keys()
	datos2 = []
	for x in c:
		datos2.append(len(datos[x]))

	fig, ax = plt.subplots()
	data = c
	n, bins = np.histogram(data, 60, (min(c)-0.5, max(c)+0.5))
	cont = 0

	for x in range(0,len(n)): 
		if n[x] == 1:
			n[x] = datos2[cont]
			cont +=1

	left = np.array(bins[:-1])
	right = np.array(bins[1:])
	bottom = np.zeros(len(left))
	top = bottom + n
	XY = np.array([[left,left,right,right], [bottom,top,top,bottom]]).T

	barpath = path.Path.make_compound_path_from_polys(XY)

	patch = patches.PathPatch(barpath, facecolor='green',edgecolor='grey', alpha=0.5)
	ax.add_patch(patch)

	ax.set_xlim(left[0], right[-1])
	ax.set_ylim(bottom.min(), top.max())
	plt.xticks(c)
	plt.xlabel('Longitud')
	plt.ylabel('Cantidad')
	plt.title(r'Histograma de Longitudes')
	plt.savefig('fig2.jpg', dpi = 100)
	plt.close()
	#plt.show()

def graph3(dato1, dato2):	#Muestra en porcentaje, el total de password crackeados
	labels = 'CRACKEADAS', 'NO-CRACKEADAS'
	colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']

	sizes = [dato1, dato2]
	explode = (0.1, 0.1) 

	plt.pie(sizes, explode=explode, labels=labels, colors=colors,
			autopct='%1.1f%%', shadow=True, startangle=90)
	plt.axis('equal')
	plt.savefig('fig3.jpg', dpi = 100)
	plt.close()
	#plt.show()

def graph4(datos, top):		#Funcion que grafica el TOP 20 de passwords mas usados
	import matplotlib.pyplot as plt; plt.rcdefaults()
	import numpy as np
	import matplotlib.pyplot as plt

	nom = []
	num = []
	for x in range(0,top):
		num.append(datos[x][1])
		nom.append(datos[x][0])

	y_pos = range(top)
	performance = num

	plt.barh(y_pos, performance, align='center', alpha=0.5, color="green",edgecolor='grey')
	plt.yticks(y_pos, nom)

	plt.xlabel('Repeticiones')
	plt.title('TOP 20 DE PASSWORDS MAS USADAS')
	plt.savefig('fig4.jpg', dpi = 100)
	plt.close()
	#plt.show()

def graph5(datos):	#Grafico de coincidencias entre datos del usuario y password
	labels = ['Exacto', 'Minuscula', 'Invertido', 'Invertido-Minuscula', 'Nombre', 'Cedula', 'Celular', 'Direccion', 'Cargo', 'Empresa', 'Email', "mes"]
	colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral','yellowgreen', 'gold', 'lightskyblue', 'lightcoral','yellowgreen', 'gold', 'lightskyblue', 'lightcoral','yellowgreen', 'gold', 'lightskyblue', 'lightcoral','yellowgreen', 'gold', 'lightskyblue', 'lightcoral','yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
	catshow = [0,0,0,0,0,0,0,0,0,0,0,0,0]
	lbels = []
	for x in range(0,len(datos)):
		catshow[datos[x][2]] += 1
	c = []
	for h in range(0,12):
		if catshow[h]!=0:
			lbels.append(labels[h])
			c.append(catshow[h])
	part, pospart = max(c), catshow.index(max(c))
	c[pospart] = 0
	d, e = max(c), c.index(max(c))
	c[pospart] = part 
	zeros = numpy.zeros([len(c)], dtype="int").tolist()
	zeros[pospart], zeros[e] = 0.1, 0.1
	
	plt.pie(c, explode=zeros, labels=lbels, autopct='%1.1f%%', colors=colors, shadow=True, startangle=80)
	plt.axis('equal')
	plt.xlabel('Un total de: '+str(len(datos))+' Coincidencias')
	plt.title('COINCIDENCIAS ENTRE DATOS DE USUARIO Y PASSWORD')
	plt.savefig('fig5.jpg', dpi = 100)
	plt.close()
	#plt.show()

if __name__ == "__main__":
	
	header = """
    %s
    __  __     __        __      ___   
   /\ \/\ \  /'__`\    /'_ `\   / __`\ 
   \ \ \_/ |/\ \L\.\_ /\ \L\ \ /\ \L\ \\
    \ \___/ \ \__/.\_\\\ \____ \\\ \____/
     \/__/   \/__/\/_/ \/___L\ \\/___/ 
                         /\____/       
                         \_/__/        
     investigaciones@cslcolombia.com
	"""%VERSION

	parser = OptionParser("%prog [options] input.txt\n\nType --help for more options", version="%prog "+VERSION)
	parser.add_option("-o", "--output", dest="out", help="Formato de salida\t", metavar="reporte", default="reporte")
	parser.add_option("-r", "--report", dest="report", type="int",help="Tipo de informe a generar\t", default="1", metavar="1")
	parser.add_option("-t", "--type", dest="tpe", type="int", help="Formato del archivo de entrada\t", default="3")
	parser.add_option("--top", dest="top", help="TOP de passwords usadas\t", metavar="50", default=50)

	(options, args) = parser.parse_args()
	print header
	
	if len(args)!=1:
		parser.error("[+] DEBE INGRESAR UN ARCHIVO DE ENTRADA [+]")
		exit(1)
	else:
		print "[*] INICIANDO [*]"
	
	#cargamos archivos
	user, pws, hsh = [],[],[]
	if options.tpe == 1:	#user:pass
		user, pws = load(args[0],"tp1")
	elif options.tpe == 2:	#user:hash:pass
		user, hsh, pws = load(args[0],"tp2")
	elif options.tpe == 3:	#pass
		pws = load(args[0],"tp3")
	else:
		parser.error("[+] Formato de archivo de entrada invalido[+]")
		exit(1)
	#END-LOAD
	
	#cargamos el tipo de reporte
	if options.report == 1: 
		#generando proyecto
		name = "Proyecto"+str(numpy.random.random_integers(100))
		os.mkdir(name)
		os.chdir(name)
		os.mkdir("Imagenes")
		os.mkdir("Data")
		#######END
		
	
		#ldata = load(data,typ)
		
		os.chdir("Imagenes")
		##Fig1
		fig1 = siznumbers(pws)
		#print fig1
		graph1(fig1)
		##END Fig1
		
		##Fig2
		fig2 = ordlen(pws)
		graph2(fig2)
		##END Fig2
		
		##Fig3
		graph3(len(pws),len(pws))
		##ENDFig3
		
		##Fig4
		fig4 = repeat(pws)
		#print fig4
		graph4(fig4,20)
		##END Fig4
		print "final"
	else:
		parser.error("[*]ERROR, debe ingresar un tipo de reporte valido[*]")
		exit(1)
