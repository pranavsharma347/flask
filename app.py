from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

#render_template for render a template in flask
# Flask constructor takes the name of
# current module (__name__) as argument.
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///student.db'  # for make database in sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    first_name=db.Column(db.String(50),nullable=False)
    last_name=db.Column(db.String(50),nullable=False)
    address=db.Column(db.String(50),nullable=False)
    

    def __repr__(self) -> str:
        return f"{self.id}-{self.first_name}"
    
db.create_all()
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        address=request.form['address']
        student=Student(first_name=first_name,last_name=last_name,address=address)
        db.session.add(student)
        db.session.commit()
    allstudent=Student.query.all()
    return render_template('index.html',allstudent=allstudent)


@app.route('/update/<int:id>',methods=['GET','POST'])  # now when you open http://127.0.0.1:8000/products
def update(id):
    if request.method=='POST':
        first_name=request.form['firstname']
        last_name=request.form['lastname']
        address=request.form['address']
        student=Student.query.filter_by(id=id).first()
        student.first_name=first_name
        student.last_name=last_name
        student.address=address
        db.session.add(student)
        db.session.commit()
        return redirect('/')
    student=Student.query.filter_by(id=id).first()
    return render_template('update.html',student=student)

@app.route('/delete/<int:id>')  # now when you open http://127.0.0.1:8000/products
def delete(id):
    student=Student.query.filter_by(id=id).first()
    db.session.delete(student)
    db.session.commit()
    return redirect("/")




if __name__=='__main__':
    app.run(debug=True,port=8000)  # run in debug mode means if error is come we see in browser