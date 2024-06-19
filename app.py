import streamlit as st
import json
import os

# 파일 경로 설정
USER_DATA_FILE = "data/users.json"

# 사용자 데이터 로드
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

# 사용자 데이터 저장
def save_users(users):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=2)

# 사용자 등록
def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = {"password": password, "notes": [""] * 7}
    save_users(users)
    return True

# 사용자 로그인 확인
def validate_user(username, password):
    users = load_users()
    return username in users and users[username]["password"] == password

# 노트 저장
def save_notes(username, tab_index, note):
    users = load_users()
    if username in users:
        users[username]["notes"][tab_index] = note
        save_users(users)

# 노트 로드
def load_notes(username, tab_index):
    users = load_users()
    if username in users:
        return users[username]["notes"][tab_index]
    return ""

# Streamlit 애플리케이션 시작
st.title("Tabbed Notepad")

# 세션 상태 초기화
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "tab_index" not in st.session_state:
    st.session_state["tab_index"] = 0

# 로그인 상태 확인
if st.session_state["username"] == "":
    st.subheader("Login")
    login_username = st.text_input("Username")
    login_password = st.text_input("Password", type="password")
    if st.button("Login"):
        if validate_user(login_username, login_password):
            st.session_state["username"] = login_username
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")
    
    st.subheader("Register")
    register_username = st.text_input("New Username")
    register_password = st.text_input("New Password", type="password")
    if st.button("Register"):
        if register_user(register_username, register_password):
            st.success("Registration successful")
        else:
            st.error("User already exists")
else:
    st.subheader(f"Welcome, {st.session_state['username']}")
    days = ["SU", "MO", "TU", "WE", "TH", "FR", "SA"]
    st.session_state["tab_index"] = st.selectbox("Select Day", range(7), format_func=lambda x: days[x])
    note = st.text_area("Your Notes", load_notes(st.session_state["username"], st.session_state["tab_index"]))
    if st.button("Save"):
        save_notes(st.session_state["username"], st.session_state["tab_index"], note)
        st.success("Notes saved")
    
    if st.button("Logout"):
        st.session_state["username"] = ""
        st.experimental_rerun()
