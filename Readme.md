# Anxiety Diagnosis Game

An interactive web app built with **Django** and **Tailwind CSS** that helps users subtly identify potential anxiety disorder traits based on their choices. The game is inspired by DSM-5 categories and provides a simple, user-friendly quiz experience with a modern UI and dark mode support.

---

## Features

- Interactive quiz with multiple choice questions
- Tracks user answers and calculates scores per anxiety disorder type
- Provides a diagnosis summary with score breakdown
- Dark mode toggle with preference saved across sessions
- Session-based gameplay (no login required)
- Kenyan-themed questions for local relatability

---

## Tech Stack

- **Backend:** Django 4.x
- **Frontend:** Tailwind CSS, vanilla JavaScript
- **Database:** PostgreSQL (recommended), SQLite for quick setup
- **Other:** UUID for unique session/question IDs, localStorage for theme persistence

---

## Setup & Installation

1. **Clone the repo:**

   ```bash
   git clone https://github.com/yourusername/anxiety-diagnosis-game.git
   cd anxiety-diagnosis-game
2. Create and activate a virtual environment:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt

4. Configure your database settings in settings.py.

5. Run migrations:

bash
Copy
Edit
python manage.py migrate

6. Load initial questions fixture:

bash
Copy
Edit
python manage.py loaddata initial_questions.json

7. Run the development server:

bash
Copy
Edit
python manage.py runserver

8. Open your browser at: http://localhost:8000

9. Usage
Click Start Game to begin the quiz.

Choose the answers that best fit your feelings or experiences.

After answering all questions, view your diagnosis and score breakdown.

Use the dark mode toggle at the top-right to switch themes.

Replay anytime by clicking the Play Again button on the results page.

10. Project Structure
game/ - Django app containing models, views, urls, templates, and static files

game/fixtures/initial_questions.json - initial data for questions and choices

templates/ - HTML templates using Django template language

static/ - Tailwind CSS and JavaScript files

Customization
Add or update questions in the JSON fixture file.

Adjust scoring or add new anxiety disorder types in models.py.

Modify UI styles by editing Tailwind classes in templates.

Contribution
Feel free to fork, open issues, or submit pull requests!
Let’s make mental health awareness fun and accessible.

License
This project is open source under the MIT License.

Contact
Created by Quasi Maina
GitHub: https://github.com/quasimaina
Email: your.email@example.com

yaml
Copy
Edit

