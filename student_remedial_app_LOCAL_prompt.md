# Student Remedial Learning Application — LOCAL APP (Desktop + Mobile)
## Full Build Prompt

**Stack: Python + Django · MySQL · HTML/CSS/Vanilla JS · Anthropic Claude API**
**Type: Downloadable Local Application — Fully Responsive (Desktop + Mobile Compatible)**

---

## WHAT KIND OF APPLICATION THIS IS

This is a LOCAL APPLICATION that works on both desktop and mobile devices. It is:
- Downloaded and installed on a Windows or macOS machine
- Run by double-clicking a launcher — no browser URL to type, no internet hosting required
- Self-contained: Django runs silently in the background as a local server
- Accessed through any web browser at http://127.0.0.1:8000 on the host machine
- Also accessible from any device on the same Wi-Fi/LAN network via the host machine's local IP (e.g. http://192.168.1.x:8000) — so students can use it on their phones or tablets without installing anything
- Packaged into a single distributable folder or installer using PyInstaller

This is NOT:
- A cloud-hosted web application
- A native mobile app (no React Native / Flutter)
- A traditional desktop GUI app (no Tkinter/PyQt)

The browser is used as the rendering surface — the app behaves like a native app on both desktop and mobile browsers. The entire UI must be fully responsive using CSS media queries and mobile-first design principles.

---

## HOW THE APP STARTS (User Experience)

1. User downloads the installer or zipped folder onto a Windows or macOS machine
2. User runs the setup wizard once (enters MySQL credentials, API key)
3. From then on: user double-clicks the desktop shortcut or `Launch App` executable
4. A small system tray icon or terminal window appears showing "App is running..."
5. The default browser opens automatically to http://127.0.0.1:8000
6. Other devices (phones, tablets) on the same Wi-Fi/LAN can access the app by navigating to http://{host-machine-local-ip}:8000 in their mobile browser — no installation needed on those devices
7. User interacts with the app entirely through the browser — fully responsive on any screen size
8. Closing the launcher window / tray icon shuts down the local server

---

## TECH STACK

| Layer         | Technology                                                    |
|---------------|---------------------------------------------------------------|
| Backend       | Python 3.11 + Django 4.2                                      |
| Database      | MySQL 8.0 installed locally on user's machine (via mysqlclient) |
| Frontend      | Django Templates — HTML5 + CSS3 + Vanilla JS ONLY            |
| Responsive    | Pure CSS media queries — mobile-first, no frameworks          |
| AI Engine     | Anthropic Python SDK · Model: claude-sonnet-4-20250514        |
| Auth          | Django built-in auth + custom role middleware                 |
| Sessions      | Django DB-backed sessions                                     |
| Launcher      | Python script (launcher.py) using subprocess + webbrowser     |
| LAN Access    | Django dev server bound to 0.0.0.0:8000 for same-network devices |
| Packaging     | PyInstaller — bundles into .exe (Windows) or .app (macOS)    |
| CSS           | Custom CSS with CSS variables — NO Bootstrap / NO Tailwind    |

---

## PROJECT FOLDER STRUCTURE

```
remedial_app/
├── launcher.py                  ← MAIN ENTRY POINT — starts server, opens browser
├── setup_wizard.py              ← First-run configuration wizard
├── manage.py
├── requirements.txt
├── config.json                  ← Stores local config (DB creds, API key) after setup
├── remedial_app/                ← Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── middleware.py            ← Role-based access middleware
├── core/
│   ├── templates/
│   │   └── base.html
│   └── static/
│       └── css/
│           └── main.css
├── accounts/                    ← Auth: login, signup, logout
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/accounts/
│       ├── student_login.html
│       ├── admin_login.html
│       └── student_signup.html
├── students/                    ← Student portal
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/students/
│       ├── dashboard.html
│       ├── subject_detail.html
│       ├── learn.html
│       ├── quiz.html
│       ├── quiz_result.html
│       ├── leaderboard.html
│       └── final_result.html
├── admin_portal/                ← Admin portal
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/admin_portal/
│       ├── dashboard.html
│       ├── materials.html
│       ├── material_new.html
│       ├── students_list.html
│       ├── student_detail.html
│       └── leaderboard.html
└── quiz/                        ← AI quiz engine
    ├── models.py
    └── generator.py
```

---

## LAUNCHER SCRIPT — launcher.py (CRITICAL FILE)

This is the file the user double-clicks to start the application.

