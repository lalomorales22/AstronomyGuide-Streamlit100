import streamlit as st
import ollama
import time
import json
import os
import random
from datetime import datetime
from openai import OpenAI

# List of available models
MODELS = [
    "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo",  # OpenAI models
    "llama3.1:8b", "gemma2:2b", "mistral-nemo:latest", "phi3:latest",  # Ollama models
]

# Astronomy topics
ASTRONOMY_TOPICS = [
    "Solar System", "Stars", "Galaxies", "Cosmology", "Exoplanets",
    "Black Holes", "Nebulae", "Telescopes", "Space Exploration", "Astrobiology"
]

# Learning modes
LEARNING_MODES = [
    "Virtual Tour", "Concept Explanation", "Historical Timeline",
    "Interactive Quiz", "Image Analysis", "Space News", "Astronomical Phenomena",
    "Scientist Spotlight", "Equipment Guide"
]

def get_ai_response(messages, model):
    if model.startswith("gpt-"):
        return get_openai_response(messages, model)
    else:
        return get_ollama_response(messages, model)

def get_openai_response(messages, model):
    client = OpenAI()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content, response.usage.prompt_tokens, response.usage.completion_tokens
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, 0, 0

def get_ollama_response(messages, model):
    try:
        response = ollama.chat(
            model=model,
            messages=messages
        )
        return response['message']['content'], response['prompt_eval_count'], response['eval_count']
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, 0, 0

def stream_response(messages, model):
    if model.startswith("gpt-"):
        return stream_openai_response(messages, model)
    else:
        return stream_ollama_response(messages, model)

def stream_openai_response(messages, model):
    client = OpenAI()
    try:
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )
        return stream
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def stream_ollama_response(messages, model):
    try:
        stream = ollama.chat(
            model=model,
            messages=messages,
            stream=True
        )
        return stream
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def save_conversation(messages, filename):
    conversation = {
        "timestamp": datetime.now().isoformat(),
        "messages": messages
    }
    
    os.makedirs('conversations', exist_ok=True)
    file_path = os.path.join('conversations', filename)
    
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                conversations = json.load(f)
        else:
            conversations = []
    except json.JSONDecodeError:
        conversations = []
    
    conversations.append(conversation)
    
    with open(file_path, 'w') as f:
        json.dump(conversations, f, indent=2)

def load_conversations(uploaded_file):
    if uploaded_file is not None:
        try:
            conversations = json.loads(uploaded_file.getvalue().decode("utf-8"))
            return conversations
        except json.JSONDecodeError:
            st.error(f"Error decoding the uploaded file. The file may be corrupted or not in JSON format.")
            return []
    else:
        st.warning("No file was uploaded.")
        return []

def generate_quiz(topic, num_questions):
    prompt = f"Generate a multiple-choice quiz with {num_questions} questions about {topic} in astronomy. Format the quiz in a JSON structure with 'questions' as the key, and each question should have 'question', 'options' (array of 4 choices), and 'correct_answer' (index of the correct option) fields."
    messages = [
        {"role": "system", "content": "You are an astronomy education AI assistant specializing in creating quizzes about space and celestial objects."},
        {"role": "user", "content": prompt}
    ]
    response, _, _ = get_ai_response(messages, st.session_state.model)
    try:
        quiz_data = json.loads(response)
        return quiz_data['questions']
    except json.JSONDecodeError:
        st.error("Error parsing the quiz data. Please try again.")
        return []

