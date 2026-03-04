from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import streamlit as st

# Initialize the Flask application
app = Flask(__name__)

# Configure the database
# Using os.path.abspath to ensure the path is correct
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'family.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the database model for a Family Member
class FamilyMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<FamilyMember {self.name}>'

# Create the database tables
#@app.before_first_request
def create_tables():
    db.create_all()

# Route to serve the front-end
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to add a new family member
@app.route('/api/add_member', methods=['POST'])
def add_member():
    data = request.get_json()
    new_member_name = data.get('name')
    if not new_member_name:
        return jsonify({'error': 'Name is required'}), 400
    
    new_member = FamilyMember(name=new_member_name)
    db.session.add(new_member)
    db.session.commit()
    
    return jsonify({'message': 'Family member added successfully'}), 201

# API endpoint to get all family members
@app.route('/api/get_members', methods=['GET'])
def get_members():
    members = FamilyMember.query.all()
    # Convert list of objects to list of dictionaries
    members_list = [{'name': member.name} for member in members]
    return jsonify(members_list)

if __name__ == '__main__':
    app.run(debug=True)

