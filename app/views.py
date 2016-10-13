
import json
from flask import render_template, redirect, url_for, session, flash, request, g
from config import ELASTIC_SCAN_INDEX, ELASTIC_SCAN_DOC_TYPE, UPLOAD_LOC
from app import app, es
from forms import ScanForm
from werkzeug.utils import secure_filename

@app.route('/')
def index():
    res = es.get(index="dfir", doc_type="scan", id=2)['_source']
    return render_template('index.html', title="Home", res=res)


@app.route('/upload', methods=('GET', 'POST'))
def upload():
    form = ScanForm()
    if form.validate_on_submit():
        if form.fileup.data:
            print form.fileup.data.read()
            flash('scan file uploaded!')
            return redirect(url_for('index'))
        elif form.textup.data:
            print form.textup.data
            flash('scan text uploaded!')
            return redirect(url_for('index'))
    return render_template('upload_scan.html', form=form)
