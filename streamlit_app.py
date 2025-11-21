import streamlit as st
import random
import json
import os
import tempfile
import io

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
            "id": 1,
            "topic": "Language Categories",
            "question": "Which category of programming languages achieves its effect by changing the value of variables through assignment statements?",
            "options": {
                "A": "Functional Languages",
                "B": "Logic Programming Languages", 
                "C": "Imperative Languages",
                "D": "Object-Oriented Languages"
            },
            "correct_answer": "C",
            "page": 1,
            "explanation": "Imperative languages work by changing program state through assignment statements and commands."
        },
        {
            "id": 2,
            "topic": "Functional Programming",
            "question": "Which of the following is a key characteristic of functional programming?",
            "options": {
                "A": "Mutable state",
                "B": "Side effects",
                "C": "Immutable data",
                "D": "Class inheritance"
            },
            "correct_answer": "C",
            "page": 2,
            "explanation": "Functional programming emphasizes immutable data and avoiding side effects."
        }
    ]

def analyze_exam_topics(questions):
    """Analyze and categorize exam questions by topic"""
    topics = {}
    for q in questions:
        topic = q.get('topic', 'General')
        topics[topic] = topics.get(topic, 0) + 1
    return topics

def initialize_exam_state(questions=None):
    """Initialize or reset the exam state"""
    if questions is None:
        questions = load_questions_from_json()
    
    st.session_state.questions = questions
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.user_answers = [None] * len(questions)
    st.session_state.exam_completed = False
    st.session_state.topics = analyze_exam_topics(questions)
    st.session_state.questions_loaded = True

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

    # Initialize session state
    if 'questions_loaded' not in st.session_state:
        initialize_exam_state()
    
    # Header
    st.title("💻Exam")
    st.markdown("### Upload your own JSON question file or use the built-in questions")
    
    # File Upload Section - PROMINENTLY DISPLAYED
    with st.expander("📁 Upload Your JSON Question File", expanded=True):
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
        
        **Alternative formats also supported:**
        - Direct array of questions
        - Any key containing an array of questions with 'question', 'options', and 'correct_answer' fields
        """)
        
        uploaded_file = st.file_uploader(
            "Choose a JSON file", 
            type="json",
            help="Upload your questions in JSON format",
            key="file_uploader"
        )
        
        # AUTO-LOAD when file is uploaded
        if uploaded_file is not None and uploaded_file != st.session_state.get('last_uploaded_file'):
            # Parse the uploaded file
            questions = parse_uploaded_json(uploaded_file)
            
            if questions:
                # Auto-load the questions
                initialize_exam_state(questions)
                st.session_state.last_uploaded_file = uploaded_file
                st.success(f"✅ Automatically loaded {len(questions)} questions from uploaded file!")
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
            placeholder='Paste your JSON questions here...\n\nExample:\n{\n  "questions": [\n    {\n      "question": "Your question?",\n      "options": {"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"},\n      "correct_answer": "A",\n      "explanation": "Your explanation"\n    }\n  ]\n}',
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
    if not st.session_state.questions:
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
            current_attempted = st.session_state.current_question + 1 if st.session_state.current_question > 0 else 0
            st.metric("Current Score", f"{st.session_state.score}/{current_attempted}")
        else:
            st.metric("Final Score", f"{st.session_state.score}/{len(st.session_state.questions)}")
    with col4:
        if st.button("🔄 Reset to Built-in Questions"):
            initialize_exam_state()
            st.rerun()
    
    # Source indicator
    current_source = "📁 Uploaded File" if st.session_state.get('last_uploaded_file') else "📝 Built-in Questions"
    st.write(f"**Current question source:** {current_source}")
    
    # Sidebar for exam progress and info
    with st.sidebar:
        st.header("📊 Exam Progress")
        
        current_score = st.session_state.score
        total_questions = len(st.session_state.questions)
        
        if not st.session_state.exam_completed:
            questions_attempted = st.session_state.current_question + 1
            progress = questions_attempted / total_questions
            score_percentage = (current_score / questions_attempted) * 100 if questions_attempted > 0 else 0
        else:
            questions_attempted = total_questions
            progress = 1.0
            score_percentage = (current_score / total_questions) * 100
        
        st.write(f"**Score:** {current_score}/{questions_attempted}")
        st.write(f"**Accuracy:** {score_percentage:.1f}%")
        st.progress(progress)
        st.write(f"**Progress:** {questions_attempted}/{total_questions}")
        
        # Exam controls
        st.header("🎯 Exam Controls")
        if st.button("🔄 Restart Exam", use_container_width=True):
            initialize_exam_state(st.session_state.questions)
            st.rerun()
        
        if st.button("🔀 Shuffle Questions", use_container_width=True):
            random.shuffle(st.session_state.questions)
            st.session_state.current_question = 0
            st.session_state.answered = False
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
            user_answer = st.radio(
                "Select your answer:",
                option_labels,
                format_func=lambda x: f"{x}. {current_q['options'][x]}",
                key=f"q{st.session_state.current_question}"
            )
            
            # Submit button
            if st.button("🚀 Submit Answer", type="primary"):
                st.session_state.answered = True
                st.session_state.user_answers[st.session_state.current_question] = user_answer
                
                # Check if answer is correct
                if user_answer == current_q['correct_answer']:
                    st.session_state.score += 1
                
                # Rerun to show results and explanation
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
                        st.rerun()
            
            with col2:
                if st.session_state.current_question < len(st.session_state.questions) - 1:
                    if st.button("⏭️ Next Question", type="primary", use_container_width=True):
                        st.session_state.current_question += 1
                        st.session_state.answered = False
                        st.rerun()
                else:
                    if st.button("🏁 Finish Exam", type="primary", use_container_width=True):
                        st.session_state.exam_completed = True
                        st.rerun()
            
            with col3:
                if st.button("🔄 Try Again", use_container_width=True):
                    st.session_state.answered = False
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
            st.success("### 🏆 Outstanding! Programming Languages Expert!")
        elif score_percentage >= 80:
            st.success("### 🌟 Excellent! Strong Understanding of Concepts!")
        elif score_percentage >= 70:
            st.info("### 👍 Very Good! Solid Knowledge Base!")
        elif score_percentage >= 60:
            st.warning("### 📚 Good! Review Challenging Topics!")
        else:
            st.error("### 💪 Keep Studying! Focus on Fundamental Concepts!")
        
        # Detailed answer review with explanations
        st.subheader("🔍 Detailed Answer Review")
        for i, question in enumerate(st.session_state.questions):
            with st.expander(f"Question {i+1}: {question['question'][:80]}...", expanded=False):
                user_ans = st.session_state.user_answers[i]
                correct_ans = question['correct_answer']
                
                # Show question details
                st.write(f"**Topic:** {question.get('topic', 'General')}")
                if 'page' in question:
                    st.write(f"**Reference:** Page {question['page']}")
                
                # Show user's answer vs correct answer
                st.write(f"**Your answer:** {user_ans}. {question['options'][user_ans] if user_ans else 'Not answered'}")
                st.write(f"**Correct answer:** {correct_ans}. {question['options'][correct_ans]}")
                
                # Show explanation
                if 'explanation' in question and question['explanation']:
                    st.info(f"**Explanation:** {question['explanation']}")
                
                # Show result
                if user_ans == correct_ans:
                    st.success("✅ You answered this correctly!")
                else:
                    st.error("❌ You answered this incorrectly.")
        
        # Restart option
        st.write("---")
        if st.button("🔄 Take Exam Again", type="primary"):
            initialize_exam_state(st.session_state.questions)
            st.rerun()

if __name__ == "__main__":
    main()
