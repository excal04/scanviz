
import json
from flask import render_template, redirect, url_for, session, flash, request, g
from config import ELASTIC_SCAN_INDEX, ELASTIC_SCAN_DOC_TYPE, UPLOAD_LOC
from app import app, es
from forms import ScanForm
from werkzeug.utils import secure_filename

@app.route('/')
def index():
    return render_template('index.html', title="Home")


@app.route('/upload', methods=('GET', 'POST'))
def upload():
    form = ScanForm()
    if form.validate_on_submit():
        # we want either text upload of file upload
        contents = None
        if form.fileup.data:
            contents = form.fileup.data.read()
        elif form.textup.data:
            contents = form.textup.data

        if contents:
            res = es.index(index=ELASTIC_SCAN_INDEX,
                doc_type=ELASTIC_SCAN_DOC_TYPE,
                body=json.loads(contents))
            if res:
                flash('scan uploaded!')
            else:
                flash('error indexing data')
            return redirect(url_for('index'))
    return render_template('upload_scan.html', form=form)
