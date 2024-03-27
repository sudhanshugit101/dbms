from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///construction.db'
db = SQLAlchemy(app)

# Patents Table
class Patent(db.Model):
    PatentID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(100), nullable=False)
    InventorID = db.Column(db.Integer, db.ForeignKey('inventor.InventorID'), nullable=False)
    FilingDate = db.Column(db.String(20), nullable=False)
    Abstract = db.Column(db.Text, nullable=False)

# Inventors Table
class Inventor(db.Model):
    InventorID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    Organization = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), nullable=False)

# Assignees Table
class Assignee(db.Model):
    AssigneeID = db.Column(db.Integer, primary_key=True)
    AssigneeName = db.Column(db.String(100), nullable=False)
    Country = db.Column(db.String(50), nullable=False)
    ContactPerson = db.Column(db.String(100), nullable=False)
    ContactEmail = db.Column(db.String(100), nullable=False)

# Categories Table
class Category(db.Model):
    CategoryID = db.Column(db.Integer, primary_key=True)
    CategoryName = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.Text, nullable=True)
    ParentCategoryID = db.Column(db.Integer, db.ForeignKey('category.CategoryID'))
    CreatedAt = db.Column(db.String(20), nullable=False)

# References Table
class Reference(db.Model):
    ReferenceID = db.Column(db.Integer, primary_key=True)
    PatentID = db.Column(db.Integer, db.ForeignKey('patent.PatentID'), nullable=False)
    CitationType = db.Column(db.String(50), nullable=False)
    ReferencePatentID = db.Column(db.Integer, db.ForeignKey('patent.PatentID'), nullable=False)
    PublicationDate = db.Column(db.String(20), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Sample data
sample_data = {
    'patents': [
        {'Title': 'Patent A', 'InventorID': 1, 'FilingDate': '2024-03-01', 'Abstract': 'Abstract for Patent A'},
        {'Title': 'Patent B', 'InventorID': 2, 'FilingDate': '2024-04-01', 'Abstract': 'Abstract for Patent B'},
        # Add more patent data as needed
    ],
    'inventors': [
        {'FirstName': 'John', 'LastName': 'Doe', 'Organization': 'XYZ Inc', 'Email': 'john@example.com'},
        {'FirstName': 'Jane', 'LastName': 'Smith', 'Organization': 'ABC Corp', 'Email': 'jane@example.com'},
        # Add more inventor data as needed
    ],
    'assignees': [
        {'AssigneeName': 'Company X', 'Country': 'USA', 'ContactPerson': 'Mr. X', 'ContactEmail': 'x@example.com'},
        {'AssigneeName': 'Company Y', 'Country': 'UK', 'ContactPerson': 'Ms. Y', 'ContactEmail': 'y@example.com'},
        # Add more assignee data as needed
    ],
    'categories': [
        {'CategoryName': 'Category A', 'Description': 'Description for Category A', 'ParentCategoryID': None, 'CreatedAt': '2024-01-01'},
        {'CategoryName': 'Category B', 'Description': 'Description for Category B', 'ParentCategoryID': None, 'CreatedAt': '2024-01-01'},
        # Add more category data as needed
    ],
    'references': [
        {'PatentID': 1, 'CitationType': 'Type A', 'ReferencePatentID': 2, 'PublicationDate': '2024-02-01'},
        {'PatentID': 2, 'CitationType': 'Type B', 'ReferencePatentID': 1, 'PublicationDate': '2024-03-01'},
        # Add more reference data as needed
    ]
}

# Insert sample data into tables
with app.app_context():
    for table_name, data in sample_data.items():
        class_name = table_name[:-1].capitalize()  # Remove the last character and capitalize
        if class_name == "Categorie":
            class_name = "Category"  # Correct the class name
        model_class = globals()[class_name]
        
        for entry in data:
            # Check if an entry with the same data exists
            existing_entry = model_class.query.filter_by(**entry).first()
            
            if existing_entry is None:
                new_entry = model_class(**entry)
                db.session.add(new_entry)
                db.session.commit()  
# Routes
@app.route('/')
def index():
    return render_template('index.html', patents=Patent.query.all(),
                           inventors=Inventor.query.all(),
                           assignees=Assignee.query.all(),
                           categories=Category.query.all(),
                           references=Reference.query.all())

# Routes for displaying individual HTML pages
@app.route('/patents')
def patents():
    return render_template('patents.html', patents=Patent.query.all())

@app.route('/inventors')
def inventors():
    return render_template('inventors.html', inventors=Inventor.query.all())

@app.route('/assignees')
def assignees():
    return render_template('assignees.html', assignees=Assignee.query.all())

@app.route('/categories')
def categories():
    return render_template('category.html', categories=Category.query.all())

@app.route('/references')
def references():
    return render_template('references.html', references=Reference.query.all())

@app.route('/patents')
def show_patents():
    patents = Patent.query.all()  # Assuming you have a method to query all patents
    return render_template('patents.html', patents=patents)

@app.route('/add_patent', methods=['POST'])
def add_patent():
    if request.method == 'POST':
        title = request.form['title']
        inventor_id = request.form['inventor_id']
        filing_date = request.form['filing_date']
        abstract = request.form['abstract']

        new_patent = Patent(Title=title, InventorID=inventor_id, FilingDate=filing_date, Abstract=abstract)

        db.session.add(new_patent)
        db.session.commit()

    return redirect(url_for('patents'))

@app.route('/add_inventor', methods=['POST'])
def add_inventor():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        organization = request.form['organization']
        email = request.form['email']

        new_inventor = Inventor(FirstName=first_name, LastName=last_name, Organization=organization, Email=email)

        db.session.add(new_inventor)
        db.session.commit()

    return redirect(url_for('inventors'))

@app.route('/add_assignee', methods=['POST'])
def add_assignee():
    if request.method == 'POST':
        assignee_name = request.form['assignee_name']
        country = request.form['country']
        contact_person = request.form['contact_person']
        contact_email = request.form['contact_email']

        new_assignee = Assignee(AssigneeName=assignee_name, Country=country, ContactPerson=contact_person, ContactEmail=contact_email)

        db.session.add(new_assignee)
        db.session.commit()

    return redirect(url_for('asignees'))

@app.route('/add_category', methods=['POST'])
def add_category():
    if request.method == 'POST':
        category_name = request.form['category_name']
        description = request.form['description']
        parent_category_id = request.form['parent_category_id']
        created_at = request.form['created_at']

        new_category = Category(CategoryName=category_name, Description=description, ParentCategoryID=parent_category_id, CreatedAt=created_at)

        db.session.add(new_category)
        db.session.commit()

    return redirect(url_for('categories'))

@app.route('/add_reference', methods=['POST'])
def add_reference():
    if request.method == 'POST':
        patent_id = request.form['patent_id']
        citation_type = request.form['citation_type']
        reference_patent_id = request.form['reference_patent_id']
        publication_date = request.form['publication_date']

        new_reference = Reference(PatentID=patent_id, CitationType=citation_type, ReferencePatentID=reference_patent_id, PublicationDate=publication_date)

        db.session.add(new_reference)
        db.session.commit()

    return redirect(url_for('references'))



@app.route('/modify_patent/<int:id>', methods=['POST'])
def modify_patent(id):
    patent = Patent.query.get_or_404(id)
    if request.method == 'POST':
        patent.Title = request.form['title']
        patent.InventorID = request.form['inventor_id']
        patent.FilingDate = request.form['filing_date']
        patent.Abstract = request.form['abstract']

        db.session.commit()

    return redirect(url_for('patents'))

@app.route('/modify_inventor/<int:id>', methods=['POST'])
def modify_inventor(id):
    inventor = Inventor.query.get_or_404(id)
    if request.method == 'POST':
        inventor.FirstName = request.form['first_name']
        inventor.LastName = request.form['last_name']
        inventor.Organization = request.form['organization']
        inventor.Email = request.form['email']

        db.session.commit()

    return redirect(url_for('inventors'))

@app.route('/modify_assignee/<int:id>', methods=['POST'])
def modify_assignee(id):
    assignee = Assignee.query.get_or_404(id)
    if request.method == 'POST':
        assignee.AssigneeName = request.form['assignee_name']
        assignee.Country = request.form['country']
        assignee.ContactPerson = request.form['contact_person']
        assignee.ContactEmail = request.form['contact_email']

        db.session.commit()

    return redirect(url_for('assignees'))

@app.route('/modify_category/<int:id>', methods=['POST'])
def modify_category(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        category.CategoryName = request.form['category_name']
        category.Description = request.form['description']
        category.ParentCategoryID = request.form['parent_category_id']
        category.CreatedAt = request.form['created_at']

        db.session.commit()

    return redirect(url_for('categories'))

@app.route('/modify_reference/<int:id>', methods=['POST'])
def modify_reference(id):
    reference = Reference.query.get_or_404(id)
    if request.method == 'POST':
        reference.PatentID = request.form['patent_id']
        reference.CitationType = request.form['citation_type']
        reference.ReferencePatentID = request.form['reference_patent_id']
        reference.PublicationDate = request.form['publication_date']

        db.session.commit()

    return redirect(url_for('references'))




# Routes for deleting data
@app.route('/delete_patent/<int:id>', methods=['POST'])
def delete_patent(id):
    patent = Patent.query.get_or_404(id)
    db.session.delete(patent)
    db.session.commit()
    return redirect(url_for('patents'))

@app.route('/delete_inventor/<int:id>', methods=['POST'])
def delete_inventor(id):
    inventor = Inventor.query.get_or_404(id)
    db.session.delete(inventor)
    db.session.commit()
    return redirect(url_for('inventors'))

@app.route('/delete_assignee/<int:id>', methods=['POST'])
def delete_assignee(id):
    assignee = Assignee.query.get_or_404(id)
    db.session.delete(assignee)
    db.session.commit()
    return redirect(url_for('assignees'))

@app.route('/delete_category/<int:id>', methods=['POST'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('categories'))

@app.route('/delete_reference/<int:id>', methods=['POST'])
def delete_reference(id):
    reference = Reference.query.get_or_404(id)
    db.session.delete(reference)
    db.session.commit()
    return redirect(url_for('references'))


if __name__ == '__main__':
    app.run(debug=True)