```
What launcher.py must do (in order):

1. Read config.json to load:
   - DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
   - ANTHROPIC_API_KEY
   - DJANGO_SECRET_KEY
   - LAN_ACCESS (boolean — whether to allow other devices on the network)

2. If config.json does not exist → run setup_wizard.py first

3. Inject config values into environment variables so Django settings.py can read them

4. Run Django database migrations silently:
   subprocess.run(['python', 'manage.py', 'migrate', '--run-syncdb'])

5. Run the database seeder silently:
   subprocess.run(['python', 'manage.py', 'seed_db'])

6. Detect the host machine's local IP address using socket:
   import socket
   hostname = socket.gethostname()
   local_ip = socket.gethostbyname(hostname)

7. Start Django development server:
   - If LAN_ACCESS is True: bind to 0.0.0.0:8000 so other devices can reach it
     subprocess.Popen(['python', 'manage.py', 'runserver', '0.0.0.0:8000'])
   - If LAN_ACCESS is False: bind to localhost only
     subprocess.Popen(['python', 'manage.py', 'runserver', '127.0.0.1:8000'])

8. Wait 2 seconds for server to be ready

9. Open the default browser at http://127.0.0.1:8000:
   import webbrowser
   webbrowser.open('http://127.0.0.1:8000')

10. Print access information in terminal:
    "✅ Remedial Learning App is running!"
    "   Desktop access: http://127.0.0.1:8000"
    "   Mobile/LAN access: http://{local_ip}:8000  (connect other devices to same Wi-Fi)"
    "   Close this window to stop the app."

11. Keep the launcher process alive (so the server keeps running):
    - Wait for user to close the window
    - On close: terminate the Django server subprocess
```

---

## SETUP WIZARD — setup_wizard.py (FIRST-RUN ONLY)

A simple terminal-based wizard that runs once before first launch.

```
What setup_wizard.py must do:

1. Print a welcome banner in the terminal:
   "Welcome to Student Remedial Learning App — First Time Setup"

2. Prompt user to enter:
   - MySQL Host (default: localhost)
   - MySQL Port (default: 3306)
   - MySQL Database Name (default: remedial_db)
   - MySQL Username
   - MySQL Password
   - Anthropic API Key
   - Enable LAN access for mobile/tablet? (y/n — default: y)
     (If yes: other devices on the same Wi-Fi can access the app on their phones)

3. Test the MySQL connection using the entered credentials:
   - If connection fails: print error and ask to retry
   - If connection succeeds: print "✅ Database connected successfully"

4. Create the MySQL database if it doesn't exist:
   CREATE DATABASE IF NOT EXISTS {db_name};

5. Generate a random Django SECRET_KEY (use secrets.token_urlsafe(50))

6. Detect and display the local machine IP:
   print(f"📱 Mobile access will be available at: http://{local_ip}:8000")

7. Save all values to config.json in the project root including LAN_ACCESS boolean

8. Print: "✅ Setup complete! Launching the app..."

9. Continue to launcher.py flow
```

---

## CONFIG.JSON FORMAT

```json
{
  "DB_NAME": "remedial_db",
  "DB_USER": "root",
  "DB_PASSWORD": "user_entered_password",
  "DB_HOST": "localhost",
  "DB_PORT": "3306",
  "ANTHROPIC_API_KEY": "sk-ant-...",
  "SECRET_KEY": "auto-generated-django-secret-key",
  "LAN_ACCESS": true,
  "FIRST_RUN_COMPLETE": true
}
```

---

## DJANGO SETTINGS — LOADING FROM CONFIG.JSON

settings.py must NOT use a .env file. Instead:

```
import json, os, socket

BASE_DIR = Path(__file__).resolve().parent.parent
config_path = BASE_DIR / 'config.json'

if config_path.exists():
    with open(config_path) as f:
        config = json.load(f)
else:
    config = {}

SECRET_KEY = os.environ.get('SECRET_KEY', config.get('SECRET_KEY', 'fallback-key'))
DEBUG = True

# Always allow localhost + the machine's local network IP for mobile access
def get_local_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return '127.0.0.1'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', get_local_ip(), '0.0.0.0']
# This allows phones/tablets on the same Wi-Fi to connect

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':     config.get('DB_NAME', 'remedial_db'),
        'USER':     config.get('DB_USER', 'root'),
        'PASSWORD': config.get('DB_PASSWORD', ''),
        'HOST':     config.get('DB_HOST', 'localhost'),
        'PORT':     config.get('DB_PORT', '3306'),
    }
}
```

The ANTHROPIC_API_KEY must also be read from config.json in generator.py.

---

## PYINSTALLER PACKAGING

To distribute the app as a downloadable executable:

