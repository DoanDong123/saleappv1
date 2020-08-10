from functools import wraps
from flask import render_template, session, request, redirect, url_for, jsonify


def login_required(f):
    @wraps(f)
    def check(*arg, **kwargs):
        if not session.get("user"): # Chua login
            return redirect(url_for("login", next=request.url))

        return f(*arg, **kwargs)

    return check