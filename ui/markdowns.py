import streamlit as st


def styles():
    st.markdown("""
        <style>
        .main-container {
            background-color: #212121;
            color: #e0e0e0;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        .sidebar .block-container {
            background-color: #2c2c2c;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .stButton>button {
            background-color: #e53935;
            color: white;
            font-size: 16px;
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #d32f2f;
        }
        .stTextInput>div>div>input {
            border-radius: 8px;
            font-size: 16px;
            background-color: #2c2c2c;
            color: #e0e0e0;
            border: 1px solid #e53935;
            padding: 8px;
        }
        .stSelectbox select {
            background-color: #2c2c2c;
            color: #e0e0e0;
            border: 1px solid #e53935;
            border-radius: 8px;
            padding: 8px;
        }
        .stSlider>div>div>input {
            background-color: #2c2c2c;
            border-radius: 8px;
            color: #e0e0e0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    
def div():
    st.markdown('<div class="sidebar block-container">', unsafe_allow_html=True)
    

def end_div():
    st.markdown('</div>', unsafe_allow_html=True)