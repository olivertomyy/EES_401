import streamlit as st
import random
import json
import os
import tempfile
import io
import pickle
import time

# Constants for session persistence
SESSION_FILE = "exam_session.pkl"

def save_session_state():
    """Save critical session state to file for persistence"""
    try:
        session_data = {
            'questions': st.session_state.get('questions', []),
            'current_question': st.session_state.get('current_question', 0),
            'score': st.session_state.get('score', 0),
            'answered': st.session_state.get('answered', False),
            'user_answers': st.session_state.get('user_answers', []),
            'exam_completed': st.session_state.get('exam_completed', False),
            'topics': st.session_state.get('topics', {}),
            'questions_loaded': st.session_state.get('questions_loaded', False),
            'last_uploaded_file_name': st.session_state.get('last_uploaded_file_name', None),
            'session_timestamp': time.time()
        }
        
        with open(SESSION_FILE, 'wb') as f:
            pickle.dump(session_data, f)
    except Exception as e:
        print(f"Warning: Could not save session: {e}")

def load_session_state():
    """Load session state from file if it exists and is recent"""
    try:
        if os.path.exists(SESSION_FILE):
            # Check if session file is recent (less than 24 hours old)
            file_age = time.time() - os.path.getmtime(SESSION_FILE)
            if file_age < 24 * 3600:  # 24 hours
                with open(SESSION_FILE, 'rb') as f:
                    session_data = pickle.load(f)
                return session_data
    except Exception as e:
        print(f"Warning: Could not load session: {e}")
    return None

