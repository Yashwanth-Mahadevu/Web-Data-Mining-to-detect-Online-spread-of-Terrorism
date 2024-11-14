#importing required libraries

from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask import flash
from flask_material import Material
import numpy as np
import joblib
from keras.models import load_model
from keras_preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import pandas as pd
import random
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re


app = Flask(__name__)
Material(app)
app.secret_key="dont tell any one"

keywords = ['terrorism', 'bomb', 'attack', 'militant', 'extremist', 'radicalization', 'jihad', 'ISIS', 'Al-Qaeda',
 'Taliban', 'explosive', 'suicide bombing', 'hostage', 'violence', 'terrorist', 'insurgent', 'martyr', 'sleeper cell', 
 'fundamentalism', 'caliphate', 'beheading', 'massacre', 'radical', 'jihadi', 'sabotage', 'guerrilla', 
 'terrorist training', 'hijack', 'martyrdom', 'incendiary', 'propaganda', 'paramilitary', 'uprising', 'coup', 'insurgency',
  'civil unrest', 'radical group', 'sharia', 'fatwa', 'sectarian', 'hate speech', 'lone wolf', 'extremism', 'martial law', 
  'mass destruction', 'ideology', 'extremist violence', 'jihadist', 'radical Islamist', 'holy war', 'sleeper agent', 
  'bio-terrorism', 'chemical attack', 'nuclear threat', 'counter-terrorism', 'terror plot', 'religious extremism',
   'violent extremism', 'terror financing', 'suicide mission', 'car bombing', 'terrorist cell', 'war on terror', 
   'militant network', 'radical leader', 'holy jihad', 'global jihad', 'radical movement', 'terrorist ideology',
    'homegrown terrorism', 'sleeper network', 'terrorist network', 'holy martyrs', 'insurgent group', 'holy fighters', 
    'terrorist act', 'war on terror', 'militant group', 'jihadist group', 'terrorist threat', 'extremist group', 
    'terrorist campaign', 'terrorist operations', 'terrorist attack', 'terrorist propaganda', 'terrorist organization', 
    'radicalization process', 'extremist ideology', 'violent radicalization', 'religious fanaticism', 'jihadist violence', 
    'militant faction', 'violent jihad', 'fundamentalist movement','Naxalism', 'Maoism', 'ULFA', 'NSCN', 'Khalistan', 'Jihad', 'Lashkar-e-Taiba', 
    'Jaish-e-Mohammed', 'Hizbul Mujahideen', 'Al-Qaeda', 'ISIS', 'Indian Mujahideen', 
    'SIMI', 'RDX', 'Bomb blast', 'Terror plot', 'Extremism', 'Militancy', 
    'Separatist', 'Insurgency', 'Terrorist cell', 'Sleeper cell', 'Radicalization', 
    'Violence', 'Propaganda', 'Fundamentalism', 'Extremist', 'Radical Islamist', 
    'Religious extremism', 'Jihadi', 'Sharia', 'Fatwa', 'Hate speech', 'Sectarian', 
    'Martyrdom', 'Suicide bombing', 'Hostage', 'Kidnapping', 'Guerrilla', 'IED attack', 
    'Assassination', 'Beheading', 'Hijacking', 'Extortion', 'Narco-terrorism', 
    'Weapon smuggling', 'Human trafficking', 'Terror financing', 
    'Arms trafficking', 'Drug trafficking', 'Piracy', 'Cross-border terrorism', 
    'Intelligence gathering', 'Infiltration', 'Cyber terrorism', 'Bioterrorism', 
    'Nuclear threat', 'Chemical attack', 'Dirty bomb', 'IED explosion', 'Suicide attack', 
    'Urban Naxal', 'Maoist insurgent', 'Red corridor', 'Armed struggle', 'Proxy war', 
    'Terrorist network', 'Terrorist organization', 'Anti-national', 'Civil unrest', 
    'Martial law', 'Coup', 'Rebel', 'Extremist group', 'Violent extremism', 
    'Homegrown terrorism', 'Sleeper agent', 'Radical preacher', 'Holy war', 'Global jihad', 
    'Radical movement', 'Radical leader', 'Militant network', 'Holy jihad', 'Militant faction', 
    'Violent jihad', 'Fundamentalist movement', 'Terrorist act', 'Terrorist threat', 
    'Terrorist campaign', 'Terrorist operations', 'Terrorist attack', 'Terrorist propaganda', 
    'Radicalization process', 'Extremist ideology', 'Violent radicalization', 
    'Religious fanaticism', 'Jihadist violence', 'Revolutionary violence', 'Anti-state', 
    'Separatist movement', 'Self-determination', 'Insurgent group', 'Militant group', 
    'Subversive', 'Anarchist', 'Sedition', 'War on terror', 'Paramilitary', 'Martyr', 
    'Rebellion', 'Sabotage', 'Anti-terrorism', 'Counter-terrorism', 'Extremist violence', 
    'Holy martyrs', 'Radical Islamist group', 'Radical cleric', 'Islamic State', 
    'Militant Islam', 'Islamic extremism', 'Islamic fundamentalism', 'Mujahideen', 'Mujahid', 
    'Islamic insurgency', 'Islamic radicalism', 'Islamic militancy', 'Islamic terrorist', 
    'Islamic jihad', 'Islamic law', 'Sharia law', 'Islamic rebellion', 'Islamic State supporter', 
    'Islamic caliphate', 'Islamic emirate', 'Islamic governance', 'Islamic extremist group', 
    'Islamic militant group', 'Islamic terrorist group', 'Islamic radical', 'Islamic extremist', 
    'Islamic militant', 'Islamic terrorist', 'Jihadi ideology', 'Radical ideology', 
    'Extremist ideology', 'Islamic radicalization', 'Islamic radicalism', 'Islamic terrorism', 
    'Islamic extremism', 'Islamic militancy', 'Islamic violence', 'Islamic insurgency', 
    'Islamic uprising', 'Islamic protest', 'Islamic demonstration', 'Islamic unrest', 
    'Islamic disturbance', 'Islamic upheaval', 'Islamic revolt', 'Islamic insurrection', 
    'Islamic mutiny', 'Islamic rebellion', 'Islamic revolution', 'Islamic movement', 
    'Islamic struggle', 'Islamic resistance', 'Islamic fight', 'Islamic warfare', 
    'Islamic battle', 'Islamic conflict', 'Islamic crusade', 'Islamic holy war', 
    'Islamic sacred war', 'Islamic religious war', 'Islamic holy fight', 'Islamic sacred fight', 
    'Islamic religious fight', 'Islamic jihad', 'Islamic jihadi', 'Islamic holy warrior', 
    'Islamic mujahid', 'Islamic mujahideen', 'Islamic warrior', 'Islamic fighter', 
    'Islamic soldier', 'Islamic militant', 'Islamic combatant', 'Islamic rebel', 
    'Islamic insurgent', 'Islamic guerrilla', 'Islamic partisan', 'Islamic radical', 
    'Islamic extremist', 'Islamic fundamentalist', 'Islamic zealot', 'Islamic fanatic', 
    'Islamic jihadist','kill']

