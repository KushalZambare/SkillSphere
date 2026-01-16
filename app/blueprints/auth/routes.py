from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.blueprints.auth import bp
from app import db
from app.models import User


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registration route for new users.
    GET: Display registration form
    POST: Process registration and create new user
    """
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        # Validation
        errors = []
        
        if not name:
            errors.append('Name is required.')
        if not username:
            errors.append('Username is required.')
        if not password:
            errors.append('Password is required.')
        if password != confirm_password:
            errors.append('Passwords do not match.')
        if len(password) < 6:
            errors.append('Password must be at least 6 characters long.')
        
        # Check if username already exists
        if username and User.query.filter_by(username=username).first():
            errors.append('Username already exists. Please choose a different one.')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html')
        
        # Create new user
        try:
            user = User(
                name=name,
                username=username
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            # Log the user in
            login_user(user)
            flash(f'Welcome, {user.name}! Your account has been created successfully.', 'success')
            
            # Redirect to dashboard/setup page (for now, redirect to index)
            return redirect(url_for('main.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while creating your account: {str(e)}', 'error')
            return render_template('register.html')
    
    # GET request - show registration form
    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login route for existing users.
    GET: Display login form
    POST: Process login and authenticate user
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        # Validation
        if not username:
            flash('Username is required.', 'error')
            return render_template('login.html')
        
        if not password:
            flash('Password is required.', 'error')
            return render_template('login.html')
        
        # Find user by username
        user = User.query.filter_by(username=username).first()
        
        # Check if user exists and password is correct
        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.name}!', 'success')
            
            # Redirect to dashboard/profile page (for now, redirect to index)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
            return render_template('login.html')
    
    # GET request - show login form
    return render_template('login.html')


@bp.route('/logout')
@login_required
def logout():
    """
    Logout route - logs out the current user
    """
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))
