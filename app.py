from flask import Flask, redirect, url_for, render_template, request, flash
from models import db, Person
from forms import PersonForm
import os
from werkzeug.utils import secure_filename

from helpers.helpers import upload_file, generate_unique_filename, allowed_file, create_presigned_url
from config.config import AZURE_STORAGE_CONTAINER_NAME, DB_CONNECT_STRING, DB_USER, DB_PASSWORD, LANGUAGE


# Flask configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['DEBUG'] = False


app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle+cx_oracle://{}:{}@{}'.format(DB_USER,DB_PASSWORD,DB_CONNECT_STRING)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route("/")
def index():
    '''
    [English] Home page
    [Portuguese] Página inicial
    '''
    if LANGUAGE == 'PT':
        return render_template('web/home_pt.html')
    else:
        return render_template('web/home_en.html')


@app.route("/new_person", methods=('GET', 'POST'))
def new_person():
    '''
    [English] Create new person
    [Portuguese] Adiciona nova pessoa
    '''
    form = PersonForm()
    if form.validate_on_submit():
        my_person = Person()
        form.populate_obj(my_person)

        file_to_upload = request.files['attachment']
        final_file_name = generate_unique_filename(my_person.name,my_person.surname)
        my_person.attachment = final_file_name

        db.session.add(my_person)

        if not file_to_upload:
            if LANGUAGE == 'PT':
                flash('Arquivo não selecionado.','danger')
                return render_template('web/new_person_pt.html', form=form)
            else:
                flash('File not selected.','danger')
                return render_template('web/new_person_en.html', form=form)
        
        if file_to_upload and not allowed_file(file_to_upload.filename):
            
            if LANGUAGE == 'PT':
                flash('Formato inválido. Apenas PDFs permitidos.','warning')
                return render_template('web/new_person_pt.html', form=form)
            else:
                flash('Invalid file format. Only PDFs allowed.','warning')
                return render_template('web/new_person_en.html', form=form)
        try:
            filename = secure_filename(file_to_upload.filename)
            file_to_upload.save(filename)
            upload_file(filename,AZURE_STORAGE_CONTAINER_NAME,final_file_name)
            os.remove(filename)
            db.session.commit()
            # User info
            if LANGUAGE == 'PT':
                flash('Pessoa adicionada com sucesso.', 'success')
                return redirect(url_for('persons'))
            else:
                flash('Person added successfully.', 'success')
                return redirect(url_for('persons'))
        except Exception as error:
            print(error)
            db.session.rollback()
            if LANGUAGE == 'PT':
                flash('Erro ao adicionar pessoa.', 'danger')
            else:
                flash('Error while trying to add person.', 'danger')
    
    if LANGUAGE == 'PT':    
        return render_template('web/new_person_pt.html', form=form)
    else:
        return render_template('web/new_person_en.html', form=form)


@app.route("/edit_person/<id>", methods=('GET', 'POST'))
def edit_person(id):
    '''
    [English] Edit person
    :param id: Id from person

    [Portuguese] Editar pessoa
    :param id: Id da pessoa
    '''
    my_person = Person.query.filter_by(id=id).first()
    form = PersonForm(obj=my_person)

    if form.validate_on_submit():
        try:
            if not form.attachment.data:
                form.attachment.data = my_person.attachment
                form.populate_obj(my_person)
            else:
                file_to_upload = request.files['attachment']

                if file_to_upload and not allowed_file(file_to_upload.filename):
                    if LANGUAGE == 'PT':
                        flash('Formato inválido. Apenas PDFs permitidos.','warning')
                        return render_template('web/new_person_pt.html', form=form)
                    else:
                        flash('Invalid file format. Only PDFs allowed.','warning')
                        return render_template('web/new_person_en.html', form=form)
                
                final_file_name = generate_unique_filename(my_person.name,my_person.surname)
                filename = secure_filename(file_to_upload.filename)
                file_to_upload.save(filename)
                upload_file(filename,AZURE_STORAGE_CONTAINER_NAME,final_file_name)
                os.remove(filename)

                form.populate_obj(my_person)
                my_person.attachment = final_file_name

            db.session.add(my_person)
            db.session.commit()

            if LANGUAGE == 'PT':
                flash('Atualizado com sucesso.', 'success')
            else:
                flash('Updated sucessfully.', 'success')
        except Exception as error:
            print(error)
            db.session.rollback()
            if LANGUAGE == 'PT':
                flash('Erro ao atualizar.', 'danger')
            else:
                flash('Error while updating.', 'danger')
    if LANGUAGE == 'PT':
        return render_template('web/edit_person_pt.html',form=form)
    else:
        return render_template('web/edit_person_en.html',form=form)


@app.route("/persons")
def persons():
    '''
    [English] Show alls persons
    [Portuguese] Mostra todas as pessoas
    '''
    persons = Person.query.order_by(Person.name).all()
    if LANGUAGE == 'PT':
        return render_template('web/persons_pt.html', persons=persons)
    else:
        return render_template('web/persons_en.html', persons=persons)


@app.route("/search")
def search():
    '''
    [English] Search
    [Portuguese] Pesquisar
    '''
    name_search = request.args.get('name')
    all_persons = Person.query.filter(
        Person.name.contains(name_search)
        ).order_by(Person.name).all()
    
    if LANGUAGE == 'PT':    
        return render_template('web/persons_pt.html', persons=all_persons)
    else:
        return render_template('web/persons_en.html', persons=all_persons)


@app.route("/persons/delete", methods=('POST',))
def persons_delete():
    '''
    [English] Delete person
    [Portuguese] Deletar pessoa
    '''
    try:
        person = Person.query.filter_by(id=request.form['id']).first()
        db.session.delete(person)
        db.session.commit()
        if LANGUAGE == 'PT': 
            flash('Deletado com sucesso.', 'danger')
        else:
            flash('Deleted successfully.', 'danger')
    except:
        db.session.rollback()
        
        if LANGUAGE == 'PT':
            flash('Erro ao deletar.', 'danger')
        else:
            flash('Error while deleting.', 'danger')

    return redirect(url_for('persons'))

@app.route("/persons/attachment/<id>", methods=('GET',))
def persons_attachment(id):
    '''
    [English] View attachment
    :param id: Id from attachment
    
    [Portuguese] Ver anexo
    :param id: Id do anexo

    '''
    my_person = Person.query.filter_by(id=id).first()
    attachment_pre_signed_url = create_presigned_url(AZURE_STORAGE_CONTAINER_NAME,my_person.attachment)

    return redirect(attachment_pre_signed_url)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
