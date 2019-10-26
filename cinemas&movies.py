from flask import Flask, request
from psycopg2 import connect

def connect_cinemas_db():
    db_cnx = connect(user='postgres', password='coderslab', host='127.0.0.1',database='cinemas_db')
    db_cnx.autocommit = True
    return db_cnx

html_cinemas = """
            <!doctype html>
    <html>
    <head>
        <title>Cinemas</title>
        <meta charset="utf-8">
    </head>

    <body>

        <!-- cinemas -->
        <h1>KINA</h1>
        <a href="http://localhost:5000/">Strona główna</a>
        <a href="http://localhost:5000/movies">Filmy</a>
        <a href="http://localhost:5000/tickets">Bilety</a>
        <a href="http://localhost:5000/payments">Płatności</a>
        <div>
            <form class="cinema_form" method="post" action="/cinemas">
                <label>DODAJ KINO</label><br>
                <label>Podaj nazwę kina:</label>
                <input name="name" type="text" maxlength="255" placeholder="kino"/><br>
                <label>Podaj adres kina:</label>
                <input name="address" type="text" maxlength="255" placeholder="adres"/><br>
                <button type="submit" name="action" value="add">Dodaj</button><br>
                <br>
                <input name="search" type="text" maxlength="255" placeholder="Szukaj kina...">
                <button type="submit" name="action" value="search">Szukaj</button><br>
            </form>
        </div>
    </body>
    </html>
            
            
"""



html_movies = """
<!doctype html>
    <html>
    <head>
        <title>Movies</title>
        <meta charset="utf-8">
    </head>

    <body>

        <!-- movies -->
        <h1>FILMY</h1>
        <a href="http://localhost:5000/">Strona główna</a>
        <a href="http://localhost:5000/cinemas">Kina</a>
        <a href="http://localhost:5000/tickets">Bilety</a>
        <a href="http://localhost:5000/payments">Płatności</a>
        <div>
            <form class="movies_form" method="post" action="/movies">
                <label>DODAJ FILM</label><br>
                <label>Podaj tytuł filmu:</label>
                <input name="name" type="text" maxlength="255" placeholder="tytuł film..."/><br>
                <label>Podaj opis filmu:</label>
                <textarea name="description" type="text" maxlength="255" cols="40" rows="8" placeholder="opis filmu..."/></textarea><br>
                <label>Podaj ocenę filmu</label>
                <input name="rating" type="number" step="0.1" min="0" max="10"/><br>
                <button type="submit" name="action" value="add">Dodaj</button><br>
            
                <br>
            
                <input name="search" type="text" maxlength="255" placeholder="Szukaj kina...">
                <button type="submit" name="action" value="search">Szukaj</button><br>
                <label>Szukanie po:</label>
                <label>nazwie</label>
                <input type="radio" name="sort" value="s_name" checked>
                <label>ratingu</label>
                <input type="radio" name="sort" value="s_rating">
                
            </form>
            
        </div>
    </body>
    </html>
"""

html_tickets = """
<!doctype html>
    <html>
    <head>
        <title>Tickets</title>
        <meta charset="utf-8">
    </head>

    <body>

        <!-- tickets -->
        <h1>BILETY</h1>
        <a href="http://localhost:5000/">Strona główna</a>
        <a href="http://localhost:5000/movies">Filmy</a>
        <a href="http://localhost:5000/cinemas">Kina</a>
        <a href="http://localhost:5000/payments">Płatności</a>
        <div>
            <form class="tickets_form" method="post" action="/tickets">
                <label>DODAWANIE BILETÓW</label><br>
                <label>Ilość biletów</label>
                <input name="quantity" type="number" min="1"/><br>
                <label>Rodzaj biletu:</label>
                <select name="price">
                    <option value="adults">Dorośli - 18,50 zł</option>
                    <option value="children">Dzieci - 12 zł</option>
                </select>
                <br>
                <button type="submit" name="action" value="add">Dodaj</button><br>
                                
            </form>
        </div>
    </body>
    </html>
            
            
"""

