import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Blueprint, render_template, redirect, url_for
from app.forms import AppointmentForm
from datetime import datetime, timedelta


bp = Blueprint('main', __name__, url_prefix='/')

CONNECTION_PARAMETERS = {
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASS"),
    "dbname": os.environ.get("DB_NAME"),
    "host": os.environ.get("DB_HOST"),
}

def add_appointment(form):
    with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            params = {
                'name': form.name.data,
                'start_datetime': datetime.combine(form.start_date.data, form.start_time.data),
                'end_datetime': datetime.combine(form.end_date.data, form.end_time.data),
                'description': form.description.data,
                'private': form.private.data
            }

            insert_query = """
            INSERT INTO appointments (
                name, start_datetime, end_datetime,
                description, private
                )
            VALUES (
                %(name)s, %(start_datetime)s, %(end_datetime)s,
                %(description)s, %(private)s
                )
            ;"""

            curs.execute(insert_query, params)
    return redirect('/')

def fetch_all_appointments():
    with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            select_query = """SELECT id, name, start_datetime, end_datetime
                         FROM appointments
                         ORDER BY start_datetime;"""
            curs.execute(select_query)
            results = curs.fetchall()
        return results

def fetch_todays_appointments(year, month, day):
    today = datetime(year, month, day)  #time portion is optional in datetime, defaults to 00:00:00 (midnight)
    next_day = today + timedelta(days = 1)
    with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            params = {
                'today': today,
                'next_day': next_day
            }
            select_query = """SELECT id, name, start_datetime, end_datetime
                         FROM appointments
                         WHERE start_datetime BETWEEN %(today)s AND %(next_day)s
                         ORDER BY start_datetime;"""

            curs.execute(select_query, params)
            results = curs.fetchall()
        return results




@bp.route('/', methods=['GET'])
def main():
    today = datetime.now() #gives year, month, and day
    y = today.year
    m = today.month
    d = today.day
    return redirect(url_for('.daily', year = y, month = m, day = d))
    #gives the same result as
    #return redirect(f'/{y}/{m}/{d})
    #but is better because it isn't hard coded

    # code for fetching all appointments
    # form1 = AppointmentForm()
    # if form1.validate_on_submit():
    #     add_appointment(form1)

    # results = fetch_all_appointments()
    # return render_template('main.html', rows=results, form=form1)

@bp.route("/<int:year>/<int:month>/<int:day>", methods = ['GET', 'POST'])
def daily(year, month, day):
    form1 = AppointmentForm()
    if form1.validate_on_submit():
        add_appointment(form1)

    results = fetch_todays_appointments(year, month, day)
    return render_template('main.html', rows=results, form=form1, year=year, month=month, day=day)
