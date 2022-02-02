
from flask import Flask,render_template,request,session, redirect, url_for
import mysql.connector
from biciklista import Biciklista

app = Flask(__name__)
app.config['SECRET_KEY'] = "RAF2021-2022"
mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="", # ako niste nista menjali u phpmyadminu ovo su standardni
    # username i password
	database="januar2022" # iz phpmyadmin 
    )

@app.route('/')
def index():
    return 'Hello world'


@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'GET':
		return render_template(
			'register.html'
		)

	prijava = request.form['prijava']
	pol = request.form['pol']
	sifra = request.form['sifra']
	potvrda = request.form['potvrda']
	vreme_prva_etapa = request.form['vreme_prva_etapa']
	vreme_druga_etapa = request.form['vreme_druga_etapa']

	cursor = mydb.cursor(prepared = True)
	sql = "SELECT * FROM biciklisti WHERE broj_prijave = ?"
	values = (prijava, )
	cursor.execute(sql, values)

	res = cursor.fetchone()

	if res != None:
		return render_template(
			'register.html',
			broj_prijave_error = 'Vec postoji nalog sa tom prijavom!'
		)

	if sifra != potvrda:
		return render_template(
			'register.html',
			potvrda_error = 'Sifre se ne poklapaju!'
		)

	if int(vreme_prva_etapa) <= 0:
		return render_template(
			'register.html',
			prva_etapa_error = 'Vreme za etapu mora biti pozitivno!'
		)

	if int(vreme_druga_etapa) <= 0:
		return render_template(
			'register.html',
			druga_etapa_error = 'Vreme za etapu mora biti pozitivno!'
		)

	cursor = mydb.cursor(prepared = True)
	sql = "INSERT INTO biciklisti VALUES (null, ?, ?, ?, ?, ?)"
	values = (prijava, sifra, pol, vreme_prva_etapa, vreme_druga_etapa)
	cursor.execute(sql, values)

	mydb.commit()

	return redirect(
		url_for('show_all')
	)


@app.route('/show_all')
def show_all():
	
	cursor = mydb.cursor(prepared = True)
	sql = "SELECT * FROM biciklisti"
	cursor.execute(sql)

	res = cursor.fetchall()

	if res == None:
		return 'Ne postoji ni jedan biciklista u bazi!'

	n = len(res)
	res = list(res)

	biciklisti = []

	for i in range(n):
		res[i] = dekodiraj(res[i])
		id_bicikliste = res[i][0]
		prijava = res[i][1]
		sifra = res[i][2]
		pol = res[i][3]
		prva_etapa = res[i][4]
		druga_etapa = res[i][5]

		biciklista = Biciklista(id_bicikliste, prijava, pol, sifra, prva_etapa, druga_etapa)
		biciklisti.append(biciklista)


	return render_template(
		'show_all.html',
		biciklisti = biciklisti
	)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template(
			'login.html'
		)

	prijava = request.form['prijava']
	sifra = request.form['sifra']

	cursor = mydb.cursor(prepared = True)
	sql = "SELECT * FROM biciklisti WHERE broj_prijave = ?"
	values = (prijava, )
	cursor.execute(sql, values)

	res = cursor.fetchone()


	if res == None:
		return render_template(
			'login.html',
			prijava_error = 'Ne postoji nalog sa tom prijavom!'
		)

	res = dekodiraj(res)

	if res[2] != sifra:
		return render_template(
			'login.html',
			sifra_error = 'Pogresna sifra!'
		)

	session['prijava'] = prijava

	return redirect(
		url_for('show_all')
	)
	

@app.route('/logout')
def logout():
	if 'prijava' not in session:
		return redirect(
			url_for('show_all')
		)

	session.pop('prijava')
	return redirect(
		url_for('login')
	)


@app.route('/profil/<broj_prijave>')
def profil(broj_prijave):

	cursor = mydb.cursor(prepared = True)
	sql = "SELECT * FROM biciklisti WHERE broj_prijave = ?"
	values = (broj_prijave, )
	cursor.execute(sql, values)

	res = cursor.fetchone()

	if res == None:
		return redirect(
			url_for('show_all')
		)

	res = dekodiraj(res)

	id_bicikliste = res[0]
	prijava = res[1]
	sifra = res[2]
	pol = res[3]
	prva_etapa = res[4]
	druga_etapa = res[5]

	biciklista = Biciklista(id_bicikliste, prijava, pol, sifra, prva_etapa, druga_etapa)

	return render_template(
		'profil.html',
		biciklista = biciklista
	)


@app.route('/rang_lista_po_etapi/<broj_etape>')
def rang_lista(broj_etape):

	if broj_etape not in ['1', '2']:
		return redirect(
			url_for('show_all')
		)

	if broj_etape == '1':
		cursor = mydb.cursor(prepared = True)
		sql = "SELECT * FROM biciklisti ORDER BY etapa_jedan;"
		cursor.execute(sql)

	if broj_etape == '2':
		cursor = mydb.cursor(prepared = True)
		sql = "SELECT * FROM biciklisti ORDER BY etapa_dva;"
		cursor.execute(sql)

	res = cursor.fetchall()

	n = len(res)
	res = list(res)

	biciklisti = []

	for i in range(n):
		res[i] = dekodiraj(res[i])
		id_bicikliste = res[i][0]
		prijava = res[i][1]
		sifra = res[i][2]
		pol = res[i][3]
		prva_etapa = res[i][4]
		druga_etapa = res[i][5]

		biciklista = Biciklista(id_bicikliste, prijava, pol, sifra, prva_etapa, druga_etapa)
		biciklisti.append(biciklista)
	
	return render_template(
		'rang_lista.html',
		biciklisti = biciklisti
	)


def dekodiraj(data):
	n = len(data)
	data = list(data)

	for i in range(n):
		if isinstance(data[i], bytearray):
			data[i] = data[i].decode()

	return data

app.run(debug=True)