html_payments = """
<!doctype html>
    <html>
    <head>
        <title>Payments</title>
        <meta charset="utf-8">
    </head>

    <body>

        <!-- payments -->
        <h1>PŁATNOŚCI</h1>
        <a href="http://localhost:5000/">Strona główna</a>
        <a href="http://localhost:5000/movies">Filmy</a>
        <a href="http://localhost:5000/cinemas">Kina</a>
        <a href="http://localhost:5000/tickets">Bilety</a>
        <div>
            <form class="payments_form" method="post" action="/payments">
                <label>DODAWANIE PŁATNOŚCI</label><br>
                <label>Data płatności</label>
                <input name="pay_date" type="date"/><br>
                <label>Rodzaj płatności:</label>
                <select name="pay_type">
                    <option value="card">Karta kredytowa/płatnicza</option>
                    <option value="cash">Gotówka</option>
                </select>
                <br>
                <button type="submit" name="action" value="add">Dodaj</button><br>
            
                <br>
            
                <label>Znajdź płatność</label><br>
                <br>
                <label>Starszą niż...
                <input name="older" type="date">
                <button type="submit" name="action" value="search_1">Szukaj</button><br>
                <label>Nowszą niż...</label>
                <input name="newest" type="date">
                <button type="submit" name="action" value="search_2">Szukaj</button><br>
                <label>W zakresie od </label>
                <input name="search_from" type="date">
                <label> do </label>
                <input name="search_to" type="date">
                <button type="submit" name="action" value="search_3">Szukaj</button><br>
                <label>W dniu...</label>
                <input name="search" type="date">
                <button type="submit" name="action" value="search_4">Szukaj</button><br>                
            </form>
        
"""


def cinema_site():
    html_parts = []
    html_parts.append(html_cinemas)
    cnx = connect_cinemas_db()
    cursor = cnx.cursor()
    cursor.execute('select id, name, address from cinema;')
    html_parts.append('<p>Lista kin:</p>')
    html_parts.append('<ul>')

    for cin in cursor:
        l = '<form class="cinema" method="post" action="/cinemas">' \
            '   <li>{}, {}' \
                    ' <input id="{}" type="hidden" value="{}" name="id_delete">' \
                    ' <button type="submit" name="action" value="del">Usuń</button>' \
                '</li>' \
            '</form>'.format(cin[1], cin[2], cin[0], cin[0])
        html_parts.append(l)
    html_parts.append('</ul>')
    html_parts.append('</div></body></html>')
    cnx.close()
    html = '\n'.join(html_parts)
    return html

def movies_site():
    html_parts = []
    html_parts.append(html_movies)
    cnx = connect_cinemas_db()
    cursor = cnx.cursor()
    cursor.execute('select id, name, description, rating from movie;')
    html_parts.append('<p>Lista filmów:</p>')
    html_parts.append('<ul>')

    for cin in cursor:
        l = '<form class="movie" method="post" action="/movies">' \
            '   <li>{}, {}, {}' \
            ' <input id="{}" type="hidden" value="{}" name="id_delete">' \
            ' <button type="submit" name="action" value="del">Usuń</button>' \
            '</li>' \
            '</form>'.format(cin[1], cin[2], cin[3], cin[0], cin[0])
        html_parts.append(l)
    html_parts.append('</ul>')
    html_parts.append('</div></body></html>')
    cnx.close()
    html = '\n'.join(html_parts)
    return html


def ticket_site():
    html_parts = []
    html_parts.append(html_tickets)
    cnx = connect_cinemas_db()
    cursor = cnx.cursor()
    cursor.execute('select id, quantity, price from ticket;')
    html_parts.append('<p>Lista biletów:</p>')
    html_parts.append('<ul>')

    for cin in cursor:
        l = '<form class="ticket" method="post" action="/tickets">' \
            '   <li>Ilość: {}, suma: {} zł.' \
                    ' <input id="{}" type="hidden" value="{}" name="id_delete">' \
                    ' <button type="submit" name="action" value="del">Usuń</button>' \
                '</li>' \
            '</form>'.format(cin[1], cin[2], cin[0], cin[0])
        html_parts.append(l)
    html_parts.append('</ul>')
    html_parts.append('</div></body></html>')
    cnx.close()
    html = '\n'.join(html_parts)
    return html

