

from flask import send_from_directory,request,url_for

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
