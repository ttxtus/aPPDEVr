from flask import Flask, render_template, request, redirect, url_for
from Forms import  CreateSignUpForm
import shelve, SignUp


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')

@app.route('/createSignUp', methods=['GET', 'POST'])
def create_signup():
    create_signup_form = CreateSignUpForm(request.form)
    if request.method == 'POST' and create_signup_form.validate():
        signups_dict = {}
        db = shelve.open('signup.db', 'c')

        try:
            signups_dict = db['SignUp']
        except:
            print("Error in retrieving Accounts from signup.db.")

        signup = SignUp.SignUp(create_signup_form.first_name.data, create_signup_form.last_name.data, create_signup_form.mobile_no.data, create_signup_form.password.data, create_signup_form.email.data)
        signups_dict[signup.get_account_id()] = signup
        db['SignUp'] = signups_dict

        db.close()

        return redirect(url_for('retrieve_signup'))
    return render_template('createSignUp.html', form=create_signup_form)



@app.route('/retrieveSignUp')
def retrieve_signup():
    signups_dict = {}
    db = shelve.open('signup.db', 'r')
    signups_dict = db['SignUp']
    db.close()

    signups_list = []
    for key in signups_dict:
        signup = signups_dict.get(key)
        signups_list.append(signup)

    return render_template('retrieveSignUp.html', count=len(signups_list), signups_list=signups_list)


@app.route('/updateSignUp/<int:id>/', methods=['GET', 'POST'])
def update_signup(id):
    update_signup_form = CreateSignUpForm(request.form)
    if request.method == 'POST' and update_signup_form.validate():
        signups_dict = {}
        db = shelve.open('signup.db', 'w')
        signups_dict = db['SignUp']

        signup = signups_dict.get(id)
        signup.set_first_name(update_signup_form.first_name.data)
        signup.set_last_name(update_signup_form.last_name.data)
        signup.set_mobile_no(update_signup_form.mobile_no.data)
        signup.set_password(update_signup_form.password.data)
        signup.set_email(update_signup_form.email.data)


        db['SignUp'] = signups_dict
        db.close()

        return redirect(url_for('retrieve_signup'))
    else:
        signups_dict = {}
        db = shelve.open('signup.db', 'r')
        signups_dict = db['SignUp']
        db.close()

        signup = signups_dict.get(id)

        update_signup_form.first_name.data = signup.get_first_name()
        update_signup_form.last_name.data = signup.get_last_name()
        update_signup_form.mobile_no.data = signup.get_mobile_no()
        update_signup_form.password.data = signup.get_password()
        update_signup_form.email.data = signup.get_email()


        return render_template('updateSignUp.html', form=update_signup_form)




@app.route('/deleteSignUp/<int:id>', methods=['POST'])
def delete_signup(id):
    signups_dict = {}
    db = shelve.open('signup.db', 'w')
    signups_dict = db['SignUp']

    signups_dict.pop(id)

    db['SignUp'] = signups_dict
    db.close()

    return redirect(url_for('retrieve_signup'))


if __name__ == '__main__':
    app.run()

