from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config import Config
from models import db, User, Transaction, SavingsAccount
from forms import RegisterForm, LoginForm, TransferForm, SavingsForm, PaymentForm

@app.route('/savings', methods=['GET', 'POST'])
@login_required
def savings():
    form = SavingsForm()
    savings = SavingsAccount.query.filter_by(user_id=current_user.id).first()

    if form.validate_on_submit():
        amount = float(form.amount.data)

        if form.action.data == 'deposit':
            if current_user.balance >= amount:
                current_user.balance -= amount
                savings.balance += amount
                flash('Средства переведены в накопления')
            else:
                flash('Недостаточно средств')

        elif form.action.data == 'withdraw':
            if savings.balance >= amount:
                savings.balance -= amount
                current_user.balance += amount
                flash('Средства выведены с накоплений')
            else:
                flash('Недостаточно накоплений')

        db.session.commit()
        return redirect(url_for('savings'))

    return render_template('savings.html', form=form, savings=savings)


@app.route('/payments', methods=['GET', 'POST'])
@login_required
def payments():
    form = PaymentForm()

    if form.validate_on_submit():
        amount = float(form.amount.data)

        if current_user.balance < amount:
            flash('Недостаточно средств')
            return redirect(url_for('payments'))

        current_user.balance -= amount

        transaction = Transaction(
            sender_id=current_user.id,
            receiver_id=current_user.id,
            amount=amount,
            description=f'Оплата: {form.category.data}'
        )

        db.session.add(transaction)
        db.session.commit()

        flash('Платёж выполнен')
        return redirect(url_for('payments'))

    return render_template('payments.html', form=form)


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
