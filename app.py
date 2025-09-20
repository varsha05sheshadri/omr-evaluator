# app.py
import streamlit as st
import cv2
import numpy as np

ANSWER_KEY_A = [
    0,2,2,2,2,0,2,2,2,2,
    0,3,3,0,1,0,2,3,1,1,
    0,3,1,0,2,1,2,1,3,2,
    2,0,2,2,0,1,2,1,3,3,
    1,2,2,0,2,1,2,2,3,1,
    1,2,0,1,2,1,0,0,1,1,
    2,2,0,2,2,1,2,2,2,1,
    1,0,1,1,2,1,1,1,1,2,
    1,0,2,1,2,1,1,1,2,2,
    0,1,2,1,2,1,2,0,2,2
]

ANSWER_KEY_B = ANSWER_KEY_A  # same as A for simplicity

# -------------------------
# OMR evaluation function
# -------------------------
def evaluate_omr(image_file, set_choice='A'):
    if set_choice.upper() == 'A':
        ANSWER_KEY = ANSWER_KEY_A
    else:
        ANSWER_KEY = ANSWER_KEY_B

    try:
        # Read image from uploaded file
        image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        questionCnts = sorted(cnts, key=lambda c: cv2.boundingRect(c)[1])

        bubbles_per_question = 4
        questions = [questionCnts[i:i+bubbles_per_question] for i in range(0, len(questionCnts), bubbles_per_question)]
        questions = questions[:len(ANSWER_KEY)]

        correct_count = 0
        results = []

        for q_index, q_bubbles in enumerate(questions):
            if len(q_bubbles) != bubbles_per_question:
                continue
            q_bubbles = sorted(q_bubbles, key=lambda c: cv2.boundingRect(c)[0])
            bubble_values = []
            for bubble in q_bubbles:
                mask = np.zeros(thresh.shape, dtype="uint8")
                cv2.drawContours(mask, [bubble], -1, 255, -1)
                mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                bubble_values.append(cv2.countNonZero(mask))
            chosen_option = int(np.argmax(bubble_values))
            correct_option = ANSWER_KEY[q_index]
            is_correct = chosen_option == correct_option
            if is_correct:
                correct_count += 1
            results.append({
                "question": q_index + 1,
                "chosen": chosen_option,
                "correct": is_correct
            })

        return {"score": correct_count, "details": results}, None

    except Exception as e:
        return None, str(e)

# -------------------------
# Streamlit UI
# -------------------------

# Custom CSS styling
st.markdown(
    """
    <style>
    body {
        background-color: #f4f4f9;
    }
    .title {
        color: #4CAF50;
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        margin-top: 20px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        height: 3em;
        width: 12em;
        border-radius: 10px;
        border: none;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title">Zero-Day OMR Evaluator</div>', unsafe_allow_html=True)

# User inputs
set_choice = st.radio("Select Answer Set", options=['A', 'B'], index=0)
uploaded_file = st.file_uploader("Upload OMR Sheet (Image)", type=['jpg','jpeg','png'])

# Process uploaded file
if uploaded_file is not None:
    result, error = evaluate_omr(uploaded_file, set_choice=set_choice)
    if error:
        st.error(f"Error: {error}")
    else:
        st.success(f"Score: {result['score']} / {len(result['details'])}")
        st.markdown("### Detailed Results")
        st.json(result['details'])