```
PyInstaller command:
pyinstaller --onedir --noconsole --name "RemedialLearningApp" launcher.py

This creates a /dist/RemedialLearningApp/ folder containing:
  - RemedialLearningApp.exe (Windows) or RemedialLearningApp.app (macOS)
  - All bundled Python dependencies
  - Django project files

IMPORTANT PyInstaller notes:
  - Use --onedir (not --onefile) to keep Django templates/static accessible
  - Include all template folders with --add-data flags:
      --add-data "templates;templates"
      --add-data "static;static"
      --add-data "accounts/templates;accounts/templates"
      --add-data "students/templates;students/templates"
      --add-data "admin_portal/templates;admin_portal/templates"
  - Include manage.py, config.json in the dist folder
  - mysqlclient requires Microsoft Visual C++ redistributable on Windows
    (document this in README)
  - The dist folder is what gets zipped and distributed to users
```

---

## README / INSTALLATION INSTRUCTIONS (to include in the distribution)

```
=== Student Remedial Learning App — Installation Guide ===

REQUIREMENTS (user must install these separately):
  1. Python 3.11 or higher — https://python.org
  2. MySQL 8.0 Community Server — https://dev.mysql.com/downloads/
  3. Active internet connection (for AI quiz generation only)

INSTALLATION STEPS:
  1. Download and unzip RemedialLearningApp.zip
  2. Open a terminal in the unzipped folder
  3. Run: pip install -r requirements.txt
  4. Double-click launcher.py OR run: python launcher.py
  5. On first run: complete the setup wizard in the terminal
  6. The app will open automatically in your browser

USING ON DESKTOP:
  - Open http://127.0.0.1:8000 in your browser
  - Or just launch the app — it opens automatically

USING ON MOBILE / TABLET (same Wi-Fi required):
  - Make sure your phone is on the same Wi-Fi as the computer running the app
  - Check the terminal window for a line like:
    "📱 Mobile/LAN access: http://192.168.1.x:8000"
  - Open that URL in your phone's browser
  - The app is fully responsive and works on any mobile browser
  - For the best experience on iPhone/Android, tap "Add to Home Screen"
    in your browser menu to use it like a native app

EVERY DAY USAGE:
  - Just double-click launcher.py (or the packaged .exe)
  - The app opens in your browser automatically
  - Close the terminal window to stop the app

NOTE: Your data is stored locally in MySQL on this device.
      All progress, quizzes, and student records are saved permanently.
```

---

## DATABASE DESIGN

### User Model (Custom AbstractUser)
Extend Django's AbstractUser with:
- `role` field: choices are `admin` or `student`
- Set as `AUTH_USER_MODEL` in settings.py

### Subject Model
- Fields: `id`, `name` (unique)
- Pre-seeded with: Mathematics, Science, English, History, Geography

### Enrollment Model
- Fields: `student (FK)`, `subject (FK)`, `initial_marks (0–100)`, `starting_level`, `current_level`, `subject_status`
- Boolean flags: `beginner_done`, `intermediate_done`, `advanced_done`
- Unique constraint: one enrollment per student-subject pair
- Level choices: BEGINNER, INTERMEDIATE, ADVANCED
- Status choices: IN_PROGRESS, COMPLETED

### Material Model
- Fields: `subject (FK)`, `title`, `content (TextField — markdown)`, `level`, `posted_by (FK)`, `posted_at`

### Quiz Model
- Fields: `material (FK)`, `level`, `generated_at`

### Question Model
- Fields: `quiz (FK)`, `question_text`, `option_a`, `option_b`, `option_c`, `option_d`, `correct_index (0–3)`, `explanation`

### QuizAttempt Model
- Fields: `student (FK)`, `quiz (FK)`, `score (0–100)`, `passed (bool)`, `points_earned`, `attempted_at`

### LeaderboardEntry Model
- Fields: `student (OneToOne)`, `weekly_points`, `all_time_points`, `streak_days`, `last_active (date)`, `week_reset_at (datetime)`

---

## URL ROUTES

### Public Routes
| URL                     | Purpose                                        |
|-------------------------|------------------------------------------------|
| `/`                     | Landing page — two portal entry buttons        |
| `/student/login/`       | Student login                                  |
| `/student/signup/`      | Student registration + subject/marks selection |
| `/admin-portal/login/`  | Admin login                                    |
| `/logout/`              | Clear session, redirect to landing             |

### Student Routes (role=student required)
| URL                                      | Purpose                               |
|------------------------------------------|---------------------------------------|
| `/student/dashboard/`                    | Subject cards with progress overview  |
| `/student/subject/<subject_id>/`         | Level breakdown for one subject       |
| `/student/learn/<material_id>/`          | Study page with timer + content       |
| `/student/quiz/<quiz_id>/`               | Take the AI-generated quiz            |
| `/student/quiz-result/<attempt_id>/`     | Score, promotion result, points       |
| `/student/leaderboard/`                  | Weekly and all-time leaderboard       |
| `/student/final-result/`                 | Final certificate (strictly gated)    |