@app.route('/')
def home():
    return render_template('login.html')
    # User is not loggedin redirect to login page


@app.route('/main')
def main():
    return render_template('index.html')
    # User is not loggedin redirect to login page

@app.route('/admin_index')
def admin_index():
    return render_template('admin_index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html', )

@app.route('/ana', methods=['POST'])
def ana():
    msg = request.form.get('msg')
    url = request.form.get('url')
    detected = False
    matched_keywords = []

    # Analyze the message
    if msg:
        for keyword in keywords:
            if keyword.lower() in msg.lower():
                detected = True
                matched_keywords.append(keyword)
    
    # Analyze the URL content
    if url:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text()
            for keyword in keywords:
                if keyword.lower() in text.lower():
                    detected = True
                    matched_keywords.append(keyword)
        except Exception as e:
            print(f"Error fetching URL content: {e}")

    # Remove duplicates
    matched_keywords = list(set(matched_keywords))

    return render_template('contact.html', class1="Terrorist Activity Detected" if detected else "No Terrorist Activity Detected", res=1, keyword_match=", ".join(matched_keywords) if matched_keywords else None) 

@app.route('/con')
def cont():
    return render_template('cont.html')

#@app.route('/report')
#def report():
    #return render_template('report.html')


@app.route('/', methods=["POST"])
def login():
    if request.method == 'POST':
        username = request.form['id']
        password = request.form['pass']
        
        # List of valid usernames, passwords and their roles
        valid_credentials = {
            'admin': {'password': 'admin@123', 'role': 'admin'},
            'user': {'password': 'user@123', 'role': 'user'}
        }
        
        if username in valid_credentials and password == valid_credentials[username]['password']:
            role = valid_credentials[username]['role']
            if role == 'user':
                return redirect(url_for('main'))
            elif role == 'admin':
                return redirect(url_for('admin_index'))
        else:
            flash("Wrong username or password")
            return render_template("login.html")





@app.route('/main',methods=["POST"])
def analyze():
	if request.method == 'POST':
		msg = request.form['msg']


		# Load the saved model, vectorizer, and encoder
		model = load_model('terrorism_model.h5')
		vectorizer = joblib.load('tfidf_vectorizer.pkl')
		encoder = joblib.load('label_encoder.pkl')

		def predict(text):
			# Clean and preprocess the input text
			text_tfidf = vectorizer.transform([text]).toarray()
			
			# Predict the label
			y_pred_categorical = model.predict(text_tfidf)
			y_pred = encoder.inverse_transform(y_pred_categorical.argmax(axis=1))
			
			return y_pred[0]

		# Example usage
		input_text = msg
		predicted_label = predict(input_text)
		print("Predicted Label:", predicted_label)

		result = predicted_label
		if result == 1:
			class1 = "Terrorist Activity Detected"
			
		else:
			class1 = "No Terrosit Activity"


		return render_template('contact.html',class1=class1,res=1)


reports = []  # To store reports

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        department = request.form['department']
        
        report = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
            'department': department
        }
        reports.append(report)

        flash(f'Report sent to "{department}" successfully.')
        return redirect(url_for('report'))

    return render_template('report.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    selected_department = None
    filtered_reports = reports

    if request.method == 'POST':
        selected_department = request.form['department']
        filtered_reports = [report for report in reports if report['department'] == selected_department]

    return render_template('admin_index.html', reports=filtered_reports, selected_department=selected_department)



if __name__ == "__main__":
    app.run(debug=True)