from flask import Flask, request, render_template, redirect, url_for, flash
from database import db_session
from models import Member, Inventory, BookingTrip
from database import init_db
import csv
import io
import configparser


config = configparser.ConfigParser()

# Read the config file
config.read('config.ini')

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = config['flask']['secret_key']


@app.route('/populate_data', methods=['GET', 'POST'])   
def insert_records_into_table():

    """
        Take csv file as input and insert csv file data into Model:
        Member:-  First_name, Last_name, booking_count, date_joined
        Inventory:-  title, description, remaining_count, expiration_date
    """

    if request.method == 'POST':
        file_name = request.files['filename']
        table_name = request.form.get('model_name')

        with io.TextIOWrapper(file_name, encoding="utf-8") as file:
            contents = csv.DictReader(file)
            if table_name == 'member':
                db_session.bulk_insert_mappings( Member, contents )
            elif table_name == 'inventory':
                db_session.bulk_insert_mappings( Inventory, contents)
            else:
                return "Model not match in DB"  

            db_session.commit()
        flash( f"Table {table_name} records inserted successfully", 'success')

        return render_template('file_upload.html')
    else:
        return render_template('file_upload.html')



# Define a route
@app.route('/book',  methods=['GET', 'POST']    )
def book_booking():


    """
        Book a booking of member 

        We can use this as API   
        endpoint :- /book
        form_data = member_id:1
                    inventory_id:3

    """

    if request.method == 'POST':
        
        member_id = int(request.form.get('member_id'))
        inventory_id = int(request.form.get('inventory_id'))
        
        book_obj = BookingTrip.query.filter(BookingTrip.member_id==member_id).all()
        inv_book_obj = BookingTrip.query.filter(BookingTrip.inventory_id==inventory_id).all()

        if len(book_obj) >= 2:
            flash('Member reached max_booking count booking not completed', 'danger')
            return redirect(url_for('book_booking')) 
        
        inv_obj = Inventory.query.get(inventory_id)

        if len(inv_book_obj) < inv_obj.remaining_count:
            booking_obj = BookingTrip(member_id=member_id, inventory_id=inventory_id)
            db_session.add(booking_obj)
            db_session.commit()
            db_session.refresh(booking_obj)
            flash('Booking Done successfully', 'success')
            return redirect(url_for('book_booking')) 

        else:
            flash('Inventory is full booking not completed', 'danger')
            return redirect(url_for('book_booking')) 

    else:
        return render_template('book.html', member_list = Member.query.all(), inventory_list=Inventory.query.all())


@app.route('/', methods=['GET'])
def list_booking_obj():
    """Display the list of Booking """
    return render_template('booking_list.html',booking_obj = BookingTrip.query.all())


@app.route('/cancel/<int:booking_id>', methods=['GET'])
def cancel_booking(booking_id):

    """
        Cancel the booking 
        Use this END point for cancel booking 

        :-  /cancel/5


    """

    booking_obj = BookingTrip.query.get(booking_id)
    
    if booking_obj:
        # Delete the booking
        db_session.delete(booking_obj)
        db_session.commit()
        flash('Booking cancel successfully', 'success')
        return redirect(url_for('list_booking_obj')) 
    else:
        return "Booking not found"



@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    init_db()
    app.run(debug=True)