### Admin Routes (role=admin required)
| URL                                       | Purpose                              |
|-------------------------------------------|--------------------------------------|
| `/admin-portal/dashboard/`                | Overview stats and counts            |
| `/admin-portal/materials/`                | List all posted materials            |
| `/admin-portal/materials/new/`            | Post material (triggers AI gen)      |
| `/admin-portal/students/`                 | All students list                    |
| `/admin-portal/students/<student_id>/`    | Individual student progress view     |
| `/admin-portal/leaderboard/`              | Read-only leaderboard                |

---

## CORE BUSINESS LOGIC

### 1. Student Signup
- Fields: name, email, password, confirm password
- Subject selection via checkboxes (5 subjects shown)
- For each checked subject: a marks input field appears (Vanilla JS — no page reload)
- On submit:
  - Create User with role='student'
  - For each selected subject + marks:
    - marks < 40 → BEGINNER (no auto-completion)
    - 40 ≤ marks < 70 → INTERMEDIATE (beginner_done = True)
    - marks ≥ 70 → ADVANCED (beginner_done = True, intermediate_done = True)
  - Create Enrollment record for each, set current_level = starting_level
  - Create LeaderboardEntry for student
  - Log student in and redirect to dashboard

### 2. Learn Page + Timer
- Render material content (convert markdown → HTML server-side)
- JavaScript starts a 60-second countdown on page load
- Timer state stored in localStorage with key: `timer_done_<material_id>_<student_id>`
- If key already "true": quiz button immediately enabled (student visited before)
- On timer expiry: set localStorage key to "true", enable quiz button
- Quiz button links to quiz for the student's current level on this subject

### 3. Quiz Submission + Promotion
- 10 MCQ questions answered one at a time
- Score = (correct answers ÷ 10) × 100
- Promotion thresholds:
  - BEGINNER: score ≥ 70 → promote to INTERMEDIATE
  - INTERMEDIATE: score ≥ 75 → promote to ADVANCED
  - ADVANCED: score ≥ 80 → mark subject COMPLETED
- Failed attempts: unlimited retries allowed
- On retry: generate a brand new quiz from Claude API (delete old quiz first)
- On pass: update enrollment flags and current_level in database

### 4. Points Calculation
After every quiz submission:
- Level multipliers: BEGINNER = 1.0×, INTERMEDIATE = 1.5×, ADVANCED = 2.0×
- base_points = score number (e.g. score of 82 = 82 base points)
- level_points = base_points × multiplier
- Bonus points:
  - +50 if this attempt causes a level promotion
  - +100 if this attempt completes the entire subject
  - +20 streak bonus if student was also active the previous day
- total = level_points + bonuses (rounded to integer)
- Update LeaderboardEntry: add total to weekly_points AND all_time_points
- Update streak_days: compare last_active date with today

### 5. Weekly Leaderboard Reset (No Background Process)
- On every leaderboard page load (student or admin):
  - Calculate this week's Monday at 00:00:00
  - Find all LeaderboardEntry rows where week_reset_at < that Monday
  - Set weekly_points = 0 and week_reset_at = this Monday for those rows
  - all_time_points is NEVER touched by this reset

### 6. Final Result Gate
- On every request to /student/final-result/:
  - Fetch all enrollments for current student
  - If any enrollment has subject_status != COMPLETED → redirect to dashboard
  - Only if ALL enrollments are COMPLETED → render certificate page

### 7. Admin Post Material
- Admin submits: subject, level, title, content
- Save Material to database
- Immediately call AI generator for ALL THREE levels (BEGINNER, INTERMEDIATE, ADVANCED)
- 30 questions saved to database (10 per level)
- Show success flash message