def payments_site():
    html_parts = []
    html_parts.append(html_payments)
    cnx = connect_cinemas_db()
    cursor = cnx.cursor()
    cursor.execute('select id, type, date from payment;')
    html_parts.append('<p>Lista płatności:</p>')
    html_parts.append('<ul>')

    for cin in cursor:
        l = '<form method="post" action="/payments">' \
            '<li>Rodzaj płatności: {}. Data płatności: {}. ' \
                '<input id="{}" type="hidden" value="{}" name="id_delete">' \
                '<button type="submit" name="action" value="del">Usuń</button>' \
            '</li>' \
            '</form>'.format(cin[1], cin[2], cin[0], cin[0], cin[0])
        html_parts.append(l)
    html_parts.append('</ul>')
    html_parts.append('</div></body></html>')
    cnx.close()
    html = '\n'.join(html_parts)
    return html



app = Flask(__name__)


@app.route("/")
def main():
    return """
        <!doctype html>
<html>
<head>
    <title>Choice</title>
    <meta charset="utf-8">
</head>

<body>
    <h1>APLIKACJA WEBOWA DO OPERACJI NA BAZIE CINEMAS_DB</h1>
    <h3>Wybierz jedną z opcji</h3>
        <ul>
            <li>
                <a href="http://localhost:5000/cinemas">Kina</a>
            </li>
            <li>
                <a href="http://localhost:5000/movies">Filmy</a>
            </li>
            <li>
                <a href="http://localhost:5000/tickets">Bilety</a>
            </li>
            <li>
                <a href="http://localhost:5000/payments">Płatności</a>
            </li>
        </ul>  

</body>
</html>
        """

@app.route("/cinemas", methods=['GET', 'POST'])
def cinema():
    if request.method == 'GET':
        return cinema_site()
    else:
        if request.form['action'] == 'add':
            name = request.form['name']
            address = request.form['address']
            if len(name) == 0:
                return """
                <html>
                <head>
                    <title>Cinemas</title>
                    <meta charset="utf-8">
                </head>
                    <body>
                        <p>Błąd: za krótka nazwa kina</p>
                        <a href='http://localhost:5000/cinemas'>Wróć do strony wyszukiwania</a>
                    </body>
                </html>
                """
            if len(address) == 0:
                return """
                <html>
                <head>
                    <title>Cinemas</title>
                    <meta charset="utf-8">
                </head>
                    <body>
                        <p>Błąd: za krótki adres kina</p>
                        <a href='http://localhost:5000/cinemas'>Wróć do strony wyszukiwania</a>
                    </body>
                </html>
                """

            cnx = connect_cinemas_db()
            cursor = cnx.cursor()
            sql = """
            insert into cinema(name, address) values(%s, %s);
            """
            cursor.execute(sql, (name, address))
            cursor.close()
            cnx.close()
            return cinema_site()
        if request.form['action'] == 'search':
            s = request.form['search']
            html_parts = []
            html_parts.append(html_cinemas)
            html_parts.append('<a href="http://localhost:5000/cinemas">Usuń wyniki wyszukiwania</a>')
            cnx = connect_cinemas_db()
            cursor = cnx.cursor()
            sql = "select name, address from cinema where name ilike %s;"
            cursor.execute(sql, ['%{}%'.format(s)])
            html_parts.append('<p>Lista kin:</p>')
            html_parts.append('<ul>')

            for cin in cursor:
                l = '<li>{}, {}</li>'.format(cin[0], cin[1])
                html_parts.append(l)
            html_parts.append('</ul>')
            cursor.close()
            cnx.close()
            html = '\n'.join(html_parts)
            return html
        if request.form['action'] == 'del':
            id = request.form['id_delete']
            cnx = connect_cinemas_db()
            cursor = cnx.cursor()
            cursor.execute("delete from cinema where id=%s;", [id])
            cursor.close()
            cnx.close()
            return cinema_site()


