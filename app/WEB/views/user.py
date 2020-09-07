from flask import Blueprint, render_template, url_for, request, redirect, flash


user_bp = Blueprint('user_bp', __name__, url_prefix='/user')
