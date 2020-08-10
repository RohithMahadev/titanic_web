from flask import *
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,RadioField,SelectField
from wtforms.validators import DataRequired
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
df = pd.read_csv('titanic_training_data.csv')
df.replace(to_replace=np.nan,value=30,inplace = True)
lb_make = LabelEncoder()
df["Sex_code"] = lb_make.fit_transform(df["Sex"])
x = df[[ 'Pclass', 'Sex_code', 'Age', 'SibSp','Parch']]
y= df['Survived']
knn= KNeighborsClassifier(n_neighbors = 7)
knn.fit(x,y)


csrf = CSRFProtect()
app = Flask(__name__)
app.secret_key = 'zr@i-*k6gq6n=6xktv56tcmfcbyf^ck1wh=fyf155p#1j(-&g0'
csrf.init_app(app)

class registerformman(FlaskForm):
   tclass = RadioField('Ticket Class', choices=[('1','1'),('2','2'),('3','3')])
   age = StringField('Age', validators=[DataRequired()])
   sibsb = StringField('No of Siblings', validators=[DataRequired()])
   parch = StringField('No. of accompanying persons [3 max]', validators=[DataRequired()])
   gender = RadioField('Gender', choices=[('0','Female'),('1','Male')])


@app.route('/',methods=['GET','POST'])
def index():
   form=registerformman(request.form)
   if request.method == 'POST' and form.validate_on_submit():
      tt_prd = knn.predict([[float(form.tclass.data),float(form.gender.data),float(form.age.data),float(form.sibsb.data),float(form.parch.data)]])
      if(tt_prd[0]==0):
         return render_template('drowned.html')
      else:
         return render_template('saved.html')
   else:
      return render_template('index.html',form=form)









# @app.route('/')
# def index():
#    return render_template('index.html')

if __name__ == '__main__':
   app.run()