@app.route("/movies", methods=['GET', 'POST'])
def movie():
    if request.method == 'GET':
        return movies_site()
    else:
        if request.form['action'] == 'add':
            name = request.form['name']
            description = request.form['description']
            rating = request.form['rating']
            if len(name) == 0:
                return """
                <html>
                <head>
                    <title>Movies</title>
                    <meta charset="utf-8">
                </head>
                    <body>
                        <p>Błąd: za krótka nazwa filmu</p>
                        <a href='http://localhost:5000/movies'>Wróć do formularza dodawania Filmy</a>
                    </body>
                </html>
                """
            if len(description) == 0:
                return """
                <html>
                <head>
                    <title>Movies</title>
                    <meta charset="utf-8">
                </head>
                    <body>
                        <p>Błąd: za krótki opis filmu</p>
                        <a href='http://localhost:5000/movies'>Wróć do formularza dodawania Filmy</a>
                    </body>
                </html>
                """
            if len(rating) == 0:
                return """
                <html>
                <head>
                    <title>Movies</title>
                    <meta charset="utf-8">
                </head>
                    <body>
                        <p>Błąd: ocena filmu musi być określona</p>
                        <a href='http://localhost:5000/movies'>Wróć do formularza dodawania Filmy</a>
                    </body>
                </html>
                """


            cnx = connect_cinemas_db()
            cursor = cnx.cursor()
            sql = """
            insert into movie(name, description, rating) values(%s, %s, %s);
            """
            cursor.execute(sql, (name, description, rating))
            cursor.close()
            cnx.close()
            return movies_site()
        if request.form['action'] == 'search':
            s = request.form['search']
            sort = request.form['sort']

            if sort == 's_name':
                html_parts = []
                html_parts.append(html_movies)
                html_parts.append('<a href="http://localhost:5000/movies">Usuń wyniki wyszukiwania</a>')
                cnx = connect_cinemas_db()
                cursor = cnx.cursor()
                sql = "select name, description, rating from movie where name ilike %s;"
                cursor.execute(sql, ['%{}%'.format(s)])
                html_parts.append('<p>Lista odnalezionych po nazwie filmów:</p>')
                html_parts.append('<ul>')

                for cin in cursor:
                    l = '<li>{}, {}, {}</li>'.format(cin[0], cin[1], cin[2])
                    html_parts.append(l)
                html_parts.append('</ul>')
                cursor.close()
                cnx.close()
                html = '\n'.join(html_parts)
                return html

            if sort == 's_rating':
                
                try:
                    html_parts = []
                    html_parts.append(html_movies)
                    html_parts.append('<a href="http://localhost:5000/movies">Usuń wyniki wyszukiwania</a>')
                    cnx = connect_cinemas_db()
                    cursor = cnx.cursor()
                    sql = "select name, description, rating from movie where rating = %s;"
                    cursor.execute(sql, [float(s)])
                    html_parts.append('<p>Lista odnalezionych po ocenie filmów:</p>')
                    html_parts.append('<ul>')

                    for cin in cursor:
                        l = '<li>{}, {}, {}</li>'.format(cin[0], cin[1], cin[2])
                        html_parts.append(l)
                    html_parts.append('</ul>')
                    cursor.close()
                    cnx.close()
                    html = '\n'.join(html_parts)
                    return html
                except ValueError:
                    return """
                    <html>
                <head>
                    <title>Movies</title>
                    <meta charset="utf-8">
                </head>
                    <body>
                        <p>Błąd: przy wyszukiwaniu po ocenie należy wpisać liczbę</p>
                        <a href='http://localhost:5000/movies'>Wróć do formularza dodawania filmów</a>
                    </body>
                </html>
                    """

        if request.form['action'] == 'del':
            id = request.form['id_delete']
            cnx = connect_cinemas_db()
            cursor = cnx.cursor()
            cursor.execute("delete from movie where id=%s;", [id])
            cursor.close()
            cnx.close()
            return movies_site()

@app.route("/tickets", methods=['GET', 'POST'])
def tickets():
    if request.method == 'GET':
        return ticket_site()
    else:
        if request.form['action'] == 'add':
            quantity = request.form['quantity']
            price = request.form['price']

            cnx = connect_cinemas_db()
            cursor = cnx.cursor()
            sql = """
            insert into ticket(quantity, price) values(%s, %s);
            """
            if price == "adults":
                cursor.execute(sql, (quantity, (int(quantity)*18.5)))
            elif price == "children":
                cursor.execute(sql, (quantity, (int(quantity) * 12)))
            cursor.close()
            cnx.close()
            return ticket_site()

        if request.form['action'] == 'del':
            id = request.form['id_delete']
            cnx = connect_cinemas_db()
            cursor = cnx.cursor()
            cursor.execute("delete from ticket where id=%s;", [id])
            cursor.close()
            cnx.close()
            return ticket_site()