### 8. Role Middleware
Custom Django middleware protecting all routes:
- /student/* → must be authenticated with role='student'
- /admin-portal/* (except /login/) → must be authenticated with role='admin'
- Public routes: /, /student/login/, /student/signup/, /admin-portal/login/, /logout/

---

## AI QUIZ GENERATION — FULL SPECIFICATION

### Trigger Points
1. When admin posts a new material → generate for all 3 levels simultaneously
2. When student clicks Retry after failing → generate fresh quiz for that level only

### Claude API Setup (quiz/generator.py)
- Import: `import anthropic`
- Load API key from config.json (not from environment or .env)
- Model: `claude-sonnet-4-20250514`
- Max tokens: 4000

### Level Descriptions for Prompt
- BEGINNER: Basic recall and simple comprehension. Simple language. Test whether the student remembers key facts and definitions from the material.
- INTERMEDIATE: Application and analysis. Require the student to apply concepts, compare ideas, and explain relationships — not just recall.
- ADVANCED: Evaluation, synthesis, and critical thinking. Ask about edge cases, implications, real-world applications, and nuanced understanding requiring deep mastery.

### Exact Prompt to Send Claude
```
You are an expert educational quiz generator.

Generate exactly 10 multiple-choice questions from the study material below.

Subject: {subject_name}
Topic / Title: {material_title}
Difficulty Level: {BEGINNER | INTERMEDIATE | ADVANCED}
Level Guidance: {level description from above}

Study Material:
"""
{material_content}
"""

Rules:
- Each question must have exactly 4 answer options (A, B, C, D)
- Only one option is correct per question
- Questions must only be based on the provided material above
- Include a brief explanation for why the correct answer is right
- correctAnswer is 0-indexed: 0 = A, 1 = B, 2 = C, 3 = D

Return ONLY a valid JSON array. No markdown formatting, no code fences, no preamble, no extra text.

[
  {
    "question": "...",
    "options": ["Option A text", "Option B text", "Option C text", "Option D text"],
    "correctAnswer": 2,
    "explanation": "..."
  }
]
```

### Response Handling
- Strip any markdown code fences (```json ... ```) if present before JSON parsing
- Create one Quiz record per level linked to the material
- Create 10 Question records per Quiz
- If generation fails for one level: log the error, continue with other levels
- On retry: delete existing Quiz (and cascade delete Questions) for material+level, then generate fresh

---

## FRONTEND DESIGN SPECIFICATION

### Design Language
- Clean academic desktop-app feel that scales beautifully to mobile
- Dark navy sidebar (#0F172A), white content area, blue accent (#4F8EF7)
- Google Fonts: 'Outfit' (headings) + 'Inter' (body)
- All colors as CSS custom properties
- No external CSS frameworks — pure custom CSS with media queries only
- Mobile-first approach: base styles are for mobile, desktop overrides via `min-width` media queries

---

### RESPONSIVE DESIGN SPECIFICATION (CRITICAL)

Every single page must work perfectly on the following screen sizes:
- Mobile portrait:  320px – 480px  (e.g. small Android phones)
- Mobile landscape: 481px – 767px  (e.g. iPhone landscape)
- Tablet:           768px – 1024px (e.g. iPad)
- Desktop:          1025px+        (e.g. laptop/PC)

#### Breakpoints (define as CSS variables or use consistently)
```
--bp-mobile:  480px
--bp-tablet:  768px
--bp-desktop: 1025px

Media queries to use:
  @media (max-width: 480px)  { /* mobile portrait only */ }
  @media (max-width: 767px)  { /* all mobile sizes */      }
  @media (min-width: 768px)  { /* tablet and up */         }
  @media (min-width: 1025px) { /* desktop only */          }
```

#### Sidebar Behavior (most important responsive element)
- DESKTOP (1025px+): Fixed left sidebar, always visible, 240px wide. Main content has margin-left: 240px.
- TABLET (768px–1024px): Collapsible sidebar — hidden by default, slides in from left when hamburger menu button is tapped. Sidebar overlaps content (position: fixed) with a dark overlay behind it.
- MOBILE (< 768px): No sidebar at all. Replace with a bottom navigation bar fixed to the bottom of the screen with icon + label for: Dashboard, Subjects, Leaderboard, Profile.

#### Bottom Navigation Bar (mobile only — < 768px)
- Fixed position at bottom of screen (position: fixed; bottom: 0; left: 0; right: 0)
- Height: 60px
- Background: --sidebar-bg (#0F172A)
- 4 items evenly spaced: Dashboard (🏠), Subjects (📚), Leaderboard (🏆), Profile (👤)
- For admin mobile: Dashboard (🏠), Materials (📄), Students (👥), Leaderboard (🏆)
- Active item highlighted with --primary color
- Text label below each icon, font-size: 10px

#### Hamburger Menu Button (tablet only — 768px–1024px)
- Shown in top-left corner of the top navbar on tablet
- On click (Vanilla JS): toggle sidebar open/closed, show/hide dark overlay
- Overlay click also closes sidebar
- Sidebar slides in with CSS transition: transform: translateX(-100%) → translateX(0)

#### Top Navigation Bar
- DESKTOP: Shows app name/logo on left, user name + logout on right. No hamburger.
- TABLET: Shows hamburger button on left, app name in center, logout icon on right.
- MOBILE: Shows app name in center, only a logout icon button on right. No hamburger (uses bottom nav instead).
- Height: 56px on mobile, 64px on desktop

#### Typography Scaling
```
/* Mobile base sizes */
h1: 1.5rem
h2: 1.25rem
h3: 1.1rem
body: 0.9rem
buttons: 0.85rem

