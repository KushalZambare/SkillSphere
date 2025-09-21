
# SkillSphere Career Guidance System

SkillSphere is an AI-powered web application that provides personalized career and college recommendations based on a student's academic profile, interests, and goals. Leveraging advanced AI models, SkillSphere helps students make informed decisions about their future education and career paths.

---

## 🚀 Features

- **Personalized Career Recommendations:** Get tailored career suggestions based on your academic strengths, interests, and preferences.
- **College Matching:** Receive a curated list of colleges/universities that align with your profile, location, and budget.
- **Actionable Roadmap:** Obtain a step-by-step roadmap to achieve your career goals, including academic, extracurricular, and skill-building milestones.
- **Modern Web Interface:** Simple, user-friendly interface for input and results.
- **Save Reports:** Download your personalized recommendations and roadmap for future reference.

---

## 🗂️ Project Structure

```
SkillSphere/
├── app.py                  # Main Flask application
├── core/
│   ├── __init__.py        # Core module initializer
│   ├── models.py          # Data models for user and recommendations
│   ├── recommendation_system.py  # AI-powered recommendation logic
│   ├── user_input.py      # User profile creation and parsing
│   └── utils.py           # Utility functions (API, parsing, saving)
├── static/
│   └── css/
│       └── style.css      # Application styles
├── templates/
│   ├── index.html         # User input form
│   └── results.html       # Results display page
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
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
   Enter your academic details, interests, and preferences, then submit the form to receive your personalized recommendations and roadmap.

4. **Save your results:**
   Download your recommendations and roadmap for future planning.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for suggestions, bug fixes, or improvements.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.