from flask import abort


def handle_validation_errors(errors):
    if len(errors):
        errorString = ''
        for k in errors:
            errorString += k + ' '
            for error in errors[k]:
                errorString += error + ', '
            errorString += '\n'
        abort(409, errorString)