/* Desktop sizes */
@media (min-width: 1025px) {
  h1: 2rem
  h2: 1.5rem
  h3: 1.2rem
  body: 1rem
  buttons: 0.95rem
}
```

#### Grid and Layout Rules
- Dashboard subject cards: 1 column on mobile, 2 columns on tablet, 2–3 columns on desktop
- Admin stat cards: 1 column on mobile, 2 columns on tablet, 4 columns on desktop
- All CSS grids use: `grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))`
- No horizontal scrolling allowed on any page at any breakpoint
- All tables must become scrollable horizontally on mobile (overflow-x: auto on wrapper div)
- Padding: 12px on mobile, 20px on tablet, 32px on desktop

#### Touch-Friendly Interactive Elements
- All buttons minimum height: 44px (Apple HIG standard for touch targets)
- All clickable list items minimum height: 48px
- Quiz option buttons: full-width on mobile, comfortable padding (16px top/bottom)
- No hover-only states — all hover effects must also work on tap/focus
- Form inputs minimum height: 44px, font-size minimum 16px (prevents iOS zoom on focus)
- Touch target spacing: minimum 8px gap between any two tappable elements

#### Page-Specific Responsive Rules

LEARN PAGE (most complex layout):
- DESKTOP: Two-column layout (65% content, 35% sticky sidebar panel)
- TABLET: Two-column layout (70% content, 30% sticky panel) but panel is less wide
- MOBILE: Single column. Timer panel moves to TOP of page (above content), not sidebar. Quiz button is full-width, sticky at bottom of viewport when timer done.

QUIZ PAGE:
- All screen sizes: single column, centered
- Option buttons: full-width on mobile, 80% width centered on desktop
- Progress bar: full-width on all sizes
- "Next" button: full-width on mobile, auto-width centered on desktop

LEADERBOARD TABLE:
- DESKTOP: Full table with all columns visible
- TABLET: All columns, slightly smaller text
- MOBILE: Horizontal scroll on table wrapper, OR collapse to card-style rows where each row shows: rank + name on top line, points + streak on second line

ADMIN MATERIAL FORM:
- DESKTOP: Two-column layout (label left, input right) for Subject and Level fields
- MOBILE: Single column, all fields full-width, label above input

STUDENT SIGNUP SUBJECT CARDS:
- DESKTOP: 3-column grid of subject checkbox cards
- TABLET: 2-column grid
- MOBILE: 1-column, full-width cards, marks input below each card

FINAL RESULT / CERTIFICATE PAGE:
- DESKTOP: Centered certificate box with decorative border, max-width 700px
- MOBILE: Full-width, reduced decorative elements, font sizes scaled down, still celebratory

#### CSS File Organization
Organize main.css in this order:
1. CSS custom properties (:root variables)
2. CSS reset / box-sizing
3. Base mobile-first styles (applies to all sizes)
4. Component styles (cards, buttons, forms, badges, tables)
5. Layout: sidebar + main content (desktop default)
6. @media (max-width: 767px) — mobile overrides: bottom nav, no sidebar, single column
7. @media (min-width: 768px) and (max-width: 1024px) — tablet overrides: hamburger sidebar
8. @media (min-width: 1025px) — desktop enhancements

#### Viewport Meta Tag (MUST be in base.html)
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
```

#### PWA-Like Mobile Feel (Optional Enhancement)
Add to base.html for better mobile experience:
```html
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="theme-color" content="#0F172A">
```
This makes the browser chrome match the app color when added to home screen on iOS/Android.

---

### CSS Variables (main.css)
```
:root {
  --primary:       #4F8EF7;
  --primary-dark:  #2563EB;
  --success:       #22C55E;
  --danger:        #EF4444;
  --warning:       #F59E0B;
  --bg:            #F8FAFC;
  --sidebar-bg:    #0F172A;
  --sidebar-text:  #CBD5E1;
  --card-bg:       #FFFFFF;
  --border:        #E2E8F0;
  --text-primary:  #1E293B;
  --text-muted:    #64748B;
  --radius:        12px;
  --shadow:        0 1px 3px rgba(0,0,0,0.08), 0 4px 16px rgba(0,0,0,0.05);
}
```

### Template Structure
```
base.html  (HTML boilerplate, CSS link, font imports)
  ├── student_base.html  → sidebar links: Dashboard, Subjects, Leaderboard, Final Result
  └── admin_base.html   → sidebar links: Dashboard, Materials, Students, Leaderboard
```

### Page-by-Page UI Requirements

**Landing Page (`/`)**
- Full-height split screen: left side = app branding and tagline, right side = two portal cards
- Student Portal card and Admin Portal card, each with icon + button
- Professional, welcoming design with app name prominently displayed

