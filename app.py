from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config import Config
from models import db, User, Transaction
from forms import RegisterForm, LoginForm, TransferForm

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists')
            return redirect(url_for('register'))

        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists')
            return redirect(url_for('register'))

        user = User(
            username=form.username.data,
            email=form.email.data
        )

        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Registration successful')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))

        flash('Invalid email or password')

    return render_template('login.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    form = TransferForm()

    if form.validate_on_submit():
        recipient = User.query.filter_by(username=form.recipient.data).first()
        amount = form.amount.data

        if not recipient:
            flash('Recipient not found')
            return redirect(url_for('transfer'))

        if recipient.id == current_user.id:
            flash('You cannot transfer to yourself')
            return redirect(url_for('transfer'))

        if current_user.balance < amount:
            flash('Insufficient funds')
            return redirect(url_for('transfer'))

        current_user.balance -= amount
        recipient.balance += amount

        transaction = Transaction(
            sender_id=current_user.id,
            receiver_id=recipient.id,
            amount=amount,
            description=form.description.data or 'Transfer'
        )

        db.session.add(transaction)
        db.session.commit()

        flash('Transfer successful')
        return redirect(url_for('dashboard'))

    return render_template('transfer.html', form=form)


@app.route('/history')
@login_required
def history():
    transactions = Transaction.query.filter(
        (Transaction.sender_id == current_user.id) |
        (Transaction.receiver_id == current_user.id)
    ).order_by(Transaction.timestamp.desc()).all()

    return render_template('history.html', transactions=transactions)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
