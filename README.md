
# SkillSphere Career Guidance System

SkillSphere is an AI-powered web application that provides personalized career and college recommendations based on a student's academic profile, interests, and goals. Leveraging advanced AI models, SkillSphere helps students make informed decisions about their future education and career paths.

---

## 🚀 How SkillSphere Works

1. Users enter their academic background, interests, and goals.
2. The system analyzes the input using predefined logic.
3. Personalized career and college recommendations are generated.

---

## 🚀 Features

- **Personalized Career Recommendations:** Get tailored career suggestions based on your academic strengths, interests, and preferences.
- **College Matching:** Receive a curated list of colleges/universities that align with your profile, location, and budget.
- **Actionable Roadmap:** Obtain a step-by-step roadmap to achieve your career goals, including academic, extracurricular, and skill-building milestones.
- **Modern Web Interface:** Simple, user-friendly interface for input and results.
- **Save Reports:** Download your personalized recommendations and roadmap for future reference in txt file.

---

## 📸 Screenshots

The following screenshots showcase the current SkillSphere user interface.  
Actual recommendations may vary based on user input.

### 🏠 Landing Page
Users can choose to create a new account or log in as an existing user to begin receiving personalized career guidance.

![Landing Page](screenshots/landing-page.png)

---

### 📝 User Profile Input Form
Users provide academic details, interests, hobbies, and preferences which are used to generate personalized career and college recommendations.

![User Input Form](screenshots/user-input-form.png)

---

### 🎨 UI Layout Reference
This image represents the intended structure and layout of the SkillSphere input interface for clarity and consistency.

![UI Reference](screenshots/ui-reference.png)

---

## 🗂️ Project Structure

```
SkillSphere/
├── app.py                  
├── core/
│   ├── __init__.py       
│   ├── models.py          
│   ├── recommendation_system.py  
│   ├── user_input.py      
│   └── utils.py          
├── static/
│   └── css/
│       └── style.css      
├── templates/
│   ├── index.html         
│   └── results.html      
├── requirements.txt   
|___screenshots    
└── README.md  
          
```

---

## 🛠️ Installation

1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd SkillSphere
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

---

## 💡 Usage

1. **Start the application:**
   ```sh
   python app.py
   ```

2. **Open your browser:**
   Go to [http://127.0.0.1:5000](http://127.0.0.1:5000)

3. **Fill out your profile:**
   Enter your academic details, interests and preferences, then submit the form to receive your personalized recommendations and roadmap.

4. **Save your results:**
   Download your Recommendations and Roadmap for future planning.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for suggestions, bug fixes, or improvements.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