def main():
    st.set_page_config(layout="wide")
    st.title("Astronomy Guide: Virtual Universe Explorer")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "token_count" not in st.session_state:
        st.session_state.token_count = {"prompt": 0, "completion": 0}

    if "user_name" not in st.session_state:
        st.session_state.user_name = "Space Explorer"

    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []

    if "current_question" not in st.session_state:
        st.session_state.current_question = 0

    if "score" not in st.session_state:
        st.session_state.score = 0

    st.session_state.user_name = st.text_input("Enter your name:", value=st.session_state.user_name)

    st.sidebar.title("Astronomy Guide Configuration")
    st.session_state.model = st.sidebar.selectbox("Choose a model", MODELS)

    topic = st.sidebar.selectbox("Select astronomy topic", ASTRONOMY_TOPICS)
    mode = st.sidebar.selectbox("Choose learning mode", LEARNING_MODES)

    difficulty_level = st.sidebar.select_slider(
        "Select difficulty level",
        options=["Beginner", "Intermediate", "Advanced"],
        value="Intermediate"
    )

    if mode == "Interactive Quiz":
        num_questions = st.sidebar.number_input("Number of questions", min_value=1, max_value=10, value=5)
        if st.sidebar.button("Generate Quiz"):
            st.session_state.quiz_questions = generate_quiz(topic, num_questions)
            st.session_state.current_question = 0
            st.session_state.score = 0

    custom_instructions = st.sidebar.text_area("Custom Instructions", 
        f"""You are an expert Astronomy Guide AI. Your role is to provide engaging and educational content about the universe. Use the following information to tailor your responses:

Topic: {topic}
Learning Mode: {mode}
Difficulty Level: {difficulty_level}

When providing astronomy education:
1. Explain astronomical concepts clearly and accurately
2. Use vivid descriptions to help users visualize celestial objects and phenomena
3. Provide relevant scientific facts and recent discoveries
4. Discuss the scale and distances involved in astronomy
5. Explain how astronomers study the universe
6. Adapt the content to the chosen difficulty level

For different learning modes:
- Virtual Tour: Guide users through a simulated journey of celestial objects or regions
- Concept Explanation: Provide detailed explanations of astronomical concepts
- Historical Timeline: Discuss the history of astronomical discoveries and space exploration
- Interactive Quiz: Generate quiz questions to test knowledge (handled separately)
- Image Analysis: Describe and explain astronomical images
- Space News: Discuss recent developments and discoveries in astronomy
- Astronomical Phenomena: Explain various celestial events and their significance
- Scientist Spotlight: Highlight important astronomers and their contributions
- Equipment Guide: Explain telescopes and other astronomical tools

When interacting with the user:
- Encourage curiosity and wonder about the universe
- Provide clarification on complex ideas when needed
- Suggest additional resources for further exploration
- Relate astronomical concepts to everyday life when possible
- Address common misconceptions in astronomy

Remember, your goal is to inspire awe and understanding of the universe, making astronomy accessible and exciting for learners of all levels.""")

    theme = st.sidebar.selectbox("Choose a theme", ["Light", "Dark"])
    if theme == "Dark":
        st.markdown("""
        <style>
        .stApp {
            background-color: #1E1E1E;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)

    if st.sidebar.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.token_count = {"prompt": 0, "completion": 0}
        st.session_state.quiz_questions = []
        st.session_state.current_question = 0
        st.session_state.score = 0

    st.sidebar.subheader("Conversation Management")
    save_name = st.sidebar.text_input("Save conversation as:", "astronomy_exploration_session.json")
    if st.sidebar.button("Save Conversation"):
        save_conversation(st.session_state.messages, save_name)
        st.sidebar.success(f"Conversation saved to conversations/{save_name}")

    st.sidebar.subheader("Load Conversation")
    uploaded_file = st.sidebar.file_uploader("Choose a file to load conversations", type=["json"], key="conversation_uploader")
    
    if uploaded_file is not None:
        try:
            conversations = load_conversations(uploaded_file)
            if conversations:
                st.sidebar.success(f"Loaded {len(conversations)} conversations from the uploaded file")
                selected_conversation = st.sidebar.selectbox(
                    "Select a conversation to load",
                    range(len(conversations)),
                    format_func=lambda i: conversations[i]['timestamp']
                )
                if st.sidebar.button("Load Selected Conversation"):
                    st.session_state.messages = conversations[selected_conversation]['messages']
                    st.sidebar.success("Conversation loaded successfully!")
            else:
                st.sidebar.error("No valid conversations found in the uploaded file.")
        except Exception as e:
            st.sidebar.error(f"Error loading conversations: {str(e)}")

    if mode == "Interactive Quiz" and st.session_state.quiz_questions:
        if st.session_state.current_question < len(st.session_state.quiz_questions):
            question = st.session_state.quiz_questions[st.session_state.current_question]
            st.subheader(f"Question {st.session_state.current_question + 1}")
            st.write(question['question'])
            
            user_answer = st.radio("Select your answer:", question['options'])
            if st.button("Submit Answer"):
                if user_answer == question['options'][question['correct_answer']]:
                    st.success("Correct!")
                    st.session_state.score += 1
                else:
                    st.error(f"Incorrect. The correct answer is: {question['options'][question['correct_answer']]}")
                st.session_state.current_question += 1
        else:
            st.success(f"Quiz completed! Your score: {st.session_state.score}/{len(st.session_state.quiz_questions)}")
            if st.button("Start New Quiz"):
                st.session_state.quiz_questions = []
                st.session_state.current_question = 0
                st.session_state.score = 0

    if prompt := st.chat_input("Ask about astronomy or request a virtual tour:"):
        st.session_state.messages.append({"role": "user", "content": f"{st.session_state.user_name}: {prompt}"})
        with st.chat_message("user"):
            st.markdown(f"{st.session_state.user_name}: {prompt}")

        ai_messages = [
            {"role": "system", "content": custom_instructions},
            {"role": "system", "content": f"Provide astronomy education for {topic} at a {difficulty_level} level using the {mode} format when appropriate."},
        ] + st.session_state.messages

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for chunk in stream_response(ai_messages, st.session_state.model):
                if chunk:
                    if st.session_state.model.startswith("gpt-"):
                        full_response += chunk.choices[0].delta.content or ""
                    else:
                        full_response += chunk['message']['content']
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.05)
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

        _, prompt_tokens, completion_tokens = get_ai_response(ai_messages, st.session_state.model)
        st.session_state.token_count["prompt"] += prompt_tokens
        st.session_state.token_count["completion"] += completion_tokens

    st.sidebar.subheader("Token Usage")
    st.sidebar.write(f"Prompt tokens: {st.session_state.token_count['prompt']}")
    st.sidebar.write(f"Completion tokens: {st.session_state.token_count['completion']}")
    st.sidebar.write(f"Total tokens: {sum(st.session_state.token_count.values())}")

if __name__ == "__main__":
    main()
