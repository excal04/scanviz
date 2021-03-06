"""
views.py: views module for scanviz web app
author: Jeff
date: 10/2016
"""

import json
from datetime import datetime, date
from flask import render_template, redirect, url_for, session, flash, request, g
from config import ELASTIC_SCAN_INDEX, ELASTIC_SCAN_DOC_TYPE, UPLOAD_LOC
from app import app, es
from forms import ScanForm
from werkzeug.utils import secure_filename
import elasticsearch

@app.route('/')
def index():
    return render_template('index.html', title="Home")

# todo: check if correct format
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = ScanForm()
    if form.validate_on_submit():
        # we want either text upload of file upload
        contents = []
        if form.fileup.data:
            for f in request.files.getlist('fileup'):   # handle multiple files
                contents.append(f.stream.read())
        elif form.textup.data:
            contents.append(form.textup.data)

        if contents:
            for scan in contents:
                res = es.index(index=ELASTIC_SCAN_INDEX,
                    doc_type=ELASTIC_SCAN_DOC_TYPE,
                    body=json.loads(scan))
                if res:
                    flash('scan uploaded!')
                else:
                    flash('error indexing data')
            return redirect(url_for('index'))
    return render_template('upload_scan.html', form=form)


@app.route('/getsummary', methods=['POST'])
def scan_summary():
    # get date range
    from_t = datetime.min
    to_t = datetime.max
    if request.form['from'] and request.form['to']:
        from_t = datetime.strptime(request.form['from'], "%Y-%m-%dT%H:%M")
        to_t = datetime.strptime(request.form['to'], "%Y-%m-%dT%H:%M")

    ret = {"ports" : {}}

    # i'm sure there's a better way to do this... ugh.
    try:
        res = es.search(index=ELASTIC_SCAN_INDEX, q="tcp.\*.state:open")
    except elasticsearch.ElasticsearchException:    # NotFoundError
        flash("no records yet")
        return json.dumps(ret)
    for hit in res['hits']['hits']:
        scan_t = datetime.strptime(hit["_source"]["datetime"][:-7], "%Y-%m-%d %H:%M:%S")    # drops ms

        # only summarize data with scan time in range specified
        if from_t <= scan_t <= to_t:
            ports = hit["_source"]["tcp"].keys()
            for port in ports:
                if hit["_source"]["tcp"][port]["state"] == "open":
                    if ret["ports"].get(port):
                        ret["ports"][port]["count"] += 1
                    else:
                        ret["ports"][port] = {"count" : 1, "name" : hit["_source"]["tcp"][port]["name"]}

    return json.dumps(ret)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')
    else:   # POST
        res = es.search(index=ELASTIC_SCAN_INDEX, body={"query":{"match":{"hostnames.name":request.form['keyword']}}})
        return json.dumps(res['hits']['hits'][0]) if res['hits']['hits'] else "null"
