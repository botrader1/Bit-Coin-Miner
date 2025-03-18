import streamlit as st
from hashlib import sha256
import time

import webbrowser

MAX_VAL = 100000000

def SHA256(text):
    return sha256(text.encode("ascii")).hexdigest()

def mine(block_number, transactions, previous_hash, prefix_zeros):
    prefix_str = '0' * prefix_zeros
    for nonce in range(MAX_VAL):
        text = str(block_number) + transactions + previous_hash + str(nonce)
        new_hash = SHA256(text)
        if new_hash.startswith(prefix_str):
            return nonce, new_hash
    raise BaseException(f"Couldn't find correct hash after trying {MAX_VAL} times")

# Set Page Configuration
st.set_page_config(page_title="Bitcoin Mining Simulator", layout="centered")

# Initialize session state for mining result
if "mining_result" not in st.session_state:
    st.session_state.mining_result = ""

# Custom CSS for Styling
st.markdown(
    """
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .stApp {
            background-color: black;
            border-left: 10px solid #FFD700;
            border-right: 10px solid #FFD700;
        }
        h1 {
            text-align: center;
            font-weight: bold;
            color: white !important;
            border-bottom: 3px solid #FFD700;
            padding-bottom: 10px;
        }
        h5 {
            
            font-weight: bold;
            color: white !important;
            border-bottom: 3px solid #FFD700;
            padding-bottom: 10px;
        }
        .stButton>button {
            background: linear-gradient(45deg, #FFD700, #FFA500);
            color: black;
            font-size: 20px;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
            transition: 0.3s;
            display: block;
            margin: auto;
            width: 250px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background: linear-gradient(45deg, #FFA500, #FFD700);
            transform: scale(1.05);
        }

        /* 3D Animated Result Box */
        .result-box {
            background: linear-gradient(145deg, #222222, #292929);
            border: 2px solid #FFD700;
            border-radius: 15px;
            padding: 15px;
            font-size: 18px;
            font-weight: bold;
            color: white;
            text-align: center;
            box-shadow: 5px 5px 15px rgba(255, 215, 0, 0.4);
            transform: scale(0.8);
            opacity: 0;
            animation: popIn 0.5s ease-in-out forwards;
        }
        @keyframes popIn {
            0% {
                transform: scale(0.8);
                opacity: 0;
            }
            100% {
                transform: scale(1);
                opacity: 1;
            }
        }

        /* Animated Pro Plan Section */
        .pro-box {
            background: rgba(255, 215, 0, 0.1);
            border: 2px solid #FFD700;
            border-radius: 15px;
            padding: 20px;
            font-size: 20px;
            font-weight: bold;
            color: white;
            text-align: center;
            box-shadow: 0px 0px 15px #FFD700;
            margin-top: 20px;
            opacity: 0;
            animation: fadeIn 1s ease-in-out forwards;
        }
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# UI Layout
st.markdown("<h1>💰Bitcoin Mining Simulator💰</h1>", unsafe_allow_html=True)

# Apply global CSS for white text
st.markdown(
    """
    <style>
        label {
            color: white !important;
            font-size: 18px !important;
            font-weight: bold !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# UI with input fields
block_number = st.number_input("🔢 **Block Number** *(Block Identifier)*", min_value=1, value=5, step=1)
transactions = st.text_area("🔄 **Transactions** *(List of Transfers)*", "Alice -> Bob -> 10, Charlie -> Dave -> 25")
previous_hash = st.text_input("🔗 **Previous Hash** *(Hash of the Previous Block)*", "b5d4045c3f466fa91fe2cc6abe79232a1a57cdf104f7a26e716e0a1e2789df78")
difficulty = st.slider("⚡ **Difficulty Level** *(Number of Leading Zeros)*", min_value=1, max_value=5, value=5)


if st.button("Start Mining"):
     with st.spinner("Mining in progress... ⛏️"):
        start = time.time()
        nonce, new_hash = mine(block_number, transactions, previous_hash, difficulty)
        total_time = time.time() - start
        
        st.success("✅ Mining Completed! 🎉")

        if nonce is not None:
            st.session_state.mining_result = f"""
            <style>
                .result-box {{
                    background: linear-gradient(145deg, #FFD700, #FFA500);
                    border-radius: 15px;
                    padding: 20px;
                    text-align: center;
                    font-size: 20px;
                    font-weight: bold;
                    color: black;
                    box-shadow: 5px 5px 15px rgba(255, 215, 0, 0.4);
                    margin-bottom: 20px;
                }}
                .hash-box {{
                    background: black;
                    color: #FFD700;
                    font-family: 'Courier New', monospace;
                    padding: 15px;
                    border-radius: 10px;
                    font-size: 16px;
                    text-align: center;
                    box-shadow: inset 0px 0px 10px rgba(255, 215, 0, 0.7);
                    margin-top: 15px;
                }}
            </style>
            <div class="result-box">
                ✅ <b>Successfully Mined the Block!</b> <br><br>
                🔢 <b>Nonce:</b> {nonce} <br>
                ⏳ <b>Time Taken:</b> {total_time:.2f} seconds
                <div class="hash-box">
                    🔗 <b>New Hash:</b> <br> {new_hash}
                </div>
            </div>
            """
else:
        st.session_state.mining_result = ""
    
st.markdown(st.session_state.mining_result, unsafe_allow_html=True)

st.markdown('<hr style="border:1px solid yellow;">', unsafe_allow_html=True)
# Pro Feature: Payment Gateway for Pro Users
st.markdown("""
    <div class="pro-box">
        🔥 <strong>Upgrade to Pro for Exclusive Features!</strong> <br>
        🚀 For further difficulty levels, purchase the pro plan!
    </div>
""", unsafe_allow_html=True)


st.markdown('<hr style="border:1px solid yellow;">', unsafe_allow_html=True)
if st.button("🔗 Purchase Pro Plan"):
    webbrowser.open("https://your-payment-gateway.com")  # Replace with actual payment URL