def load_questions_from_json():
    """Load questions from JSON file with the programming_languages_exam_questions structure"""
    try:
        # Try to load from local file first
        if os.path.exists("programming_questions.json"):
            with open("programming_questions.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
                questions = extract_questions_from_data(data)
                if questions:
                    st.success(f"✅ Loaded {len(questions)} exam questions from local file")
                    return questions
        
        # If local file doesn't exist, use fallback questions
        st.info("📝 Using built-in exam questions")
        return get_fallback_exam_questions()
        
    except Exception as e:
        st.error(f"❌ Error loading questions: {e}")
        return get_fallback_exam_questions()

def extract_questions_from_data(data):
    """Extract questions from JSON data structure"""
    # If data is already a list of questions
    if isinstance(data, list) and len(data) > 0:
        if validate_question_structure(data[0]):
            return data
    
    # Look for questions in common keys
    possible_keys = [
        "programming_languages_exam_questions",
        "chemistry_questions",
        "questions",
        "quiz_questions",
        "exam_questions",
        "question_bank",
        "items"
    ]
    
    for key in possible_keys:
        if key in data and isinstance(data[key], list) and len(data[key]) > 0:
            questions = data[key]
            if validate_question_structure(questions[0]):
                return questions
    
    # If no standard key found, look for any list with question structure
    for key, value in data.items():
        if isinstance(value, list) and len(value) > 0:
            if validate_question_structure(value[0]):
                return value
    
    return None

def validate_question_structure(question):
    """Validate that the question has the required structure"""
    if not isinstance(question, dict):
        return False
    
    required_fields = ['question', 'options', 'correct_answer']
    return all(field in question for field in required_fields)

def get_fallback_exam_questions():
    """Provide comprehensive fallback exam questions"""
    return [
        {
"questions": [
{
"id": 1,
"topic": "Work Readiness",
"question": "What is the main reason that having a degree alone is no longer enough to stand out in the job market?",
"options": {
"A": "Most companies no longer hire based on qualifications",
"B": "Jobs that previously didn't require degrees are now being filled by graduates",
"C": "Degrees have become less valuable academically",
"D": "Employers prefer people without formal education"
},
"correct_answer": "B",
"explanation": "The PDF explains that many roles that historically didn't require degrees (e.g., clerks, managers) are now filled by graduates, so a degree alone no longer differentiates candidates."
},
{
"id": 2,
"topic": "Work Readiness",
"question": "Work readiness is BEST defined as:",
"options": {
"A": "Mastery of technical job skills",
"B": "Having a university degree and job experience",
"C": "The skills, aptitudes, and attitudes needed for workplace culture and demands",
"D": "Being ready to start a business"
},
"correct_answer": "C",
"explanation": "The document defines work readiness as the combination of skills, aptitudes, and attitudes employers expect, not solely technical qualifications."
},
{
"id": 3,
"topic": "Work Readiness",
"question": "Which of the following is NOT part of work readiness skills?",
"options": {
"A": "World-of-work awareness",
"B": "Career planning and decision making",
"C": "High-level coding ability",
"D": "Job search techniques"
},
"correct_answer": "C",
"explanation": "Work readiness emphasizes transferable and career-preparation skills; specific technical abilities like advanced coding are hard skills, not core work readiness components as listed."
},
{
"id": 4,
"topic": "Self Awareness",
"question": "What does self-awareness primarily help you do in your career?",
"options": {
"A": "Hide your weaknesses from employers",
"B": "Understand your strengths and weaknesses to grow",
"C": "Avoid difficult jobs",
"D": "Perform only technical tasks"
},
"correct_answer": "B",
"explanation": "The text stresses self-awareness allows you to identify strengths to leverage and weaknesses to improve, aiding career development."
},
{
"id": 5,
"topic": "Self Awareness",
"question": "Why do employers value candidates with self-awareness?",
"options": {
"A": "They expect candidates to be flawless",
"B": "Self-awareness makes you admit you have no weaknesses",
"C": "It enables you to identify, improve, and use strengths effectively",
"D": "It guarantees you never make mistakes"
},
"correct_answer": "C",
"explanation": "Employers like candidates who understand their capabilities and areas to develop because such candidates can grow and adapt."
},
{
"id": 6,
"topic": "Branding Yourself",
"question": "Personal branding helps you:",
"options": {
"A": "Convince employers you are perfect",
"B": "Communicate your selling points and stand out",
"C": "Focus only on your academic achievements",
"D": "Avoid competition"
},
"correct_answer": "B",
"explanation": "The PDF notes that personal branding communicates who you are and your selling points, helping employers see your fit."
},
{
"id": 7,
"topic": "Branding Yourself",
"question": "Which of the following is TRUE about personal branding?",
"options": {
"A": "It is only useful for people in business",
"B": "It makes it easier for employers to determine your suitability",
"C": "It makes you appear arrogant",
"D": "It should hide your weaknesses"
},
"correct_answer": "B",
"explanation": "The document explains a strong personal brand helps employers quickly assess suitability for roles."
},
{
"id": 8,
"topic": "Soft Skills",
"question": "Which of the following is considered a soft skill?",
"options": {
"A": "Mechanical engineering",
"B": "HTML/CSS",
"C": "Teamwork",
"D": "Data analysis"
},
"correct_answer": "C",
"explanation": "Soft skills are interpersonal and character traits; teamwork is a classic soft skill listed in the PDF."
},
{
"id": 9,
"topic": "Soft Skills",
"question": "Why are soft skills important to employers?",
"options": {
"A": "They are easier to teach than technical skills",
"B": "They define personality and work behavior",
"C": "They can replace academic qualifications",
"D": "They guarantee promotions"
},
"correct_answer": "B",
"explanation": "The PDF highlights that soft skills shape how you work with others and are crucial selection criteria alongside qualifications."
},
{
"id": 10,
"topic": "Problem Solving",
"question": "What does the 'I' in the IDEAL problem-solving framework stand for?",
"options": {
"A": "Interpret",
"B": "Identify",
"C": "Initiate",
"D": "Implement"
},
"correct_answer": "B",
"explanation": "IDEAL stands for Identify, Define, Explore, Act, and Look back — the PDF lists 'Identify' as the first step."
},
{
"id": 11,
"topic": "Problem Solving",
"question": "Problem-solving requires a combination of:",
"options": {
"A": "Teamwork alone",
"B": "Reasoning, logic, creativity, and calmness",
"C": "Academic grades and qualifications",
"D": "Physical strength and speed"
},
"correct_answer": "B",
"explanation": "The text emphasizes that reasoning, creative thinking, and composure are needed for effective problem solving."
},
{
"id": 12,
"topic": "Job Search Techniques",
"question": "Why is applying online alone not the most effective job search strategy?",
"options": {
"A": "Most applicants do not use the internet",
"B": "Online applications have less than 3% chance of leading to an interview",
"C": "Companies no longer post jobs online",
"D": "Recruiters prefer paper applications"
},
"correct_answer": "B",
"explanation": "The PDF notes that online-only approaches yield poor interview rates; active networking and referrals improve outcomes."
},
{
"id": 13,
"topic": "Job Search Techniques",
"question": "According to research, job seekers are five times more likely to be hired through:",
"options": {
"A": "Cold emails",
"B": "Online applications",
"C": "Referrals",
"D": "Random job boards"
},
"correct_answer": "C",
"explanation": "The guide cites studies showing referrals significantly increase hiring chances."
},
{
"id": 14,
"topic": "Recruiters",
"question": "Which statement is TRUE about external recruiters?",
"options": {
"A": "They work for job seekers",
"B": "They work for employers",
"C": "They guarantee job placement",
"D": "They only recruit interns"
},
"correct_answer": "B",
"explanation": "The PDF clarifies recruiters represent employers and aim to find the best candidates for roles."
},
{
"id": 15,
"topic": "CV Writing",
"question": "What is the full meaning of CV?",
"options": {
"A": "Career Version",
"B": "Curriculum Vitae",
"C": "Candidate Value",
"D": "Career Verification"
},
"correct_answer": "B",
"explanation": "CV stands for Curriculum Vitae, Latin for 'course of life,' as stated in the text."
},
{
"id": 16,
"topic": "CV Writing",
"question": "Which of the following should NOT be added to a CV?",
"options": {
"A": "Professional title",
"B": "Relevant work experience",
"C": "A detailed list of all your life events",
"D": "Education history"
},
"correct_answer": "C",
"explanation": "The guide advises brevity and relevance, discouraging exhaustive life histories on a CV."
},
{
"id": 17,
"topic": "CV Formatting",
"question": "Which font is recommended for CV writing?",
"options": {
"A": "Comic Sans",
"B": "Arial or Times New Roman",
"C": "Brush Script",
"D": "Stencil"
},
"correct_answer": "B",
"explanation": "The PDF lists standard, legible fonts such as Arial and Times New Roman as good choices for CVs."
},
{
"id": 18,
"topic": "CV Writing",
"question": "Why should graphics be minimized on a CV?",
"options": {
"A": "Recruiters prefer fully decorated CVs",
"B": "Graphics may make the CV hard to print and read",
"C": "Graphics improve professionalism",
"D": "Graphics make the CV shorter"
},
"correct_answer": "B",
"explanation": "Excessive graphics can hurt readability and printability; the PDF advises white space for clarity."
},
{
"id": 19,
"topic": "Interview Skills",
"question": "What is the main purpose of an interview?",
"options": {
"A": "To impress the employer with big words",
"B": "To determine whether both the job and candidate are a good fit",
"C": "To test your memory",
"D": "To negotiate salary immediately"
},
"correct_answer": "B",
"explanation": "The document describes interviews as two-way conversations to assess fit for both parties."
},
{
"id": 20,
"topic": "Interview Skills",
"question": "Employers decide whether to hire a candidate in approximately:",
"options": {
"A": "30 minutes",
"B": "1 hour",
"C": "5 minutes",
"D": "24 hours"
},
"correct_answer": "C",
"explanation": "The PDF mentions research suggesting interviewers form impressions in roughly five minutes."
},
{
"id": 21,
"topic": "Interview Skills",
"question": "Which of the following is a key competency employers want?",
"options": {
"A": "Ability to gossip",
"B": "Critical thinking",
"C": "Perfect handwriting",
"D": "Ability to work without supervision"
},
"correct_answer": "B",
"explanation": "Critical thinking is listed among the seven key competencies necessary for workplace success."
},
{
"id": 22,
"topic": "Public Speaking",
"question": "Public speaking is described as:",
"options": {
"A": "Speaking only during debates",
"B": "An act and art of speaking before an audience",
"C": "Speaking only to large crowds",
"D": "Talking casually to friends"
},
"correct_answer": "B",
"explanation": "The guide defines public speaking as both an act and an art of speaking before an audience."
},
{
"id": 23,
"topic": "Public Speaking",
"question": "Which is NOT one of the five steps of eloquent speech preparation?",
"options": {
"A": "Invention",
"B": "Memory",
"C": "Delivery",
"D": "Decoration"
},
"correct_answer": "D",
"explanation": "The five steps are Invention, Arrangement, Style, Memory, and Delivery; 'Decoration' is not listed."
},
{
"id": 24,
"topic": "Presentation Skills",
"question": "Which of the following is recommended to calm nerves before presenting?",
"options": {
"A": "Speaking as fast as possible",
"B": "Deep breathing",
"C": "Avoiding water",
"D": "Memorizing every exact word"
},
"correct_answer": "B",
"explanation": "The PDF recommends deep breathing to counteract adrenaline and steady the voice."
},
{
"id": 25,
"topic": "Presentation Skills",
"question": "What is the purpose of using cue cards in a presentation?",
"options": {
"A": "To read your speech word-for-word",
"B": "To trigger your mind about what comes next",
"C": "To entertain the audience",
"D": "To avoid making eye contact"
},
"correct_answer": "B",
"explanation": "Cue cards are advised so you have prompts to keep the flow without sounding memorized or robotic."
},
{
"id": 26,
"topic": "Advanced Work Readiness",
"question": "A recent graduate wants to demonstrate work readiness beyond academic credentials. Which action best shows proactive career control?",
"options": {
"A": "Waiting for job postings to appear",
"B": "Relying solely on online applications",
"C": "Creating a targeted networking plan and informational interviews",
"D": "Applying to every job regardless of fit"
},
"correct_answer": "C",
"explanation": "The PDF emphasizes being proactive—networking and informational interviews provide insight and uncover hidden opportunities."
},
{
"id": 27,
"topic": "Networking Strategy",
"question": "You have limited connections. According to the guide, what's the highest-value first step to leverage networking?",
"options": {
"A": "Mass messaging strangers on LinkedIn",
"B": "Reconnecting with former managers and colleagues for referrals",
"C": "Posting frequent random updates on social media",
"D": "Only attending in-person conferences"
},
"correct_answer": "B",
"explanation": "The text recommends reconnecting with known contacts (managers, colleagues) and asking for referrals as a top strategy."
},
{
"id": 28,
"topic": "LinkedIn Optimization",
"question": "Which change to a LinkedIn profile most directly improves discovery by recruiters?",
"options": {
"A": "Add a long list of hobbies in the About section",
"B": "Use a compelling headline that specifies the roles you seek",
"C": "Hide your work experience",
"D": "Only list education"
},
"correct_answer": "B",
"explanation": "The guide advises customizing your headline to indicate role types, which helps recruiters find you."
},
{
"id": 29,
"topic": "Referral Ethics",
"question": "A friend offers to refer you but asks you to exaggerate your role at a past employer. What's the best response?",
"options": {
"A": "Agree to exaggerate to secure the role",
"B": "Decline the referral to avoid dishonesty",
"C": "Ask your friend to refer you honestly and offer to provide accurate examples",
"D": "Edit your CV to remove the employer entirely"
},
"correct_answer": "C",
"explanation": "The PDF stresses honesty on CVs; ask for a legitimate referral and provide truthful accomplishments."
},
{
"id": 30,
"topic": "Targeted Applications",
"question": "When tailoring your CV for a role, which approach is MOST consistent with the guide's advice?",
"options": {
"A": "Use the same generic CV for all applications",
"B": "Highlight measurable achievements that mirror the job description",
"C": "Include every duty from every past job",
"D": "List only soft skills"
},
"correct_answer": "B",
"explanation": "The guide recommends focusing on measurable, relevant achievements and tailoring to the job's requirements."
},
{
"id": 31,
"topic": "CV Structure Analysis",
"question": "Which CV section is described as the best place to 'introduce yourself' and summarize your achievements?",
"options": {
"A": "Education",
"B": "Personal profile / summary",
"C": "Work experience",
"D": "Hobbies"
},
"correct_answer": "B",
"explanation": "The personal profile or summary at the top of the CV introduces you and highlights key achievements concisely, per the PDF."
},
{
"id": 32,
"topic": "CV Formatting Standards",
"question": "Which formatting choice would most likely reduce readability according to the guide?",
"options": {
"A": "One-inch margins",
"B": "Consistent date format",
"C": "Multiple fonts and heavy graphics",
"D": "Single spacing with clear headings"
},
"correct_answer": "C",
"explanation": "The document warns against gimmicky graphics and inconsistent formatting that hurt readability."
},
{
"id": 33,
"topic": "Work Experience Writing",
"question": "Which work-experience bullet best follows the guide's recommendation?",
"options": {
"A": "Responsible for customer service",
"B": "Managed customer service team",
"C": "Led a 5-person customer service team, improving response time by 30%",
"D": "Worked with customers daily"
},
"correct_answer": "C",
"explanation": "The PDF promotes measurable achievements phrased with action verbs rather than vague duty listings."
},
{
"id": 34,
"topic": "Hard vs Soft Skills",
"question": "A candidate for a marketing role lacks technical analytics tools skills but excels in communication. According to the guide, what should the candidate emphasize?",
"options": {
"A": "Only hard skills",
"B": "Soft skills and ability to learn technical tools quickly",
"C": "Omit all weaknesses from the CV",
"D": "Claim expertise in analytics"
},
"correct_answer": "B",
"explanation": "The guide says soft skills (like communication) are valuable and one can be trained in technical skills; emphasize strengths and learning ability."
},
{
"id": 35,
"topic": "CV Extras",
"question": "Which 'additional section' on a CV could most effectively demonstrate industry engagement?",
"options": {
"A": "Hobbies",
"B": "Conferences attended and professional affiliations",
"C": "Favorite movies",
"D": "High school clubs"
},
"correct_answer": "B",
"explanation": "The PDF suggests sections like conferences and affiliations highlight ongoing industry involvement and learning."
},
{
"id": 36,
"topic": "Interview Preparation",
"question": "Which preparation step directly addresses the interviewer's expectation that you understand the company?",
"options": {
"A": "Memorize a generic elevator pitch",
"B": "Research the company's website, news, and values",
"C": "Prepare only salary negotiation points",
"D": "Bring an extra CV copy"
},
"correct_answer": "B",
"explanation": "The guide stresses knowing the employer (researching company info) so you can demonstrate genuine interest and fit."
},
{
"id": 37,
"topic": "Interview Behavior",
"question": "During an in-person interview, which nonverbal behavior is LEAST likely to make a good first impression?",
"options": {
"A": "Firm handshake and eye contact",
"B": "Warm smile and good posture",
"C": "Slouching and lack of eye contact",
"D": "Polite greeting"
},
"correct_answer": "C",
"explanation": "The PDF notes first impressions rely on posture, eye contact and a firm handshake; slouching undermines this."
},
{
"id": 38,
"topic": "Interview Responses",
"question": "When asked 'What is your greatest weakness?', the best answer per the guide should:",
"options": {
"A": "Deny having any weaknesses",
"B": "Name a weakness and explain steps you are taking to improve it",
"C": "Accuse previous employers of unfairness",
"D": "Refuse to answer"
},
"correct_answer": "B",
"explanation": "The PDF recommends acknowledging a real area for improvement and describing how you're addressing it."
},
{
"id": 39,
"topic": "Interview Types",
"question": "Which interview type is described as having more back-and-forth conversation and requires several prepared talking points?",
"options": {
"A": "Traditional interview",
"B": "Conversational interview",
"C": "Phone screening",
"D": "Panel interview"
},
"correct_answer": "B",
"explanation": "The document notes conversational interviews are more interactive and you should prepare key points to discuss."
},
{
"id": 40,
"topic": "Phone & Virtual Interviews",
"question": "Which tip is most important specifically for virtual interviews according to the PDF?",
"options": {
"A": "Wear casual clothes",
"B": "Know how to use the conferencing software and test your setup",
"C": "Don't worry about background noise",
"D": "Use a low-resolution camera"
},
"correct_answer": "B",
"explanation": "Virtual interviews require technical preparation—testing audio/video and the software to avoid disruptions."
},
{
"id": 41,
"topic": "Follow-up Etiquette",
"question": "Which follow-up action is recommended within 24 hours after an interview?",
"options": {
"A": "Send a tailored thank-you email to each interviewer",
"B": "Post about the interview on social media",
"C": "Call the CEO demanding a decision",
"D": "Send multiple identical messages to HR"
},
"correct_answer": "A",
"explanation": "The PDF advises a well-written thank-you note within 24 hours as professional courtesy demonstrating interest."
},
{
"id": 42,
"topic": "Behavioral Interviewing",
"question": "Using the STAR/CAR method, what does the 'R' stand for and why is it important?",
"options": {
"A": "Review; to remind the interviewer of the question",
"B": "Result; to show the outcomes and impact of your actions",
"C": "Research; to show you researched the company",
"D": "Repeat; to repeat the question"
},
"correct_answer": "B",
"explanation": "Result (or Result/Outcome) shows the measurable impact of your action—critical to convincing interviewers of your effectiveness."
},
{
"id": 43,
"topic": "Difficult Interview Scenarios",
"question": "If an interviewer presses for a skill you lack, the guide suggests you should:",
"options": {
"A": "Lie about having the skill",
"B": "Admit the gap and highlight how you would learn or compensate",
"C": "Change the topic",
"D": "Remain silent"
},
"correct_answer": "B",
"explanation": "Honesty plus demonstrating a plan to learn or an alternative strength is the recommended approach in the document."
},
{
"id": 44,
"topic": "Presentation Design",
"question": "Which presentation tip aligns with the cognitive load advice given in the PDF?",
"options": {
"A": "Use dense slides packed with text",
"B": "Keep slides simple and avoid reading them verbatim",
"C": "Use multiple fonts and flashy animations",
"D": "Include full paragraphs on each slide"
},
"correct_answer": "B",
"explanation": "The PDF recommends simplicity, mindful cognitive load, and not reading slides word-for-word to keep audiences engaged."
},
{
"id": 45,
"topic": "Public Speaking Myths",
"question": "Which statement reflects the PDF's stance on public speaking ability?",
"options": {
"A": "Great public speaking is purely an inborn talent",
"B": "Fear of public speaking is always negative",
"C": "Public speaking skills can be developed; fear can be managed",
"D": "Only extroverts can become good speakers"
},
"correct_answer": "C",
"explanation": "The guide debunks the myths that speaking is only innate and that fear is wholly negative, encouraging practice and techniques to improve."
},
{
"id": 46,
"topic": "Audience Engagement",
"question": "Which tactic best increases audience engagement during a presentation?",
"options": {
"A": "Use long monologues without pauses",
"B": "Ask targeted questions and invite participation",
"C": "Avoid eye contact to reduce nervousness",
"D": "Read slides exactly as written"
},
"correct_answer": "B",
"explanation": "The PDF recommends engaging the audience through questions and participation to keep interest and create rapport."
},
{
"id": 47,
"topic": "Nervousness Techniques",
"question": "Which physiological technique helps control adrenaline-related presentation symptoms?",
"options": {
"A": "Rapid shallow breaths",
"B": "Deep controlled breathing",
"C": "Holding your breath",
"D": "Drinking caffeine immediately before speaking"
},
"correct_answer": "B",
"explanation": "Deep breathing counteracts adrenaline effects and stabilizes voice and calmness, per the guide."
},
{
"id": 48,
"topic": "Presentation Structure",
"question": "Which structural approach prevents sounding robotic if you forget your lines?",
"options": {
"A": "Memorizing every word",
"B": "Using key phrase cue cards and a clear structure",
"C": "Not preparing at all",
"D": "Reading slides verbatim"
},
"correct_answer": "B",
"explanation": "The PDF advises structuring presentations with cues and key phrases rather than strict memorization to stay natural."
},
{
"id": 49,
"topic": "Interview Evaluation Criteria",
"question": "Which interviewer goal is emphasized as most important when assessing a candidate?",
"options": {
"A": "Assessing the candidate's color preferences",
"B": "Determining whether the candidate has the necessary skills and fits team personality",
"C": "Testing social media following",
"D": "Finding someone who will quit soon"
},
"correct_answer": "B",
"explanation": "The PDF notes interviewers want to know both capability and cultural/team fit to ensure longevity and performance."
},
{
"id": 50,
"topic": "Job Market Strategy",
"question": "Which approach does the guide label as the 'back door' to increase interview chances?",
"options": {
"A": "Spamming recruiters",
"B": "Finding and contacting a hiring manager or recruiter directly",
"C": "Only using public job boards",
"D": "Waiting for postings to appear"
},
"correct_answer": "B",
"explanation": "The 'back door' refers to direct, human connections—contacting hiring managers/recruiters to boost visibility."
},
{
"id": 51,
"topic": "Recruiter Relations",
"question": "When building relationships with recruiters, which expectation should you keep in mind?",
"options": {
"A": "Recruiters work for you and will find any job you want",
"B": "Recruiters are independent and may only have opportunities that fit their clients' needs",
"C": "Recruiters always place candidates for free",
"D": "Recruiters guarantee interviews"
},
"correct_answer": "B",
"explanation": "The PDF makes clear recruiters work for employers and place candidates when roles match, not as a service to job-seekers."
},
{
"id": 52,
"topic": "Targeting Companies",
"question": "The guide advocates a proactive strategy targeting specific companies. Which action is part of this approach?",
"options": {
"A": "Sending a generic CV to HR",
"B": "Using LinkedIn to find the department head and requesting a conversation",
"C": "Applying randomly to roles",
"D": "Posting irrelevant content"
},
"correct_answer": "B",
"explanation": "The suggested proactive approach is finding decision-makers and requesting conversations rather than generic applications."
},
{
"id": 53,
"topic": "Networking Follow-up",
"question": "After a networking conversation, what follow-up is most likely to maintain the relationship?",
"options": {
"A": "Never contacting them again",
"B": "Sending a thank-you message and offering help or resources",
"C": "Immediately asking for a job",
"D": "Posting about them without consent"
},
"correct_answer": "B",
"explanation": "The guide recommends nurturing relationships—thank-you messages and reciprocal value help sustain connections."
},
{
"id": 54,
"topic": "Job Search Metrics",
"question": "Which is a realistic expectation cited by the guide when relying solely on online applications?",
"options": {
"A": "You will receive offers within a week",
"B": "Less than 3% chance of getting an interview",
"C": "You'll be preferred over referrals",
"D": "It guarantees a career change"
},
"correct_answer": "B",
"explanation": "The text notes that online-only applications typically yield very low interview rates—often under 3%."
},
{
"id": 55,
"topic": "CV Honesty",
"question": "What is the serious risk mentioned if you falsify academic grades on your CV?",
"options": {
"A": "You might not get the job",
"B": "It can be considered degree fraud with legal consequences",
"C": "No one will notice",
"D": "It improves your credibility"
},
"correct_answer": "B",
"explanation": "The PDF warns that falsifying qualifications can lead to charges like degree fraud and severe consequences."
},
{
"id": 56,
"topic": "CV Contact Info",
"question": "Which contact detail is advised to include on a CV?",
"options": {
"A": "Professional email and LinkedIn profile",
"B": "Every past address you've ever had",
"C": "Personal social media with unprofessional content",
"D": "Your parent's phone number only"
},
"correct_answer": "A",
"explanation": "The guide recommends including clear professional contact info like email and LinkedIn for recruiters to reach you."
},
{
"id": 57,
"topic": "Personal Profile",
"question": "When should a candidate use a CV objective instead of a CV summary?",
"options": {
"A": "When the candidate is a seasoned professional",
"B": "When the candidate has little relevant work experience",
"C": "For all CVs regardless of experience",
"D": "When the candidate wants to omit achievements"
},
"correct_answer": "B",
"explanation": "The PDF states objectives suit those with limited experience; summaries fit experienced candidates highlighting achievements."
},
{
"id": 58,
"topic": "Action Verbs",
"question": "Which verb usage best follows the guide's recommendation for CV language?",
"options": {
"A": "Responsible for preparing reports",
"B": "Prepared monthly financial reports that reduced closing time by 20%",
"C": "Was involved in team reporting",
"D": "Did many reporting tasks"
},
"correct_answer": "B",
"explanation": "Using strong action verbs with measurable results is favored over vague responsibility statements."
},
{
"id": 59,
"topic": "Interview First Impressions",
"question": "Which practice is recommended to ensure you arrive prepared at an interview?",
"options": {
"A": "Arrive exactly at the start time",
"B": "Arrive about 10 minutes early",
"C": "Arrive late to make an entrance",
"D": "Only log on to a virtual interview at the scheduled time"
},
"correct_answer": "B",
"explanation": "The guide recommends arriving 10 minutes early to gather thoughts and avoid stress from late arrival."
},
{
"id": 60,
"topic": "Behavioral Examples",
"question": "Which response exemplifies the STAR method for a leadership question?",
"options": {
"A": "I am a leader; I do great work",
"B": "When our project stalled (S), I organized a team meeting (T), delegated tasks and set milestones (A), and we completed on time with a 10% efficiency gain (R)",
"C": "I like leading teams",
"D": "I once led a team"
},
"correct_answer": "B",
"explanation": "An effective STAR answer outlines Situation, Task, Action, and Result with concrete outcomes."
},
{
"id": 61,
"topic": "Presentation Visuals",
"question": "Which slide design choice directly follows the PDF's 'use effective imagery' rule?",
"options": {
"A": "Use low-quality clip art everywhere",
"B": "Include a single high-impact, relevant image per key slide",
"C": "Avoid images entirely",
"D": "Fill slide with background pattern and text"
},
"correct_answer": "B",
"explanation": "The guide recommends effective, relevant imagery that supports rather than distracts from the message."
},
{
"id": 62,
"topic": "Public Speaking Delivery",
"question": "Which delivery habit weakens credibility according to the guide?",
"options": {
"A": "Maintaining steady eye contact",
"B": "Using filler words excessively (e.g., 'um', 'like')",
"C": "Varying vocal tone",
"D": "Using purposeful hand gestures"
},
"correct_answer": "B",
"explanation": "Excessive filler words undermine perceived confidence; the text advises practicing to minimize them."
},
{
"id": 63,
"topic": "Interview Questions: 'Tell me about yourself'",
"question": "What is the recommended length and focus for answering 'Tell me about yourself'?",
"options": {
"A": "10 minutes of life history",
"B": "30 seconds to 2 minutes focusing on recent roles, achievements and goals",
"C": "A one-word answer",
"D": "Only discuss personal hobbies"
},
"correct_answer": "B",
"explanation": "The guide advises a concise 30-second to 2-minute overview linking experience, achievements and goals relevant to the job."
},
{
"id": 64,
"topic": "Interview Questions: 'Why us?'",
"question": "Which element makes an effective answer to 'Why do you want to work for our company?'",
"options": {
"A": "Generic praise about the company",
"B": "Specific examples from company research and how you can contribute",
"C": "Discuss salary expectations immediately",
"D": "Say you had no other options"
},
"correct_answer": "B",
"explanation": "Employers look for evidence of company research and clear connection between your skills and their needs."
},
{
"id": 65,
"topic": "Interview Red Flags",
"question": "Which interview behavior is a red flag for employers?",
"options": {
"A": "Talking negatively about all previous employers",
"B": "Explaining a constructive learning from a past challenge",
"C": "Asking thoughtful questions at the end",
"D": "Being punctual"
},
"correct_answer": "A",
"explanation": "Speaking poorly of previous employers is unprofessional and signals potential attitude problems to hiring teams."
},
{
"id": 66,
"topic": "Information Sessions",
"question": "What is the key advantage of attending information sessions as a new graduate?",
"options": {
"A": "They are evaluative tests",
"B": "They provide networking opportunities and company insight in a non-evaluative setting",
"C": "You always get hired on the spot",
"D": "They replace the need for interviews"
},
"correct_answer": "B",
"explanation": "The PDF notes information sessions let you build rapport and learn about companies without formal evaluation."
},
{
"id": 67,
"topic": "Industry Conferences",
"question": "Which behavior at an industry conference most aligns with the guide's networking advice?",
"options": {
"A": "Collect business cards without following up",
"B": "Engage in meaningful conversations and follow up afterwards",
"C": "Attend only social events with no professional purpose",
"D": "Skip sessions and only eat snacks"
},
"correct_answer": "B",
"explanation": "Meaningful engagement followed by follow-up fosters relationships—an emphasized strategy in the document."
},
{
"id": 68,
"topic": "Professional Organizations",
"question": "Joining professional organizations helps you primarily by:",
"options": {
"A": "Guaranteeing a job",
"B": "Providing networking, knowledge and career advancement opportunities",
"C": "Replacing the need for a CV",
"D": "Eliminating the need to interview"
},
"correct_answer": "B",
"explanation": "The guide recommends joining professional bodies to gain connections, insights, and career growth."
},
{
"id": 69,
"topic": "References",
"question": "Which practice is recommended regarding references before applying for jobs?",
"options": {
"A": "List random contacts without notice",
"B": "Contact referees in advance, update contact info, and brief them on your job search",
"C": "Never provide references",
"D": "Use fictional referees to improve chances"
},
"correct_answer": "B",
"explanation": "The PDF advises preparing and informing references so they can provide timely and relevant support."
},
{
"id": 70,
"topic": "Presentation Tips",
"question": "Which of the 'Ten Tips' specifically warns against reading from slides?",
"options": {
"A": "Keep it simple",
"B": "Do not read your slides",
"C": "Use effective imagery",
"D": "Use black slides"
},
"correct_answer": "B",
"explanation": "One of the listed tips is explicitly 'Do not read your slides', emphasizing natural delivery and audience engagement."
},
{
"id": 71,
"topic": "Hard Interview Scenario",
"question": "You are asked in an interview to explain a project failure. What's the best way to respond?",
"options": {
"A": "Blame teammates and avoid responsibility",
"B": "Use STAR: describe the situation, your role, actions you took, and lessons learned with resulting improvement",
"C": "Say you never fail",
"D": "Refuse to answer"
},
"correct_answer": "B",
"explanation": "The guide recommends acknowledging challenges and focusing on actions taken and lessons learned to show growth."
},
{
"id": 72,
"topic": "CV Online Safety",
"question": "What safety advice does the guide give about posting your CV online?",
"options": {
"A": "Always publish your home address",
"B": "Avoid including home address to reduce fraud risk while keeping contact methods safe",
"C": "Include every personal detail for transparency",
"D": "Share your CV on all public forums"
},
"correct_answer": "B",
"explanation": "The text cautions against posting home addresses publicly to prevent targeting by fraudsters."
},
{
"id": 73,
"topic": "Assessing Job Fit",
"question": "When evaluating if a job is right for you, which factor is LEAST relevant according to the guide?",
"options": {
"A": "Company culture and mission",
"B": "Role responsibilities and growth prospects",
"C": "Immediate office snack options",
"D": "Location, salary, and lifestyle priorities"
},
"correct_answer": "C",
"explanation": "While perks can matter, the guide highlights core factors like culture, responsibilities, and lifestyle alignment as more important."
},
{
"id": 74,
"topic": "Interview Closing",
"question": "Which final action during an interview demonstrates interest and professionalism?",
"options": {
"A": "Ask no questions and leave immediately",
"B": "Ask thoughtful questions about role expectations and next steps",
"C": "Demand a salary decision on the spot",
"D": "Critique the company policies"
},
"correct_answer": "B",
"explanation": "The guide recommends coming prepared with 3–6 questions to show interest and gather role information."
},
{
"id": 75,
"topic": "Public Speaking Practice",
"question": "Which rehearsal technique does the guide emphasize to improve presentations?",
"options": {
"A": "Rehearse in front of a small audience and record yourself for feedback",
"B": "Never practice to stay spontaneous",
"C": "Only read slides to practice",
"D": "Avoid feedback at all costs"
},
"correct_answer": "A",
"explanation": "Practicing in front of others and reviewing recordings helps identify improvements and build confidence, per the PDF."
},
{
"id": 76,
"topic": "Presentation Time Management",
"question": "What is a practical way to structure a talk when time is limited?",
"options": {
"A": "Cover every possible detail",
"B": "Select the most pertinent points and leave room for questions",
"C": "Speak as fast as possible to fit more content",
"D": "Read a transcript in full"
},
"correct_answer": "B",
"explanation": "The guide advises focusing on key points to keep talks concise and engaging when time is limited."
},
{
"id": 77,
"topic": "Interview Follow-up Strategy",
"question": "If you haven't heard back two weeks after an interview, what's the recommended next step?",
"options": {
"A": "Send a polite follow-up email reiterating interest and asking for any updates",
"B": "Flood their inbox with multiple messages",
"C": "Assume rejection and never follow up",
"D": "Show up at the office unannounced"
},
"correct_answer": "A",
"explanation": "The PDF suggests polite and timely follow-up inquiries to maintain engagement without being pushy."
},
{
"id": 78,
"topic": "Professional Image",
"question": "Which clothing choice aligns best with the guide's example of professional interview attire?",
"options": {
"A": "Casual shorts and flip-flops",
"B": "Neat slacks, a dress or suit, and closed-toe shoes",
"C": "Party wear",
"D": "Gym clothes"
},
"correct_answer": "B",
"explanation": "Appropriate, neat, and professional clothing (slacks, dress, suit, closed-toe shoes) is recommended for interviews in the guide."
},
{
"id": 79,
"topic": "Handling Tough Questions",
"question": "If asked an unfamiliar technical question, the guide recommends you should:",
"options": {
"A": "Make up an answer",
"B": "Ask clarifying questions, think briefly, and outline how you'd approach the problem",
"C": "Say you don't know and leave it at that",
"D": "Refuse to answer"
},
"correct_answer": "B",
"explanation": "Clarifying, thinking, and explaining a problem-solving approach shows competence and honesty, per the PDF."
},
{
"id": 80,
"topic": "Informational Interviews",
"question": "What is the primary purpose of an informational interview according to the guide?",
"options": {
"A": "To get a job offer immediately",
"B": "To learn about day-to-day responsibilities and industry insights while building relationships",
"C": "To request unpaid work",
"D": "To test interview questions"
},
"correct_answer": "B",
"explanation": "Informational interviews are exploratory meetings to gain understanding and connections, not immediate hiring evaluations."
},
{
"id": 81,
"topic": "CV Tailoring Exercise (Hard)",
"question": "Given a job requiring 'project delivery and stakeholder communication', which CV bullet best demonstrates fit?",
"options": {
"A": "Handled several projects",
"B": "Led cross-functional project delivery for a product launch, coordinating five stakeholders and delivering on time",
"C": "Worked with stakeholders occasionally",
"D": "Interested in project management"
},
"correct_answer": "B",
"explanation": "This bullet uses measurable detail and explicitly mentions coordination and delivery—directly mapping to the job requirement."
},
{
"id": 82,
"topic": "Ethical Considerations",
"question": "If you discover a recruiter has posted inaccurate information about you online, the best course of action is to:",
"options": {
"A": "Ignore it",
"B": "Politely request correction and provide accurate documentation if needed",
"C": "Publicly shame the recruiter",
"D": "Retaliate by posting false information about them"
},
"correct_answer": "B",
"explanation": "The guide implies professionalism; resolving inaccuracies calmly and with evidence preserves reputation and relationships."
},
{
"id": 83,
"topic": "Advanced Networking",
"question": "Which strategy most effectively uncovers hidden job opportunities per the PDF?",
"options": {
"A": "Rely solely on job boards",
"B": "Invest time in building and nurturing relationships with people in your industry",
"C": "Only attend social events without purpose",
"D": "Post resumes randomly in forums"
},
"correct_answer": "B",
"explanation": "The PDF repeatedly emphasizes networking and nurturing relationships as the top approach to finding hidden jobs."
},
{
"id": 84,
"topic": "CV Length and Relevance",
"question": "For most professional roles, the guide suggests the optimal CV length is:",
"options": {
"A": "10+ pages covering all life events",
"B": "Brief and relevant—concentrate on recent and pertinent achievements (typically 1–2 pages)",
"C": "One line",
"D": "A novel-length autobiography"
},
"correct_answer": "B",
"explanation": "The PDF recommends concise CVs focused on relevant recent accomplishments, avoiding excessive detail."
},
{
"id": 85,
"topic": "Presentation Accessibility",
"question": "Which accessibility practice enhances a presentation for diverse audiences?",
"options": {
"A": "Use tiny fonts and verbose slides",
"B": "Choose readable fonts, adequate spacing, and clear visual contrast",
"C": "Rely on color alone to convey meaning",
"D": "Include no slide titles"
},
"correct_answer": "B",
"explanation": "Readable fonts, spacing and contrast align with the guide's advice for clear, audience-friendly slides."
},
{
"id": 86,
"topic": "Interview Role-Play (Hard)",
"question": "If asked to prioritize tasks with conflicting deadlines, which approach best demonstrates professional judgment?",
"options": {
"A": "Do tasks in random order",
"B": "Assess impact and urgency, communicate with stakeholders, and set realistic timelines",
"C": "Ignore stakeholders and work alone",
"D": "Complain about workload"
},
"correct_answer": "B",
"explanation": "The guide highlights communication, prioritization by impact, and stakeholder alignment as markers of professional capability."
},
{
"id": 87,
"topic": "Presentation Evaluation",
"question": "After delivering a presentation, which action yields the most improvement according to the PDF?",
"options": {
"A": "Never review performance",
"B": "Watch a recording, seek feedback, and iterate on weak areas",
"C": "Assume it was perfect",
"D": "Only change slides without changing delivery"
},
"correct_answer": "B",
"explanation": "Recording your talk and obtaining feedback are recommended steps for continuous improvement."
},
{
"id": 88,
"topic": "Interview Negotiation",
"question": "Which timing for discussing salary is recommended in the guide?",
"options": {
"A": "Immediately at the start of the first interview",
"B": "After you have demonstrated fit and when an offer or clear next-stage discussion arises",
"C": "Demand it during the greeting",
"D": "Never discuss salary"
},
"correct_answer": "B",
"explanation": "The guide suggests focusing first on fit and value; compensation talks are best after mutual interest is established."
},
{
"id": 89,
"topic": "Public Speaking Recovery",
"question": "If you lose your train of thought during a presentation, the guide suggests you should:",
"options": {
"A": "Apologize profusely and stop",
"B": "Use a cue phrase, pause, take a breath, and continue from your key point",
"C": "Leave the stage",
"D": "Read a different presenter's notes"
},
"correct_answer": "B",
"explanation": "Pausing and using cues prevents panic and maintains professionalism when recovering from a lapse."
},
{
"id": 90,
"topic": "CV Personal Branding",
"question": "Which short statement best functions as a strong 'About' section on LinkedIn per the guide?",
"options": {
"A": "I like many things",
"B": "Product manager with 6 years' experience launching B2B SaaS; I specialize in cross-functional leadership and data-driven roadmaps that increased retention by 18%",
"C": "Looking for work",
"D": "Contact me"
},
"correct_answer": "B",
"explanation": "A concise, first-person summary with role, experience, specialization, and measurable outcomes fits the guide's recommendations."
},
{
"id": 91,
"topic": "Advanced CV Bullet Crafting",
"question": "Which CV bullet demonstrates both scope and outcome most effectively?",
"options": {
"A": "Worked on marketing campaigns",
"B": "Led a digital campaign across three channels reaching 1M users and increasing lead conversion by 12%",
"C": "Was part of a team",
"D": "Helped with social media"
},
"correct_answer": "B",
"explanation": "This bullet includes scope (three channels, 1M users) and a concrete outcome (12% conversion uplift)."
},
{
"id": 92,
"topic": "Networking Prioritization",
"question": "Given limited time, which networking activity yields the highest return per the guide?",
"options": {
"A": "Mass-emailing strangers",
"B": "Scheduling one meaningful conversation per week with a targeted contact",
"C": "Posting memes daily",
"D": "Attending every possible event without follow-up"
},
"correct_answer": "B",
"explanation": "The guide recommends regular, focused conversations over low-value mass outreach to build real relationships."
},
{
"id": 93,
"topic": "Interview Assessment",
"question": "How should you handle a question about a salary gap or employment gap according to the guide?",
"options": {
"A": "Lie about being employed",
"B": "Be honest, explain productive activities during the gap and what you learned",
"C": "Refuse to discuss",
"D": "Blame the economy without detail"
},
"correct_answer": "B",
"explanation": "Honesty combined with framing the gap as a time of development or productive activity is recommended."
},
{
"id": 94,
"topic": "Presentation Slide Best Practice",
"question": "Which slide practice most aligns with the 'black slides' tip?",
"options": {
"A": "Always show slides with dense text",
"B": "Include occasional blank or black slides to re-focus attention on the speaker",
"C": "Never change slides",
"D": "Use black slides as filler"
},
"correct_answer": "B",
"explanation": "The 'black slides' tip suggests using blank/black slides strategically to emphasize spoken content and maintain focus."
},
{
"id": 95,
"topic": "Interview Preparation Drill (Hard)",
"question": "When preparing examples for behavioral interviews, which approach yields the strongest set of responses?",
"options": {
"A": "Memorize unrelated stories",
"B": "Prepare 6–8 STAR examples tailored to common competencies and practice concise delivery",
"C": "Only prepare one example for all questions",
"D": "Rely on improvisation"
},
"correct_answer": "B",
"explanation": "Having multiple STAR examples for key competencies allows adaptable, evidence-based responses during interviews."
},
{
"id": 96,
"topic": "Career Mindset",
"question": "The guide urges job seekers to adopt which mindset during their search?",
"options": {
"A": "Passive wait-for-opportunity",
"B": "Active consultant approach: understand employer problems and present yourself as the remedy",
"C": "Only focus on salary",
"D": "Avoid learning about industry trends"
},
"correct_answer": "B",
"explanation": "It suggests showing employers you understand their needs and positioning yourself as the solution, not just a candidate."
},
{
"id": 97,
"topic": "Public Speaking Style",
"question": "Which stylistic recommendation improves clarity and impact in presentations?",
"options": {
"A": "Use technical jargon without explanation",
"B": "Use clear structure, plain language and rhetorical techniques to emphasize points",
"C": "Speak in monotone",
"D": "Avoid storytelling"
},
"correct_answer": "B",
"explanation": "The guide encourages stylistic choices like clear structure and rhetorical techniques to make arguments persuasive and accessible."
},
{
"id": 98,
"topic": "Advanced Problem Solving",
"question": "In the IDEAL framework's 'Explore possible solutions' step, which action is most consistent with best practice?",
"options": {
"A": "Choose the first idea that comes to mind",
"B": "Generate multiple alternatives, assess risks and benefits, and select the most viable",
"C": "Avoid brainstorming",
"D": "Pick the cheapest solution regardless of fit"
},
"correct_answer": "B",
"explanation": "The 'Explore' phase involves generating and evaluating multiple options to find a robust solution."
},
{
"id": 99,
"topic": "CV Red Flags (Hard)",
"question": "Which CV entry is most likely to trigger further verification by employers?",
"options": {
"A": "Detailed accomplishments with measurable outcomes",
"B": "An unverifiable claim of a degree from a non-existent institution",
"C": "A short, accurate job description",
"D": "Clear dates of employment"
},
"correct_answer": "B",
"explanation": "False or unverifiable academic claims are high-risk and prompt checks; the guide warns against falsification."
},
{
"id": 100,
"topic": "Presentation Audience Analysis",
"question": "Which pre-presentation action best helps tailor content to audience needs?",
"options": {
"A": "Assume everyone knows the topic",
"B": "Ask about audience background and expectations beforehand",
"C": "Prepare generic material only",
"D": "Ignore agenda constraints"
},
"correct_answer": "B",
"explanation": "Knowing the audience helps you select appropriate depth and examples; the guide recommends pre-event audience analysis."
},
{
"id": 101,
"topic": "Interview Strategy (Hard)",
"question": "You are interviewing for a role that emphasizes adaptability. Which example best demonstrates adaptability?",
"options": {
"A": "I never change my approach",
"B": "Led a project pivot when market signals changed, re-prioritised tasks and delivered features that matched new customer needs",
"C": "I prefer static environments",
"D": "I avoid ambiguous tasks"
},
"correct_answer": "B",
"explanation": "An example showing pivoting, re-prioritization and successful delivery aligns well with adaptability."
},
{
"id": 102,
"topic": "CV Proofreading",
"question": "Which step most reduces the chance of spelling/grammar errors on your CV?",
"options": {
"A": "Rely only on spellcheck",
"B": "Use spellcheck and have at least one other person review the CV",
"C": "Ignore errors; they are unimportant",
"D": "Use unconventional fonts to hide errors"
},
"correct_answer": "B",
"explanation": "The guide recommends both automated tools and human proofreading to catch errors and improve clarity."
},
{
"id": 103,
"topic": "Advanced Networking Tactic",
"question": "How should you approach a senior executive when you have no prior connection?",
"options": {
"A": "Send a long unsolicited resume",
"B": "Research their work, craft a concise message showing mutual value, and request a short exploratory conversation",
"C": "Demand a job immediately",
"D": "Ignore personalization"
},
"correct_answer": "B",
"explanation": "The guide advises research, personalization, and a consultative ask to build rapport with senior contacts."
},
{
"id": 104,
"topic": "Presentation Rehearsal (Hard)",
"question": "Which rehearsal method is most effective for improving timing and pausing?",
"options": {
"A": "Speak only in your head",
"B": "Record full runs and time each section, practicing strategic pauses and transitions",
"C": "Read the script silently",
"D": "Avoid timing practice to stay natural"
},
"correct_answer": "B",
"explanation": "Recording and timing helps refine pacing and purposeful pausing for emphasis as advised in the guide."
},
{
"id": 105,
"topic": "Interview Assessment (Hard)",
"question": "An interviewer asks for evidence of leadership under resource constraints. Which answer is strongest?",
"options": {
"A": "I would handle it if it happens",
"B": "During a hiring freeze, I reallocated existing staff, automated reporting to cut manual hours by 25%, and maintained project delivery",
"C": "I avoid leading in constrained situations",
"D": "I wait for resources to appear"
},
"correct_answer": "B",
"explanation": "Concrete actions and measurable outcomes under constraints demonstrate credible leadership experience."
},
{
"id": 106,
"topic": "CV Keyword Strategy",
"question": "To improve ATS (Applicant Tracking System) match rates, what should you do?",
"options": {
"A": "Use images instead of text",
"B": "Mirror key words and phrases from the job description in your CV where they truthfully apply",
"C": "Hide keywords in white text",
"D": "Use complex PDF layouts that ATS cannot read"
},
"correct_answer": "B",
"explanation": "The guide suggests aligning language with job descriptions (truthfully) to improve discoverability by ATS."
},
{
"id": 107,
"topic": "Presentation Q&A Handling",
"question": "When faced with a hostile question during Q&A, the best tactic is to:",
"options": {
"A": "Argue aggressively",
"B": "Stay calm, acknowledge the concern, and respond concisely with facts or offer to discuss offline",
"C": "Ignore the question",
"D": "Walk out"
},
"correct_answer": "B",
"explanation": "Remaining composed and constructive preserves credibility and often defuses hostility as advised in the guide."
},
{
"id": 108,
"topic": "Career Planning",
"question": "Which activity is LEAST helpful when planning a long-term career path?",
"options": {
"A": "Clarifying values and goals",
"B": "Tracking industry trends and skill demands",
"C": "Building a plan to acquire needed skills",
"D": "Randomly changing jobs without reflection"
},
"correct_answer": "D",
"explanation": "Strategic planning, not haphazard job changes, aligns with the document's career decision advice."
},
{
"id": 109,
"topic": "Negotiation Preparation",
"question": "Before salary negotiation, the guide suggests you should:",
"options": {
"A": "Know your market value and prepare clear examples of your impact",
"B": "Demand double without justification",
"C": "Avoid discussing accomplishments",
"D": "Accept the first offer immediately"
},
"correct_answer": "A",
"explanation": "Knowing market rates and demonstrating your value with examples positions you for stronger negotiation outcomes."
},
{
"id": 110,
"topic": "Presentation Accessibility (Hard)",
"question": "If your audience includes non-native speakers, which adjustment is most appropriate?",
"options": {
"A": "Use dense idiomatic language",
"B": "Use clear, simple language and allow slightly slower pacing",
"C": "Speed up to fit more content",
"D": "Avoid summarizing key points"
},
"correct_answer": "B",
"explanation": "Simpler language and slightly slower delivery improve comprehension for audiences with varied language proficiency."
},
{
"id": 111,
"topic": "Job Search Diversification",
"question": "Which combination best reflects a diversified job search strategy recommended by the guide?",
"options": {
"A": "Apply online only",
"B": "Network, ask for referrals, target companies directly, use recruiters and apply online selectively",
"C": "Only attend job fairs",
"D": "Post your CV on one board and wait"
},
"correct_answer": "B",
"explanation": "The guide recommends multiple channels—networking, referrals, targeted outreach, agency recruiters and selective online applications."
},
{
"id": 112,
"topic": "Interview Body Language",
"question": "Which body-language behavior increases perceived confidence?",
"options": {
"A": "Slouched posture",
"B": "Crossed arms and minimal eye contact",
"C": "Open posture, upright sitting, and measured gestures",
"D": "Avoiding hand movement entirely"
},
"correct_answer": "C",
"explanation": "Open posture, good eye contact and controlled gestures communicate confidence, as the guide outlines."
},
{
"id": 113,
"topic": "Professional Development",
"question": "Which action best demonstrates commitment to continuous professional development?",
"options": {
"A": "Never learning new tools",
"B": "Attending relevant courses/conferences and seeking certifications",
"C": "Relying only on past education",
"D": "Avoiding feedback"
},
"correct_answer": "B",
"explanation": "The guide encourages ongoing learning through training, conferences and certifications to stay competitive."
},
{
"id": 114,
"topic": "Presentation Technology",
"question": "Which technology practice can undermine a virtual presentation?",
"options": {
"A": "Testing audio/video in advance",
"B": "Using poor lighting and ignoring microphone checks",
"C": "Sharing slides in an accessible format",
"D": "Muting background noise"
},
"correct_answer": "B",
"explanation": "Poor AV setup distracts and reduces professionalism; pre-checks are recommended."
},
{
"id": 115,
"topic": "Career Story (Hard)",
"question": "Which approach frames your career narrative most persuasively for an interview?",
"options": {
"A": "Listing jobs with no context",
"B": "Telling a concise story linking experiences, key accomplishments, skills developed and future goals aligned to the role",
"C": "Talking only about personal hobbies",
"D": "Reciting your resume verbatim"
},
"correct_answer": "B",
"explanation": "A coherent narrative that connects past achievements with future goals shows purposeful career direction as the PDF advises."
},
{
"id": 116,
"topic": "Presentation Feedback",
"question": "Which type of feedback is most valuable for improving presentation effectiveness?",
"options": {
"A": "Generic praise with no specifics",
"B": "Actionable feedback on structure, delivery, and audience engagement with examples",
"C": "Harsh criticism without guidance",
"D": "No feedback at all"
},
"correct_answer": "B",
"explanation": "Actionable, specific feedback helps you iterate and improve; the guide supports structured review."
},
{
"id": 117,
"topic": "Interview Preparation Checklist",
"question": "Which item is LEAST relevant on a pre-interview checklist?",
"options": {
"A": "Research company and role",
"B": "Prepare STAR examples",
"C": "Plan travel and arrive early",
"D": "Memorize exact sentences to recite word-for-word"
},
"correct_answer": "D",
"explanation": "Memorizing verbatim can sound robotic and fail if you forget; structured practice and prompts are preferred."
},
{
"id": 118,
"topic": "CV Digital Presence",
"question": "Which online practice strengthens professional credibility per the guide?",
"options": {
"A": "Leaving LinkedIn incomplete",
"B": "Maintaining a polished LinkedIn with achievements, endorsements, and an updated profile",
"C": "Posting personal controversies",
"D": "Deleting all online presence"
},
"correct_answer": "B",
"explanation": "A compelling LinkedIn profile supports personal branding and discoverability as recommended in the PDF."
},
{
"id": 119,
"topic": "Presentation Persuasion",
"question": "Which rhetorical technique increases persuasive power in presentations?",
"options": {
"A": "Overloading slides with data",
"B": "Using clear structure, stories and evidence to support claims",
"C": "Using confusing analogies",
"D": "Delivering without examples"
},
"correct_answer": "B",
"explanation": "Stories and evidence framed within a clear structure make arguments memorable and persuasive, per the guide."
},
{
"id": 120,
"topic": "Long-term Career Planning (Hard)",
"question": "When planning a career pivot, which sequence aligns with the guide's advice?",
"options": {
"A": "Apply randomly until hired",
"B": "Assess transferable skills, research target industry, acquire key skills, network into roles and present your story",
"C": "Quit immediately and hope for the best",
"D": "Rely solely on online applications"
},
"correct_answer": "B",
"explanation": "A structured pivot involves skill mapping, targeted research, learning and relationship-building—advice echoed throughout the PDF."
},
{
"id": 121,
"topic": "Interview Reflection",
"question": "After a difficult interview, what reflection practice best prepares you for improvement?",
"options": {
"A": "Forget about it and move on",
"B": "List questions you struggled with, identify gaps in examples or knowledge, and create a plan to address them",
"C": "Blame the interviewer",
"D": "Panic and avoid future interviews"
},
"correct_answer": "B",
"explanation": "Reflecting on weaknesses and planning remedial actions aligns with the guide's emphasis on practice and preparation."
},
{
"id": 122,
"topic": "Career Opportunity Sourcing",
"question": "Which approach uncovers leadership-level roles according to the guide?",
"options": {
"A": "Only apply to junior roles",
"B": "Engage executive recruiters, build relationships with decision-makers, and demonstrate strategic impact",
"C": "Use generic job alerts",
"D": "Focus solely on entry-level networking"
},
"correct_answer": "B",
"explanation": "For senior roles, executive recruiters and direct engagement with decision-makers are key strategies discussed in the PDF."
},
{
"id": 123,
"topic": "Public Speaking Confidence",
"question": "Which mental technique helps reduce presentation anxiety mentioned in the guide?",
"options": {
"A": "Visualize a hostile audience",
"B": "Use affirmations and visualization of a positive audience reaction",
"C": "Avoid preparation to keep spontaneity",
"D": "Rely on caffeine"
},
"correct_answer": "B",
"explanation": "Visualization and positive affirmations are recommended to mentally prepare and reduce nerves before speaking."
},
{
"id": 124,
"topic": "Effective Thank-You Notes",
"question": "What should a post-interview thank-you email ideally contain?",
"options": {
"A": "A generic 'thanks' with no specifics",
"B": "A brief appreciation, one or two points reinforcing your fit and any follow-up information promised",
"C": "A demand for feedback",
"D": "A copy of your CV attached again"
},
"correct_answer": "B",
"explanation": "The guide advises personalized thank-you notes that reinforce fit and provide any requested follow-up details."
},
{
"id": 125,
"topic": "Mastery Synthesis (Hard)",
"question": "Which combined strategy best positions a graduate to outperform peers in a competitive job market?",
"options": {
"A": "Rely on a high GPA alone",
"B": "Develop transferable soft skills, craft measurable achievements on the CV, proactively network/referrals, and practice interview/presentation competencies",
"C": "Only post resumes on many boards",
"D": "Wait passively for recruiters to find you"
},
"correct_answer": "B",
"explanation": "The PDF's central thesis: combine soft-skill development, clear evidence of impact, proactive networking, and practiced interviewing/presentation to stand out."
}
]
}
    ]

def analyze_exam_topics(questions):
    """Analyze and categorize exam questions by topic"""
    topics = {}
    for q in questions:
        topic = q.get('topic', 'General')
        topics[topic] = topics.get(topic, 0) + 1
    return topics

def initialize_exam_state(questions=None, restore_progress=False):
    """Initialize or reset the exam state"""
    if questions is None:
        questions = load_questions_from_json()
    
    if restore_progress and st.session_state.get('questions_loaded', False):
        # Keep existing progress
        st.info("🔄 Restored your exam progress")
    else:
        # Reset progress
        st.session_state.questions = questions
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.user_answers = [None] * len(questions)
        st.session_state.exam_completed = False
        st.session_state.topics = analyze_exam_topics(questions)
        st.session_state.questions_loaded = True
    
    # Save session after initialization
    save_session_state()

def parse_uploaded_json(uploaded_file):
    """Parse uploaded JSON file and extract questions"""
    try:
        # Read the file content
        content = uploaded_file.read()
        
        # Try to decode as JSON
        try:
            data = json.loads(content.decode('utf-8'))
        except UnicodeDecodeError:
            # If UTF-8 fails, try other encodings
            try:
                data = json.loads(content.decode('latin-1'))
            except:
                st.error("❌ Could not decode the file. Please use UTF-8 encoding.")
                return None
        
        # Extract questions from the data
        questions = extract_questions_from_data(data)
        
        if questions:
            st.success(f"✅ Successfully loaded {len(questions)} questions!")
            return questions
        else:
            st.error("❌ No valid questions found in the uploaded file. Please check the format.")
            return None
        
    except json.JSONDecodeError as e:
        st.error(f"❌ Invalid JSON format: {e}")
        return None
    except Exception as e:
        st.error(f"❌ Error parsing JSON file: {e}")
        return None

def save_uploaded_file(uploaded_file):
    """Save uploaded file locally"""
    try:
        with open("programming_questions.json", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("✅ File saved successfully!")
        return True
    except Exception as e:
        st.error(f"❌ Error saving file: {e}")
        return False

def main():
    # Set page configuration
    st.set_page_config(
        page_title="EXAM QUESTIONS",
        page_icon="💻",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Try to load existing session first
    if 'questions_loaded' not in st.session_state:
        saved_session = load_session_state()
        if saved_session:
            # Restore from saved session
            for key, value in saved_session.items():
                st.session_state[key] = value
            st.success("🔁 Restored your previous exam session!")
        else:
            # Initialize fresh session
            initialize_exam_state()
    
    # Header
    st.title("💻 Exam - Persistent Session")
    st.markdown("### Your progress is automatically saved! Leave and return anytime.")
    
    # Auto-save notice
    st.info("💾 **Auto-save enabled**: Your progress is automatically saved and will be restored when you return.")
    
    # File Upload Section
    with st.expander("📁 Upload Your JSON Question File", expanded=False):
        st.markdown("""
        **Upload your JSON file with questions in this format:**
        ```json
        {
          "programming_languages_exam_questions": [
            {
              "id": 1,
              "topic": "Your Topic",
              "question": "Your question?",
              "options": {
                "A": "Option A",
                "B": "Option B",
                "C": "Option C",
                "D": "Option D"
              },
              "correct_answer": "A",
              "explanation": "Your explanation here"
            }
          ]
        }
        ```
        """)
        
        uploaded_file = st.file_uploader(
            "Choose a JSON file", 
            type="json",
            help="Upload your questions in JSON format",
            key="file_uploader"
        )
        
        # AUTO-LOAD when file is uploaded
        if uploaded_file is not None:
            # Parse the uploaded file
            questions = parse_uploaded_json(uploaded_file)
            
            if questions:
                # Store file info for persistence
                st.session_state.last_uploaded_file_name = uploaded_file.name
                
                # Initialize with new questions but preserve progress if compatible
                current_questions = st.session_state.get('questions', [])
                if len(current_questions) == len(questions):
                    st.info("📚 Questions updated while preserving your progress!")
                    st.session_state.questions = questions
                else:
                    st.warning("🔄 Question set changed - resetting progress")
                    initialize_exam_state(questions)
                
                save_session_state()
                st.rerun()
        
        # Manual controls for uploaded file
        if uploaded_file is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔄 Reload Uploaded Questions", type="primary"):
                    uploaded_file.seek(0)  # Reset file pointer
                    questions = parse_uploaded_json(uploaded_file)
                    if questions:
                        initialize_exam_state(questions)
                        st.success(f"✅ Reloaded {len(questions)} questions!")
                        st.rerun()
            
            with col2:
                if st.button("💾 Save File Locally"):
                    if save_uploaded_file(uploaded_file):
                        st.info("File saved as 'programming_questions.json'. It will be loaded automatically next time.")
    
    # Quick JSON Input Section
    with st.expander("📝 Or Paste JSON Directly", expanded=False):
        json_text = st.text_area(
            "Paste your JSON here:",
            height=200,
            placeholder='Paste your JSON questions here...',
            key="json_text_area"
        )
        
        if st.button("📥 Load from Text", type="secondary"):
            if json_text.strip():
                try:
                    # Create a temporary file-like object
                    fake_file = io.BytesIO(json_text.encode('utf-8'))
                    fake_file.name = "pasted_json.json"
                    
                    questions = parse_uploaded_json(fake_file)
                    if questions:
                        initialize_exam_state(questions)
                        st.success(f"✅ Loaded {len(questions)} questions from pasted JSON!")
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Error parsing JSON text: {e}")
            else:
                st.warning("Please paste some JSON text first.")
    
    # Show warning if no questions
    if not st.session_state.get('questions'):
        st.error("❌ No exam questions available.")
        return
    
    # Exam info header
    st.write("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Questions", len(st.session_state.questions))
    with col2:
        st.metric("Topics Covered", len(st.session_state.topics))
    with col3:
        if not st.session_state.exam_completed:
            current_attempted = sum(1 for ans in st.session_state.user_answers if ans is not None)
            st.metric("Current Score", f"{st.session_state.score}/{current_attempted}")
        else:
            st.metric("Final Score", f"{st.session_state.score}/{len(st.session_state.questions)}")
    with col4:
        if st.button("🔄 Reset Exam", help="Start over with current questions"):
            initialize_exam_state(st.session_state.questions)
            st.rerun()
    
    # Progress persistence info
    answered_count = sum(1 for ans in st.session_state.user_answers if ans is not None)
    st.write(f"**Progress:** {answered_count}/{len(st.session_state.questions)} questions answered • **Auto-saved**")
    
    # Source indicator
    if st.session_state.get('last_uploaded_file_name'):
        current_source = f"📁 {st.session_state.last_uploaded_file_name}"
    else:
        current_source = "📝 Built-in Questions"
    st.write(f"**Question source:** {current_source}")
    
    # Sidebar for exam progress and info
    with st.sidebar:
        st.header("📊 Exam Progress")
        
        current_score = st.session_state.score
        total_questions = len(st.session_state.questions)
        answered_count = sum(1 for ans in st.session_state.user_answers if ans is not None)
        
        if not st.session_state.exam_completed:
            progress = answered_count / total_questions
            score_percentage = (current_score / answered_count) * 100 if answered_count > 0 else 0
        else:
            progress = 1.0
            score_percentage = (current_score / total_questions) * 100
        
        st.write(f"**Score:** {current_score}/{answered_count}")
        st.write(f"**Accuracy:** {score_percentage:.1f}%")
        st.progress(progress)
        st.write(f"**Progress:** {answered_count}/{total_questions}")
        
        # Session management
        st.header("💾 Session")
        if st.button("💾 Save Progress Now", use_container_width=True):
            save_session_state()
            st.success("Progress saved!")
        
        if st.button("🗑️ Clear Saved Session", use_container_width=True):
            if os.path.exists(SESSION_FILE):
                os.remove(SESSION_FILE)
            st.success("Saved session cleared!")
            st.rerun()
        
        # Exam controls
        st.header("🎯 Exam Controls")
        if st.button("🔄 Restart Exam", use_container_width=True):
            initialize_exam_state(st.session_state.questions)
            st.rerun()
        
        if st.button("🔀 Shuffle Questions", use_container_width=True):
            random.shuffle(st.session_state.questions)
            st.session_state.current_question = 0
            st.session_state.answered = False
            save_session_state()
            st.success("Questions shuffled!")
            st.rerun()
        
        # Exam topics
        st.header("📚 Exam Topics")
        for topic, count in st.session_state.topics.items():
            st.write(f"• {topic}: {count} questions")
    
    # Main exam interface
    if not st.session_state.exam_completed:
        current_q = st.session_state.questions[st.session_state.current_question]
        
        # Question header with metadata
        st.subheader(f"📝 Question {st.session_state.current_question + 1}")
        st.markdown(f"**Topic:** {current_q.get('topic', 'General')}")
        if 'page' in current_q:
            st.markdown(f"**Reference:** Page {current_q['page']}")
        
        # Question text
        st.markdown(f"### {current_q['question']}")
        
        if not st.session_state.answered:
            # Display options for answering
            option_labels = list(current_q['options'].keys())
            
            # Pre-select if already answered
            previous_answer = st.session_state.user_answers[st.session_state.current_question]
            user_answer = st.radio(
                "Select your answer:",
                option_labels,
                index=option_labels.index(previous_answer) if previous_answer in option_labels else 0,
                format_func=lambda x: f"{x}. {current_q['options'][x]}",
                key=f"q{st.session_state.current_question}"
            )
            
            # Submit button
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("🚀 Submit Answer", type="primary"):
                    st.session_state.answered = True
                    st.session_state.user_answers[st.session_state.current_question] = user_answer
                    
                    # Check if answer is correct
                    if user_answer == current_q['correct_answer']:
                        st.session_state.score += 1
                    
                    # Auto-save after answering
                    save_session_state()
                    st.rerun()
        
        else:
            # AFTER ANSWERING - SHOW RESULTS AND EXPLANATION
            st.write("---")
            
            # Show answer result
            user_answer = st.session_state.user_answers[st.session_state.current_question]
            if user_answer == current_q['correct_answer']:
                st.success("🎉 **Correct!** Well done!")
            else:
                st.error(f"😞 **Incorrect.** The correct answer is **{current_q['correct_answer']}**")
            
            # Show color-coded options review
            st.subheader("📋 Answer Review")
            option_labels = list(current_q['options'].keys())
            for option in option_labels:
                option_text = f"{option}. {current_q['options'][option]}"
                if option == current_q['correct_answer']:
                    st.success(f"✅ **{option_text}** - **Correct Answer**")
                elif option == user_answer:
                    st.error(f"❌ **{option_text}** - **Your Answer**")
                else:
                    st.write(f"📝 {option_text}")
            
            # SHOW EXPLANATION
            st.write("---")
            if 'explanation' in current_q and current_q['explanation']:
                st.subheader("💡 Explanation")
                st.info(current_q['explanation'])
            else:
                st.warning("No explanation available for this question.")
            
            # Navigation buttons
            st.write("---")
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.session_state.current_question > 0:
                    if st.button("⏮️ Previous Question", use_container_width=True):
                        st.session_state.current_question -= 1
                        st.session_state.answered = False
                        save_session_state()
                        st.rerun()
            
            with col2:
                if st.session_state.current_question < len(st.session_state.questions) - 1:
                    if st.button("⏭️ Next Question", type="primary", use_container_width=True):
                        st.session_state.current_question += 1
                        st.session_state.answered = False
                        save_session_state()
                        st.rerun()
                else:
                    if st.button("🏁 Finish Exam", type="primary", use_container_width=True):
                        st.session_state.exam_completed = True
                        save_session_state()
                        st.rerun()
            
            with col3:
                if st.button("🔄 Try Again", use_container_width=True):
                    st.session_state.answered = False
                    save_session_state()
                    st.rerun()
    
    else:
        # Exam completed
        st.balloons()
        st.success("## 🎉 Exam Completed!")
        
        final_score = st.session_state.score
        total_questions = len(st.session_state.questions)
        score_percentage = (final_score / total_questions) * 100
        
        # Final results
        st.subheader("📈 Final Exam Results")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Questions", total_questions)
        with col2:
            st.metric("Correct Answers", final_score)
        with col3:
            st.metric("Final Score", f"{score_percentage:.1f}%")
        
        # Performance message
        st.write("---")
        if score_percentage >= 90:
            st.success("### 🏆 Outstanding! Exams Genius!")
        elif score_percentage >= 80:
            st.success("### 🌟 Excellent! Strong Understanding of Concepts!")
        elif score_percentage >= 70:
            st.info("### 👍 Very Good! Solid Knowledge Base!")
        elif score_percentage >= 60:
            st.warning("### 📚 Good! Review Challenging Topics!")
        else:
            st.error("### 💪 Keep Studying! Focus on Fundamental Concepts!")
        
        # Restart option
        st.write("---")
        if st.button("🔄 Take Exam Again", type="primary"):
            initialize_exam_state(st.session_state.questions)
            st.rerun()

if __name__ == "__main__":
    main()