@app.route("/payments", methods=['GET', 'POST'])
def payment():
    if request.method == 'GET':
        return payments_site()
    else:
        if request.form['action'] == 'add':
            pay_date = request.form['pay_date']
            pay_type = request.form['pay_type']
            cnx = connect_cinemas_db()
            cursor = cnx.cursor()
            sql = """
            insert into payment(type, date) values(%s, %s);
            """
            cursor.execute(sql, (pay_type, pay_date))
            cursor.close()
            cnx.close()
            return payments_site()
        if request.form['action'] == 'search_1':
            older = request.form['older']
            html_parts = []
            html_parts.append(html_payments)
            html_parts.append('<a href="http://localhost:5000/payments">Usuń wyniki wyszukiwania</a>')
            cnx = connect_cinemas_db()
            cursor = cnx.cursor()
            sql = "select type, date from payment where date < %s;"
            cursor.execute(sql, [older])
            html_parts.append('<p>Lista płatności starszych niż: {}</p>'.format(older))
            html_parts.append('<ul>')

            for cin in cursor:
                l = '<li>Rodzaj płatności: {}. Data płatności: {}</li>'.format(cin[0], cin[1])
                html_parts.append(l)
            html_parts.append('</ul>')
            cursor.close()
            cnx.close()
            html = '\n'.join(html_parts)
            return html
        if request.form['action'] == 'search_2':
            newest = request.form['newest']
            html_parts = []
            html_parts.append(html_payments)
            html_parts.append('<a href="http://localhost:5000/payments">Usuń wyniki wyszukiwania</a>')
            cnx = connect_cinemas_db()
            cursor = cnx.cursor()
            sql = "select type, date from payment where date > %s;"
            cursor.execute(sql, [newest])
            html_parts.append('<p>Lista płatności nowszych niż: {}</p>'.format(newest))
            html_parts.append('<ul>')

            for cin in cursor:
                l = '<li>Rodzaj płatności: {}. Data płatności: {}</li>'.format(cin[0], cin[1])
                html_parts.append(l)
            html_parts.append('</ul>')
            cursor.close()
            cnx.close()
            html = '\n'.join(html_parts)
            return html
        if request.form['action'] == 'search_3':
            search_from = request.form['search_from']
            search_to = request.form['search_to']
            html_parts = []
            html_parts.append(html_payments)
            html_parts.append('<a href="http://localhost:5000/payments">Usuń wyniki wyszukiwania</a>')
            cnx = connect_cinemas_db()
            cursor = cnx.cursor()
            sql = "select type, date from payment where date > %s and date < %s;"
            cursor.execute(sql, (search_from, search_to))
            html_parts.append('<p>Lista płatności w przedziale od {} do {}:</p>'.format(search_from, search_to))
            html_parts.append('<ul>')

            for cin in cursor:
                l = '<li>Rodzaj płatności: {}. Data płatności: {}</li>'.format(cin[0], cin[1])
                html_parts.append(l)
            html_parts.append('</ul>')
            cursor.close()
            cnx.close()
            html = '\n'.join(html_parts)
            return html
        if request.form['action'] == 'search_4':
            search = request.form['search']
            html_parts = []
            html_parts.append(html_payments)
            html_parts.append('<a href="http://localhost:5000/payments">Usuń wyniki wyszukiwania</a>')
            cnx = connect_cinemas_db()
            cursor = cnx.cursor()
            sql = "select type, date from payment where date = %s;"
            cursor.execute(sql, [search])
            html_parts.append('<p>Lista płatności z dnia: {}</p>'.format(search))
            html_parts.append('<ul>')

            for cin in cursor:
                l = '<li>Rodzaj płatności: {}. Data płatności: {}</li>'.format(cin[0], cin[1])
                html_parts.append(l)
            html_parts.append('</ul>')
            cursor.close()
            cnx.close()
            html = '\n'.join(html_parts)
            return html
        if request.form['action'] == 'del':
            id = request.form['id_delete']
            cnx = connect_cinemas_db()
            cursor = cnx.cursor()
            cursor.execute("delete from payment where id=%s;", [id])
            cursor.close()
            cnx.close()
            return payments_site()





app.run(debug=True)