**Student Signup (`/student/signup/`)**
- Multi-section form on one page (no multi-step wizard)
- Section 1: Personal info (name, email, password, confirm password)
- Section 2: Subject selection — 5 subject checkboxes displayed as cards
- When a subject checkbox is checked (Vanilla JS): a marks input (0–100) slides in below that card
- Helper text beneath each marks input: "< 40 = Beginner | 40–69 = Intermediate | ≥ 70 = Advanced"
- Submit button at bottom

**Student Dashboard (`/student/dashboard/`)**
- Header: "Welcome back, {name}" + total points badge
- 2-column grid of subject cards (1 column on smaller screens)
- Each card shows: subject name + icon, current level badge (color-coded), progress bar (e.g. 1 of 3 levels complete), subject status chip (IN PROGRESS / COMPLETED), "Continue Learning" button

**Learn Page (`/student/learn/<material_id>/`)**
- Two-column layout: 65% left content area, 35% right sticky panel
- Left: Material title (h1), then markdown content rendered as HTML (paragraphs, headings, lists, code blocks)
- Right sticky panel: circular countdown timer (shows seconds remaining), lock icon + "Read material to unlock quiz" message, quiz button that is disabled and grayed until timer finishes
- On timer completion: button turns blue, icon changes to checkmark, text changes to "✅ Take Quiz Now"
- Timer Vanilla JS uses localStorage to persist state across page refreshes
- localStorage key format: `timer_done_{material_id}_{student_id}`

**Quiz Page (`/student/quiz/<quiz_id>/`)**
- Top: horizontal progress bar + "Question X of 10" text
- Center: question text displayed prominently
- Below: four option buttons (A, B, C, D) — clicking one adds a `.selected` class visually
- Bottom: "Next Question" button (disabled if no option selected)
- Last question: button text changes to "Submit Quiz"
- All selected answers stored in hidden form inputs
- Submitted as single POST — no intermediate AJAX calls

**Quiz Result Page (`/student/quiz-result/<attempt_id>/`)**
- Large circular score display in center (e.g. "85%")
- PASS (green) or FAIL (red) badge beneath the score
- Points breakdown card:
  - Base Points: {score}
  - × Level Multiplier ({1.0× / 1.5× / 2.0×}) = {level_points}
  - Promotion Bonus: +{50 or 0}
  - Subject Complete Bonus: +{100 or 0}
  - Streak Bonus: +{20 or 0}
  - Total Points Earned: {total}
- If promoted: animated banner "🎉 Promoted to [INTERMEDIATE / ADVANCED]!"
- If subject fully complete: "🏆 Subject Complete!" banner
- Action buttons: "Retry Quiz" (if failed) | "Back to Dashboard" | "Next Subject" (if applicable)

**Leaderboard Page (`/student/leaderboard/`)**
- Two tab buttons: "This Week" and "All Time"
- Tab content switches via Vanilla JS (no page reload, toggle display CSS)
- Table columns: Rank | Name | Points | Streak
- Top 3 rows show medal icons: 🥇 🥈 🥉
- Current student's row highlighted in blue with "(You)" label
- Weekly reset note: "Resets every Monday at midnight"

**Final Result Page (`/student/final-result/`)**
- Only renders if ALL enrolled subjects are COMPLETED (403 or redirect otherwise)
- Certificate-style layout: decorative border, app logo, student name in large font
- "Certificate of Completion" heading
- List of all completed subjects with completion dates
- Total all-time points earned displayed
- Congratulatory message
- CSS-only celebration animation (e.g. confetti or glow pulse effect)

**Admin Dashboard (`/admin-portal/dashboard/`)**
- Stat cards row: Total Students | Total Materials Posted | Quizzes Generated | Active This Week
- Recent activity list: latest quiz attempts across all students
- Quick action buttons: Post New Material | View Students

**Admin Material Form (`/admin-portal/materials/new/`)**
- Form fields: Subject (dropdown), Level (dropdown: BEGINNER / INTERMEDIATE / ADVANCED), Title (text input), Content (large textarea — user types markdown)
- Below content field: "Tip: Your content will be used by AI to generate 10 quiz questions per level"
- Submit button behavior (Vanilla JS): on click → disable button → show spinner → change text to "🤖 Generating AI Quiz Questions..."
- On redirect back: flash success message "Material posted! 30 AI questions generated across 3 levels."

**Admin Student Detail (`/admin-portal/students/<student_id>/`)**
- Student header: name, email, join date, total points, current rank
- Per-subject accordion (click to expand/collapse — Vanilla JS)
- Inside each accordion: level rows showing status (✅ Complete / ⏳ In Progress / 🔒 Not Yet Reached), quiz attempt history table (date, score, pass/fail, points earned)

---

## DATABASE SEEDING

Create Django management command at:
`accounts/management/commands/seed_db.py`

