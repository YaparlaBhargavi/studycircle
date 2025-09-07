import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- Streamlit Page Config ---
st.set_page_config(page_title="StudyCircle", layout="wide")


def send_email(to_email, subject, body):
    sender_email = "yaparlabhargaviv@gmail.com"  # Change to your email
    # It's crucial to remove spaces from the password
    sender_password = "xfrjdzhgvalhtbbw"  # This should be your App Password without spaces

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        print(f"✅ Email sent to {to_email}")
    except smtplib.SMTPException as e:
        print(f"❌ SMTP Error: {e}")
        # Log the full error to a file
        with open("email_errors.log", "a") as f:
            f.write(f"{datetime.now()}: Failed to send email to {to_email} with error: {e}\n")
    except Exception as e:
        print(f"❌ General Error: {e}")
        with open("email_errors.log", "a") as f:
            f.write(f"{datetime.now()}: Failed to send email to {to_email} with a general error: {e}\n")

# --- CSS Styling with Glass UI and Animations ---
def apply_custom_css():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
            @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');
            
            :root {
                --primary-color: #6a11cb;
                --secondary-color: #2575fc;
                --background-color-start: #f4f7f9;
                --background-color-end: #e5eef7;
                --glass-bg: rgba(255, 255, 255, 0.4);
                --glass-border: rgba(255, 255, 255, 0.2);
                --text-color: #333333;
                --card-bg-color: rgba(255, 255, 255, 0.5);
                --accent-hover: #4d0099;
                --animation-duration: 0.3s;
            }

            body {
                font-family: 'Poppins', sans-serif;
                background: url("https://media.istockphoto.com/id/1060478984/photo/background-blue-gradient-abstract.jpg?s=612x612&w=0&k=20&c=7p-t1Lrtla7jPHzgiudd97O0JUOLHkL5aTbr-VA3Wrw=") no-repeat center center fixed;
                background-size: cover;
                background-attachment: fixed;
            }

            .stApp {
                color: var(--text-color);
                background: url("https://media.istockphoto.com/id/1060478984/photo/background-blue-gradient-abstract.jpg?s=612x612&w=0&k=20&c=7p-t1Lrtla7jPHzgiudd97O0JUOLHkL5aTbr-VA3Wrw=") no-repeat center center fixed;
                background-size: cover;
            }
            .st-emotion-cache-18ni7ap {
                padding-top: 0rem;
            }

            .glass-container {
                background: var(--glass-bg);
                border-radius: 16px;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border: 1px solid var(--glass-border);
                padding: 20px;
                margin-bottom: 20px;
                transition: transform var(--animation-duration) ease-in-out, box-shadow var(--animation-duration) ease-in-out;
            }
            .glass-container:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
            }

            .navbar {
                display: flex;
                justify-content: flex-end;
                background-color: transparent;
                padding: 15px;
                border-bottom: 1px solid transparent;
            }
            .navbar a {
                margin-left: 20px;
                text-decoration: none;
                font-weight: 600;
                color: var(--text-color);
                font-size: 18px;
                transition: color var(--animation-duration) ease-in-out, transform var(--animation-duration) ease-in-out;
            }
            .navbar a:hover {
                color: var(--primary-color);
                transform: scale(1.1);
            }

            h1, h2, h3, h4 {
                color: var(--primary-color);
                transition: color var(--animation-duration) ease-in-out;
            }
            
            .stButton > button {
                background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
                color: white;
                border-radius: 8px;
                border: none;
                padding: 12px 25px;
                font-weight: 700;
                cursor: pointer;
                text-transform: uppercase;
                letter-spacing: 1px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                transition: all var(--animation-duration) ease;
            }
            .stButton > button:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 20px rgba(0,0,0,0.2);
            }
            .stButton > button:active {
                transform: translateY(0);
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            }
            
            .stSuccess, .stInfo, .stError, .stWarning {
                border-left: 5px solid;
                padding: 1rem;
                margin-bottom: 1rem;
                border-radius: 5px;
                background: var(--glass-bg);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
            }
            .stSuccess { border-color: #28a745; }
            .stInfo { border-color: var(--primary-color); }
            .stError { border-color: #dc3545; }
            .stWarning { border-color: #ffc107; }
            
            .st-emotion-cache-16idsys {
                background: transparent;
                padding: 0;
            }
            
            .st-emotion-cache-10o42p7 {
                background: var(--glass-bg);
                border-radius: 16px;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border: 1px solid var(--glass-border);
                margin-bottom: 20px;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .fade-in {
                animation: fadeIn 0.5s ease-in-out forwards;
            }

            .hero-section {
                text-align: center;
                padding: 50px 20px;
                background: var(--glass-bg);
                border-radius: 20px;
                margin-bottom: 30px;
            }
            .hero-section h1 {
                font-size: 4rem;
                font-weight: 800;
                background: linear-gradient(45deg, #6a11cb, #2575fc);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: pulse 2s infinite ease-in-out;
            }
            .hero-section p {
                font-size: 1.5rem;
                color: var(--text-color);
                margin-top: 10px;
                font-weight: 300;
            }
            
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.02); }
                100% { transform: scale(1); }
            }

            .feature-card {
                text-align: center;
                padding: 20px;
                border-radius: 12px;
                background: rgba(255, 255, 255, 0.5);
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                transition: transform 0.2s ease-in-out, background var(--animation-duration) ease;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            .feature-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 20px rgba(0,0,0,0.15);
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(255, 255, 255, 0.6) 100%);
            }
            .feature-card .icon {
                font-size: 3rem;
                background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 10px;
            }
            .feature-card h4 {
                font-weight: 600;
                margin-top: 0;
            }

            .home-section-title {
                text-align: center;
                margin-bottom: 30px;
                font-size: 2.5rem;
                color: var(--primary-color);
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 2px;
            }
            
            .feature-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
            }
            
            .alert-glow {
                animation: glow 1.5s infinite ease-in-out alternate;
            }
            
            @keyframes glow {
                from { box-shadow: 0 0 5px rgba(255, 193, 7, 0.4); }
                to { box-shadow: 0 0 20px rgba(255, 193, 7, 0.8); }
            }

            /* Responsive adjustments */
            @media (max-width: 768px) {
                .hero-section h1 {
                    font-size: 2.5rem;
                }
                .hero-section p {
                    font-size: 1rem;
                }
                .home-section-title {
                    font-size: 2rem;
                }
            }

        </style>
    """, unsafe_allow_html=True)
    
# --- DB Connection ---
def get_connection():
    """Establishes a connection to the MySQL database."""
    # IMPORTANT: Update these credentials for your local MySQL setup.
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="cseds@32",
        database="circle"
    )

# --- User Functions ---
def register_user(name, email, password):
    """Registers a new user in the database."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        conn.commit()
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def authenticate_user(email, password):
    """Authenticates a user and returns their data."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
        return None
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def get_subjects():
    """Fetches all available subjects from the database."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM subjects")
        return [row[0] for row in cursor.fetchall()]
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
        return []
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def show_chat(subject):
    """Displays the chat feed for a given subject."""
    st.markdown("#### 🧑‍💻 Chat Feed")
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.message, u.name, c.timestamp 
            FROM chat c JOIN users u ON c.user_id = u.id
            WHERE c.subject = %s ORDER BY c.timestamp DESC LIMIT 10
        """, (subject,))
        chats = cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
        chats = []
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

    for chat in chats[::-1]:
        st.write(f"**{chat['name']}** ({chat['timestamp'].strftime('%Y-%m-%d %H:%M')}): {chat['message']}")

def log_new_topic(user_id, subject, topic):
    """Logs a new topic in the progress tracking table."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO progress_tracking (user_id, subject, topic_name, progress_status) 
            VALUES (%s, %s, %s, %s)
        """, (user_id, subject, topic, 'Not Started'))
        conn.commit()
        st.success(f"Topic '{topic}' logged successfully! ✅")
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def update_progress(user_id, subject, topic_name, progress_status, update_text, study_hours, session_count):
    """Updates study progress for a user."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Check if topic already exists for the user in this subject
        cursor.execute("""
            SELECT id FROM progress_tracking 
            WHERE user_id = %s AND subject = %s AND topic_name = %s
        """, (user_id, subject, topic_name))
        existing_topic = cursor.fetchone()

        if existing_topic:
            # Update existing record
            cursor.execute("""
                UPDATE progress_tracking
                SET progress_status = %s, update_text = %s, study_hours = study_hours + %s, session_count = session_count + %s
                WHERE id = %s
            """, (progress_status, update_text, study_hours, session_count, existing_topic[0]))
            st.success(f"Progress for topic '{topic_name}' updated successfully! ✅")
        else:
            # Insert new record if topic doesn't exist
            cursor.execute("""
                INSERT INTO progress_tracking 
                (user_id, subject, topic_name, progress_status, update_text, study_hours, session_count)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (user_id, subject, topic_name, progress_status, update_text, study_hours, session_count))
            st.success(f"New topic '{topic_name}' added and progress logged! ✅")
        conn.commit()
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()
            
def log_chat_message(user_id, subject, message):
    """Logs a new chat message."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chat (user_id, subject, message) VALUES (%s, %s, %s)", (user_id, subject, message))
        conn.commit()
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def log_reminder(user_id, subject, message, scheduled_time):
    """Logs a new reminder for the user."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reminders (user_id, subject, message, scheduled_time) 
            VALUES (%s, %s, %s, %s)
        """, (user_id, subject, message, scheduled_time))
        conn.commit()
        st.success(f"Reminder scheduled for {scheduled_time.strftime('%Y-%m-%d %H:%M')}! 🔔")
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def get_current_reminders(user_id, subject):
    """Fetches upcoming reminders for the user."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        current_time = datetime.now()
        cursor.execute("""
            SELECT message, scheduled_time, email_sent 
            FROM reminders 
            WHERE user_id = %s AND subject = %s AND scheduled_time > %s
            ORDER BY scheduled_time ASC
        """, (user_id, subject, current_time))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
        return []
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def update_email_sent_status(user_id, scheduled_time):
    """Updates the email_sent status to True for a specific reminder."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE reminders
            SET email_sent = TRUE
            WHERE user_id = %s AND scheduled_time = %s
        """, (user_id, scheduled_time))
        conn.commit()
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def get_all_topics_for_subject(subject):
    """Fetches all topics logged by all users for a given subject."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.id, u.name, GROUP_CONCAT(pt.topic_name SEPARATOR ', ') as topics
            FROM progress_tracking pt JOIN users u ON pt.user_id = u.id
            WHERE pt.subject = %s
            GROUP BY u.id, u.name
        """, (subject,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
        return []
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

# --- NEW Alert System Function with Email Logic ---
def check_for_due_reminders(user_id, subject):
    """
    Checks for reminders due within the next hour,
    displays an on-screen alert, and sends an email.
    """
    reminders = get_current_reminders(user_id, subject)
    now = datetime.now()
    user_email = st.session_state.user.get('email')
    user_name = st.session_state.user.get('name', 'User')

    for reminder in reminders:
        if now < reminder['scheduled_time'] < now + timedelta(hours=1):
            # Display on-screen alert
            st.markdown(f"""
                <div class="glass-container alert-glow">
                    <div class="stWarning">
                        <i class="fa-solid fa-bell"></i> <strong>Heads up! You have a reminder coming up soon:</strong>
                        <br>
                        <strong>{reminder['scheduled_time'].strftime('%I:%M %p')}:</strong> {reminder['message']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Send email only if it hasn't been sent before
            if not reminder['email_sent']:
                email_subject = "StudyCircle Reminder Alert!"
                email_body = f"""
                Hello {user_name},

                This is a friendly reminder from StudyCircle.

                Your study session reminder is coming up soon:

                Time: {reminder['scheduled_time'].strftime('%b %d, %I:%M %p')}
                Subject: {subject}
                Reminder: {reminder['message']}

                Keep up the great work!

                Best regards,
                The StudyCircle Team
                """
                send_email(user_email, email_subject, email_body)
                update_email_sent_status(user_id, reminder['scheduled_time'])


# --- Navigation Bar ---
def navigation():
    """Displays the main navigation bar."""
    if st.session_state.user:
        st.markdown("""
            <div class="navbar">
                <a href='?page=Dashboard'>Dashboard</a>
                <a href='?page=Logout'>Logout</a>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="navbar">
                <a href='?page=Home'>Home</a>
                <a href='?page=Login'>Login</a>
                <a href='?page=Register'>Register</a>
            </div>
        """, unsafe_allow_html=True)

# --- Home Page ---
def home_page():
    """Displays the home page content with a simple, attractive, and crazy feel."""
    if st.session_state.user:
        st.query_params["page"] = "Dashboard"
        st.rerun()

    # Hero Section - No Image
    st.markdown("""
        <div class="hero-section glass-container fade-in">
            <h1>StudyCircle</h1>
            <p>Your one-stop hub for collaborative learning and success.</p>
            <div style="margin-top: 30px;">
                <a href='?page=Register' style="text-decoration: none;">
                    <button class="stButton">Join the Circle</button>
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # About and Problem Statement Section
    st.markdown("<h2 class='home-section-title'>How We Make Learning Better</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="glass-container fade-in" style="height: 100%;">
                <h3 style="color: var(--primary-color);">What We Do</h3>
                <p>StudyCircle helps students connect and collaborate. We use smart tech to match you with peers, keep everyone in sync, and help you track your progress. It's a simple way to make group study more productive.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="glass-container fade-in" style="height: 100%;">
                <h3 style="color: var(--primary-color);">Why It Works</h3>
                <p>Studying with others can be tough when you're not on the same page. StudyCircle solves this by aligning your team's topics and goals. This means less confusion, more focus, and better results for everyone.</p>
            </div>
        """, unsafe_allow_html=True)

    # Core Features Section with Icons
    st.markdown("<h2 class='home-section-title'>Our Powerful Features</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-container fade-in">
            <div class="feature-grid">
                <div class="feature-card">
                    <div class="icon"><i class="fa-solid fa-lightbulb"></i></div>
                    <h4>Smart Matching</h4>
                    <p>Find study partners with similar topics and goals.</p>
                </div>
                <div class="feature-card">
                    <div class="icon"><i class="fa-solid fa-list-check"></i></div>
                    <h4>Topic Tracking</h4>
                    <p>Log and manage your study topics in real time.</p>
                </div>
                <div class="feature-card">
                    <div class="icon"><i class="fa-solid fa-chart-line"></i></div>
                    <h4>Progress Visualizer</h4>
                    <p>See your collective progress at a glance.</p>
                </div>
                <div class="feature-card">
                    <div class="icon"><i class="fa-solid fa-comments"></i></div>
                    <h4>Group Chat</h4>
                    <p>Communicate with your study group instantly.</p>
                </div>
                <div class="feature-card">
                    <div class="icon"><i class="fa-solid fa-calendar-check"></i></div>
                    <h4>Session Reminders</h4>
                    <p>Schedule alerts to keep your team on track.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- Dashboard Components ---
def show_study_progress(user, subject):
    """Displays the user's study progress metrics and charts."""
    st.markdown("""<div class="glass-container">""", unsafe_allow_html=True)
    conn = None # Initialize conn to None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT SUM(study_hours) FROM progress_tracking WHERE user_id = %s AND subject = %s", (user['id'], subject))
        total_hours = cursor.fetchone()[0] or 0

        cursor.execute("SELECT SUM(session_count) FROM progress_tracking WHERE user_id = %s AND subject = %s", (user['id'], subject))
        total_sessions = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(DISTINCT user_id) FROM chat WHERE subject = %s", (subject,))
        study_partners = cursor.fetchone()[0] or 0

    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
        total_hours, total_sessions, study_partners = 0, 0, 0
    finally:
        if conn and conn.is_connected():
            conn.close()

    st.markdown("### 📈 Study Progress Overview (Current Subject)")
    col1, col2, col3 = st.columns(3)
    col1.metric("Hours Studied", f"{int(total_hours)}")
    col2.metric("Sessions", f"{int(total_sessions)}")
    col3.metric("Study Partners", f"{int(study_partners)}")

    # Topic Progress
    st.markdown("### 🧠 Your Topics")
    with st.expander("View My Progress"):
        conn = None # Re-initialize conn for this block
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT topic_name, progress_status, SUM(study_hours) as hours, SUM(session_count) as sessions
                FROM progress_tracking
                WHERE user_id = %s AND subject = %s
                GROUP BY topic_name, progress_status
            """, (user['id'], subject))
            topics = cursor.fetchall()
        except mysql.connector.Error as err:
            st.error(f"Database error: {err}")
            topics = []
        finally:
            if conn and conn.is_connected():
                conn.close()

        if topics:
            for topic in topics:
                # Ensure status is one of the expected values before calculating progress
                progress_value = 0
                if topic['progress_status'] == 'In Progress':
                    progress_value = 50
                elif topic['progress_status'] == 'Completed':
                    progress_value = 100
                
                st.write(f"**{topic['topic_name']}**")
                st.progress(
                    progress_value / 100,
                    text=f"Status: {topic['progress_status']} | Hours: {topic['hours']:.1f} | Sessions: {int(topic['sessions'])}"
                )
        else:
            st.info("No topic progress found yet. Log a new topic below!")

    # Pie Chart
    st.markdown("### 🥧 Progress Distribution")
    conn = None # Re-initialize conn for this block
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT progress_status, COUNT(*) as count 
            FROM progress_tracking 
            WHERE user_id = %s AND subject = %s 
            GROUP BY progress_status
        """, (user['id'], subject))
        data = cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
        data = []
    finally:
        if conn and conn.is_connected():
            conn.close()

    if data:
        df = pd.DataFrame(data)
        fig = px.pie(
            df, 
            names='progress_status', 
            values='count', 
            title='Topic Progress Breakdown',
            color_discrete_sequence=px.colors.sequential.Tealgrn
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data for pie chart. Start logging your topics!")
    st.markdown("</div>", unsafe_allow_html=True)


def show_peer_matcher(user, subject):
    """Displays matched peers for the selected subject using simulated clustering."""
    st.markdown("""<div class="glass-container">""", unsafe_allow_html=True)
    st.markdown("### 🧑‍🤝‍🧑 Find Study Partners")
    
    all_topics = get_all_topics_for_subject(subject)
    
    if len(all_topics) > 1:
        # Prepare data for clustering
        df = pd.DataFrame(all_topics)
        
        # Use TF-IDF to vectorize the topics
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(df['topics'])
        
        # Determine number of clusters (a simple heuristic)
        k = min(len(df), 5) # Cap at 5 clusters for demo
        
        if k > 1:
            # Apply KMeans clustering
            kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto') # Use 'auto' for n_init
            df['cluster'] = kmeans.fit_predict(X)
            
            # Find the user's cluster
            user_cluster_row = df[df['id'] == user['id']]
            if not user_cluster_row.empty:
                user_cluster = user_cluster_row['cluster'].iloc[0]
                
                # Get peers in the same cluster (excluding the current user)
                peers = df[(df['cluster'] == user_cluster) & (df['id'] != user['id'])]
                
                if not peers.empty:
                    st.markdown(f"*Great news! We've found people with similar study goals in {subject}:*")
                    for index, row in peers.iterrows():
                        st.success(f"**{row['name']}** is studying: {row['topics']}")
                else:
                    st.info("No close matches yet within your current topics. Try logging more unique topics!")
            else:
                st.info("You haven't logged any topics yet to be matched. Start by adding a new topic!")

        else:
            st.info("Not enough diverse topics logged to form distinct groups. Keep adding your study goals!")
    else:
        st.info("Be the first to log a topic and start a study group!")
    st.markdown("</div>", unsafe_allow_html=True)


def show_sync_alert_system(user, subject):
    """Manages and displays sync reminders."""
    st.markdown("""<div class="glass-container">""", unsafe_allow_html=True)
    st.markdown("### ⏰ Sync Alert System")
    with st.expander("Schedule a new reminder"):
        reminder_message = st.text_area("What do you need a reminder for?")
        date_col, time_col = st.columns(2)
        with date_col:
            reminder_date = st.date_input("Date", min_value=datetime.now().date())
        with time_col:
            reminder_time = st.time_input("Time", value=(datetime.now() + timedelta(minutes=15)).time())
        
        if st.button("Schedule Reminder"):
            if reminder_message and reminder_date and reminder_time:
                scheduled_datetime = datetime.combine(reminder_date, reminder_time)
                if scheduled_datetime > datetime.now():
                    log_reminder(user['id'], subject, reminder_message, scheduled_datetime)
                    st.rerun()
                else:
                    st.error("Scheduled time must be in the future.")
            else:
                st.error("Please fill in all fields.")

    st.markdown("#### Your Upcoming Reminders")
    reminders = get_current_reminders(user['id'], subject)
    if reminders:
        for reminder in reminders:
            st.info(f"{reminder['scheduled_time'].strftime('%b %d, %I:%M %p')}: {reminder['message']}")
    else:
        st.markdown("No upcoming reminders scheduled.")
    st.markdown("</div>", unsafe_allow_html=True)


def show_topic_input_and_progress_log(user, subject):
    """Provides UI for logging topics and updating progress."""
    st.markdown("""<div class="glass-container">""", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ➕ Log New Topic")
        topic = st.text_input("New Topic Name", key="new_topic_input")
        if st.button("Log Topic", key="log_topic_btn"):
            if topic.strip():
                log_new_topic(user['id'], subject, topic)
                st.rerun()
            else:
                st.error("Topic name cannot be empty.")
    
    with col2:
        st.markdown("### 📚 Update Study Progress")
        
        # Fetch existing topics for the user in the selected subject
        conn = None
        existing_topics_list = []
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT DISTINCT topic_name FROM progress_tracking 
                WHERE user_id = %s AND subject = %s
                ORDER BY topic_name
            """, (user['id'], subject))
            existing_topics_list = [row['topic_name'] for row in cursor.fetchall()]
        except mysql.connector.Error as err:
            st.error(f"Database error fetching topics: {err}")
        finally:
            if conn and conn.is_connected():
                conn.close()

        selected_topic_to_update = st.selectbox(
            "Select Topic to Update (or type new)", 
            options=[""] + existing_topics_list, 
            key="update_topic_select"
        )
        
        topic_name_input = st.text_input("Or type new topic name", value=selected_topic_to_update, key="update_topic_input_manual")
        
        progress_status = st.selectbox("Status", ['Not Started', 'In Progress', 'Completed'], key="progress_status")
        study_hours = st.number_input("Hours Studied (add to total)", min_value=0.0, format="%.1f", key="study_hours")
        session_count = st.number_input("Sessions Attended (add to total)", min_value=0, step=1, key="session_count")
        
        if st.button("Submit Progress", key="submit_progress_btn"):
            final_topic_name = topic_name_input.strip()
            if final_topic_name:
                update_progress(user['id'], subject, final_topic_name, progress_status, "", study_hours, session_count)
                st.rerun()
            else:
                st.error("Please select or enter a topic name.")
    st.markdown("</div>", unsafe_allow_html=True)
    
def show_weekly_report(user):
    """Displays a weekly performance report as a bar chart."""
    st.markdown("""<div class="glass-container">""", unsafe_allow_html=True)
    st.markdown("### 📊 Weekly Performance Report")
    
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        # Fetch data for the last 7 days
        seven_days_ago = datetime.now() - timedelta(days=7)
        cursor.execute("""
            SELECT SUM(study_hours) as daily_hours, DATE(timestamp) as study_date
            FROM progress_tracking
            WHERE user_id = %s AND timestamp >= %s
            GROUP BY study_date
            ORDER BY study_date
        """, (user['id'], seven_days_ago))
        
        data = cursor.fetchall()
        
    except mysql.connector.Error as err:
        st.error(f"Database error fetching weekly report: {err}")
        data = []
    finally:
        if conn and conn.is_connected():
            conn.close()

    if data:
        df = pd.DataFrame(data)
        df['study_date'] = pd.to_datetime(df['study_date'])
        # Ensure all days of the last week are present, even with 0 hours
        date_range = pd.date_range(seven_days_ago.date(), periods=7, freq='D')
        full_df = pd.DataFrame({'study_date': date_range})
        full_df = pd.merge(full_df, df, on='study_date', how='left').fillna(0)
        full_df['day_of_week'] = full_df['study_date'].dt.day_name()
        
        fig = px.bar(
            full_df,
            x='day_of_week',
            y='daily_hours',
            title='Study Hours This Week',
            labels={'day_of_week': 'Day of the Week', 'daily_hours': 'Hours Studied'},
            color_discrete_sequence=[px.colors.qualitative.Plotly[0]]
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No study data available for the last week.")
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_dashboard(user):
    """Main dashboard combining all modules."""
    
    # NEW: Display user info at the top
    st.title(f"Welcome, {user['name']} 👋")
    st.markdown(f"*Email:* {user['email']}")
    
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get overall subjects logged in
        cursor.execute("SELECT COUNT(DISTINCT subject) FROM progress_tracking WHERE user_id = %s", (user['id'],))
        subjects_logged = cursor.fetchone()[0] or 0
        
        # Get whole time spent on sessions
        cursor.execute("SELECT SUM(study_hours) FROM progress_tracking WHERE user_id = %s", (user['id'],))
        total_study_hours_overall = cursor.fetchone()[0] or 0
        
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
        subjects_logged = 0
        total_study_hours_overall = 0
    finally:
        if conn and conn.is_connected():
            conn.close()
            
    st.markdown(f"*Overall Subjects Logged:* {subjects_logged}")
    st.markdown(f"*Total Study Hours (All Subjects):* {total_study_hours_overall:.1f} hours")
    
    st.markdown("---")
    
    subjects = get_subjects()
    if not subjects:
        st.warning("No subjects available. Please contact admin to add subjects.")
        return

    # 1. Subjects Selection (Top of the page)
    selected_subject = st.selectbox("Select Subject", subjects, key="subject_selectbox")
    
    # NEW: Check for and display alerts at the top of the dashboard
    check_for_due_reminders(user['id'], selected_subject)

    # 2. Peer Matcher
    show_peer_matcher(user, selected_subject)

    # 3. Sync Alert System
    st.markdown("""<div class="fade-in">""", unsafe_allow_html=True)
    show_sync_alert_system(user, selected_subject)
    st.markdown("</div>", unsafe_allow_html=True)

    # 4. Log New Topic and Update Progress (in one container)
    show_topic_input_and_progress_log(user, selected_subject)
    
    # 5. Study Progress and Progress Distribution (in one container)
    st.markdown("""<div class="fade-in">""", unsafe_allow_html=True)
    show_study_progress(user, selected_subject)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 6. Weekly Report
    st.markdown("""<div class="fade-in">""", unsafe_allow_html=True)
    show_weekly_report(user)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 7. Group Chat (at the bottom)
    st.markdown("---")
    st.markdown("### 💬 Group Chat")
    chat_col, button_col = st.columns([4, 1])
    with chat_col:
        message = st.text_input("Your Message", key="chat_message_input", label_visibility="collapsed")
    with button_col:
        st.markdown("<br>", unsafe_allow_html=True) # Add a line break for alignment
        if st.button("Send", key="send_chat_btn"):
            if message.strip():
                log_chat_message(user['id'], selected_subject, message)
                st.rerun()
            else:
                st.error("Message cannot be empty.")
    
    show_chat(selected_subject)
    
# --- App Entry Point ---
def main():
    """Main function to run the Streamlit app."""
    
    # Initialize session state variables at the top of the main function.
    if "user" not in st.session_state:
        st.session_state.user = None
    if "page" not in st.query_params:
        st.query_params["page"] = "Home"

    apply_custom_css()
    navigation()

    page = st.query_params["page"]

    if page == "Home":
        home_page()
            
    elif page == "Dashboard":
        if st.session_state.user:
            show_dashboard(st.session_state.user)
        else:
            st.warning("Please log in to view the dashboard.")
            st.query_params["page"] = "Login"
            st.rerun()

    elif page == "Login":
        if st.session_state.user:
            st.success("You are already logged in!")
            st.query_params["page"] = "Dashboard"
            st.rerun()
        else:
            st.subheader("🔐 Login to Your Account")
            with st.form("login_form"):
                email = st.text_input("Email", key="login_email_form")
                password = st.text_input("Password", type="password", key="login_password_form")
                submitted = st.form_submit_button("Login")
                if submitted:
                    user = authenticate_user(email, password)
                    if user:
                        st.session_state.user = user
                        st.success("Login successful!")
                        st.query_params["page"] = "Dashboard"
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")
            
    elif page == "Register":
        st.subheader("📝 Register New Account")
        with st.form("register_form"):
            name = st.text_input("Name", key="register_name_form")
            email = st.text_input("Email", key="register_email_form")
            password = st.text_input("Password", type="password", key="register_password_form")
            submitted = st.form_submit_button("Register")
            if submitted:
                if name and email and password:
                    register_user(name, email, password)
                    st.success("✅ Registration complete! Please log in.")
                    st.query_params["page"] = "Login"
                    st.rerun()
                else:
                    st.error("All fields are required.")
            
    elif page == "Logout":
        if st.session_state.user:
            st.session_state.user = None
            st.success("Logged out successfully.")
        st.query_params["page"] = "Home"
        st.rerun()

if __name__ == '__main__':
    main()