Run automatically from launcher.py on every startup (the command must be idempotent — use get_or_create so it doesn't duplicate data).

Seed the following:
1. Five subjects: Mathematics, Science, English, History, Geography
2. Two admin accounts:
   - Username: admin | Email: admin@school.com | Password: Admin@123
   - Username: principal | Email: principal@school.com | Password: Admin@123

---

## REQUIREMENTS.TXT

```
Django==4.2.9
mysqlclient==2.2.4
anthropic==0.25.0
markdown==3.5.2
PyInstaller==6.3.0
```

---

## BUILD ORDER (Recommended Implementation Sequence)

1. Set up Django project with MySQL connection (read from config.json)
2. Write setup_wizard.py — terminal prompts, DB connection test, LAN access option, config.json creation
3. Write launcher.py — reads config, detects local IP, binds to 0.0.0.0 or 127.0.0.1, runs migrations, seeds DB, starts server, opens browser, prints LAN access URL
4. Create custom User model with role field, run first migration
5. Build accounts app: landing page, student login, admin login, student signup with dynamic JS subject-marks form
6. Create Subject, Enrollment, LeaderboardEntry models — implement signup enrollment logic with auto-level-completion
7. Create quiz app: Quiz, Question, QuizAttempt models
8. Implement AI quiz generator (quiz/generator.py) using Anthropic Claude API
9. Build admin portal: material list + material post form + trigger quiz generation on save
10. Build student learn page with 60-second localStorage timer in Vanilla JS
11. Build quiz page: one-question-at-a-time Vanilla JS interface, form submission, scoring logic
12. Implement promotion logic, level advancement, subject completion detection
13. Build quiz result page with full points breakdown display
14. Implement points calculation and LeaderboardEntry update after each quiz
15. Build leaderboard page with weekly reset logic on page load
16. Build admin student detail view (read-only progress accordion)
17. Build final result page with server-side gate check
18. Apply full CSS design system — start mobile-first, then add tablet and desktop breakpoints
19. Implement bottom navigation bar for mobile (< 768px)
20. Implement hamburger + slide-in sidebar for tablet (768px–1024px)
21. Implement fixed sidebar for desktop (1025px+)
22. Test responsive layout at every breakpoint on Chrome DevTools (320px, 480px, 768px, 1024px, 1280px)
23. Test touch targets — all buttons must be at least 44px tall on mobile
24. Test full student journey: signup → learn → quiz → promote → complete → final result
25. Test admin journey: login → post material → view student progress
26. Test LAN mobile access: open app URL on a real phone on same Wi-Fi
27. Test PyInstaller packaging on Windows and macOS
28. Write distribution README with installation and mobile access instructions

---

## KEY CONSTRAINTS & RULES

- Admins CANNOT take quizzes, enroll in subjects, or visit any /student/ route — middleware blocks this
- Students CANNOT post materials or visit any /admin-portal/ route — middleware blocks this
- Quiz questions are NEVER manually entered — all questions come exclusively from Claude API
- Progress is NEVER lost — all state is in MySQL, persists across app restarts
- Timer state uses localStorage so browser refresh does not restart the 60-second timer
- Weekly leaderboard reset happens on page load (not a background process) — no need for cron
- Weekly reset only zeros out weekly_points — all_time_points is sacred and never decremented
- Retry always generates completely new questions — the old quiz record is deleted before generating
- Final Result page enforces the gate check on every request — not just on first visit
- config.json must NEVER be committed to version control if the app is open-sourced
- When LAN_ACCESS = true: server binds to 0.0.0.0:8000 and ALLOWED_HOSTS includes local IP
- When LAN_ACCESS = false: server binds to 127.0.0.1:8000 only — not reachable from other devices
- All database operations are local — student data never leaves the user's LAN
- Internet is only required for the Anthropic API calls (quiz generation) — all other features work offline
- ALL pages must be fully functional at 320px width — no horizontal overflow permitted anywhere
- Bottom navigation bar is used on mobile (< 768px) — sidebar is hidden entirely on mobile
- Hamburger + collapsible sidebar is used on tablet (768px–1024px)
- Fixed sidebar is used on desktop (1025px+)
- All touch targets (buttons, links, inputs) must be a minimum of 44px in height on mobile
- Form input font-size must be minimum 16px to prevent iOS Safari from zooming on focus
- No functionality may be hidden or inaccessible on mobile — everything available on desktop must also be reachable on mobile, just in a different layout

---

*Prompt prepared for: Student Remedial Learning Application (Local App — Desktop + Mobile)*
*Stack: Django 4.2 · MySQL · HTML/CSS/Vanilla JS · Anthropic Claude API*
*Distribution: PyInstaller packaged executable · LAN access for mobile devices*
