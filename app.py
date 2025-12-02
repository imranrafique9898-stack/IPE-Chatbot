import streamlit as st

# ============ BASIC CONFIG ============
st.set_page_config(page_title="IPE Chatbot", page_icon="🎓")

MAIN_MENU_TEXT = (
    "Welcome to IPE – Institute of Professional Excellence! 👋\n\n"
    "How can I assist you today?"
)

CONTACT_TEXT = (
    "📞 **Contact IPE**\n"
    "- Call / WhatsApp: **0307-1722224**\n"
    "- Office Hours: **10 AM – 8 PM**"
)

ERROR_MESSAGE = "Sorry, I didn’t understand that. Please use the buttons."


# ============ STATE HELPERS ============
def init_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "state" not in st.session_state:
        st.session_state.state = "MAIN_MENU"
    if "selected_course" not in st.session_state:
        st.session_state.selected_course = None
    if "lead" not in st.session_state:
        reset_lead()
    if "pending_action" not in st.session_state:
        st.session_state.pending_action = None
    if "pending_label" not in st.session_state:
        st.session_state.pending_label = None


def reset_lead():
    st.session_state.lead = {
        "full_name": None,
        "email": None,
        "phone": None,
        "availability": None,
        "course_interest": None,
        "source": None,
    }


def go_to_main_menu():
    st.session_state.state = "MAIN_MENU"
    st.session_state.selected_course = None
    reset_lead()
    return MAIN_MENU_TEXT


def set_action(action_value: str, label: str):
    """Callback used by buttons to store the action in session state."""
    st.session_state.pending_action = action_value
    st.session_state.pending_label = label


# ============ LOGIC HANDLERS ============
def handle_main_menu(choice: str) -> str:
    if choice == "1":
        st.session_state.state = "COURSE_MENU"
        return "Please select a course from the buttons below."

    elif choice == "2":
        # Admissions guidance + lead flow
        st.session_state.state = "AD_LEAD_NAME"
        reset_lead()
        st.session_state.lead["source"] = "Admissions"
        return (
            "**Admissions Guidance**\n\n"
            "Contact via Call/WhatsApp: **0307-1722224**\n"
            "Registration is **Free**.\n\n"
            "Please enter your **Full Name**:"
        )

    elif choice == "3":
        st.session_state.state = "FEES_INFO"
        return (
            "**Fees & Duration**\n\n"
            "💰 Fee: **Rs. 20,000 – 30,000**\n"
            "⏱ Duration: **4–8 weeks**"
        )

    elif choice == "4":
        st.session_state.state = "CONTACT_INFO"
        return CONTACT_TEXT

    elif choice == "5":
        st.session_state.state = "STUDENT_INFO"
        return (
            "**Student Support**\n\n"
            "For class timings, teacher availability or study material, "
            "please contact **0307-1722224**."
        )

    elif choice == "6":
        st.session_state.state = "UPCOMING_ASK"
        return (
            "**Upcoming Courses**\n\n"
            "- Nebosh\n"
            "- IOSH\n\n"
            "Would you like to be notified when these launch?"
        )

    elif choice == "7":
        st.session_state.state = "ASK_ANYTHING"
        return (
            "You can type your question.\n\n"
            "If the answer is not available here, please contact **0307-1722224**."
        )

    else:
        return ERROR_MESSAGE


def handle_course_menu(choice: str) -> str:
    course_map = {
        "1": "Digital Marketing",
        "2": "IELTS",
        "3": "TOEFL",
        "4": "PTE",
        "5": "LanguageCert",
        "6": "AI Learning (Python, Data Science, ML)",
        "7": "Nebosh / IOSH (Coming Soon)",
    }

    if choice in course_map:
        st.session_state.selected_course = course_map[choice]
        reset_lead()
        st.session_state.lead["course_interest"] = course_map[choice]
        st.session_state.lead["source"] = "Course Details"
        st.session_state.state = "COURSE_LEAD_NAME"
        return (
            f"You selected: **{course_map[choice]}**\n\n"
            "You can also contact us at **0307-1722224**.\n\n"
            "Please enter your **Full Name**:"
        )
    elif choice == "menu":
        return go_to_main_menu()
    else:
        return ERROR_MESSAGE


def handle_course_lead(message: str) -> str:
    msg = message.strip()

    if st.session_state.state == "COURSE_LEAD_NAME":
        if not msg:
            return "Please enter your **Full Name**:"
        st.session_state.lead["full_name"] = msg
        st.session_state.state = "COURSE_LEAD_EMAIL"
        return "Enter your **Email Address**:"

    elif st.session_state.state == "COURSE_LEAD_EMAIL":
        if not msg:
            return "Please enter your **Email Address**:"
        st.session_state.lead["email"] = msg
        st.session_state.state = "COURSE_LEAD_PHONE"
        return "Enter your **Phone Number with country code** (e.g. +92XXXXXXXXXX):"

    elif st.session_state.state == "COURSE_LEAD_PHONE":
        if not msg:
            return "Please enter your **Phone Number with country code**:"
        st.session_state.lead["phone"] = msg
        st.session_state.state = "COURSE_LEAD_AVAIL"
        return "When are you **available to be contacted**? (e.g. evenings, 3–5 PM)"

    elif st.session_state.state == "COURSE_LEAD_AVAIL":
        if not msg:
            return "Please enter your **availability** (e.g. evenings, 3–5 PM)."
        st.session_state.lead["availability"] = msg

        print("=== COURSE LEAD ===")
        print(st.session_state.lead)
        print("===================")

        st.session_state.state = "MAIN_MENU"
        reset_lead()
        return "Thank you! Our team will contact you soon.\n\n" + MAIN_MENU_TEXT

    else:
        return go_to_main_menu()


def handle_admissions_lead(message: str) -> str:
    msg = message.strip()

    if st.session_state.state == "AD_LEAD_NAME":
        if not msg:
            return "Please enter your **Full Name**:"
        st.session_state.lead["full_name"] = msg
        st.session_state.state = "AD_LEAD_EMAIL"
        return "Enter your **Email Address**:"

    elif st.session_state.state == "AD_LEAD_EMAIL":
        if not msg:
            return "Please enter your **Email Address**:"
        st.session_state.lead["email"] = msg
        st.session_state.state = "AD_LEAD_PHONE"
        return "Enter your **Phone Number with country code** (e.g. +92XXXXXXXXXX):"

    elif st.session_state.state == "AD_LEAD_PHONE":
        if not msg:
            return "Please enter your **Phone Number with country code**:"
        st.session_state.lead["phone"] = msg
        st.session_state.state = "AD_LEAD_COURSE_SELECT"
        return "Please select the **course you are interested in** from the buttons below."

    elif st.session_state.state == "AD_LEAD_COURSE_SELECT":
        course_map = {
            "c1": "Digital Marketing",
            "c2": "IELTS",
            "c3": "TOEFL",
            "c4": "PTE",
            "c5": "LanguageCert",
            "c6": "AI Learning (Python, Data Science, ML)",
            "c7": "Nebosh / IOSH (Coming Soon)",
        }
        if msg in course_map:
            st.session_state.lead["course_interest"] = course_map[msg]

            print("=== ADMISSIONS LEAD ===")
            print(st.session_state.lead)
            print("=======================")

            st.session_state.state = "MAIN_MENU"
            reset_lead()
            return (
                "Thank you for providing your information. We will contact you soon.\n\n"
                + MAIN_MENU_TEXT
            )
        else:
            return "Please choose a course using the buttons below."

    else:
        return go_to_main_menu()


def handle_upcoming_flow(message: str) -> str:
    msg = message.strip().lower()

    if st.session_state.state == "UPCOMING_ASK":
        if msg == "yes":
            reset_lead()
            st.session_state.lead["source"] = "Upcoming Courses"
            st.session_state.state = "UP_LEAD_NAME"
            return "Please enter your **Full Name**:"
        elif msg == "no":
            return go_to_main_menu()
        else:
            return "Please choose **Yes** or **No** using the buttons."

    if st.session_state.state == "UP_LEAD_NAME":
        if not msg:
            return "Please enter your **Full Name**:"
        st.session_state.lead["full_name"] = msg
        st.session_state.state = "UP_LEAD_EMAIL"
        return "Enter your **Email Address**:"

    elif st.session_state.state == "UP_LEAD_EMAIL":
        if not msg:
            return "Please enter your **Email Address**:"
        st.session_state.lead["email"] = msg
        st.session_state.state = "UP_LEAD_PHONE"
        return "Enter your **Phone Number with country code** (e.g. +92XXXXXXXXXX):"

    elif st.session_state.state == "UP_LEAD_PHONE":
        if not msg:
            return "Please enter your **Phone Number with country code**:"
        st.session_state.lead["phone"] = msg
        st.session_state.state = "UP_LEAD_COURSE_SELECT"
        return "Please select the **course you are interested in** from the buttons below."

    elif st.session_state.state == "UP_LEAD_COURSE_SELECT":
        if msg in ["nebosh", "iosh"]:
            st.session_state.lead["course_interest"] = msg.capitalize()

            print("=== UPCOMING LEAD ===")
            print(st.session_state.lead)
            print("=====================")

            st.session_state.state = "MAIN_MENU"
            reset_lead()
            return (
                "Thank you for your interest. We will contact you when these courses are launched.\n\n"
                + MAIN_MENU_TEXT
            )
        else:
            return "Please select **Nebosh** or **IOSH** using the buttons."

    else:
        return go_to_main_menu()


def handle_ask_anything(message: str) -> str:
    st.session_state.state = "MAIN_MENU"
    return (
        "Thanks for your question.\n"
        "For detailed guidance, please contact **0307-1722224**.\n\n"
        + MAIN_MENU_TEXT
    )


def handle_message(message: str) -> str:
    msg = message.strip()
    state = st.session_state.state

    if msg.lower() in ["menu", "main menu"]:
        return go_to_main_menu()

    if state == "MAIN_MENU":
        return handle_main_menu(msg)

    elif state == "COURSE_MENU":
        return handle_course_menu(msg)

    elif state in ["COURSE_LEAD_NAME", "COURSE_LEAD_EMAIL", "COURSE_LEAD_PHONE", "COURSE_LEAD_AVAIL"]:
        return handle_course_lead(msg)

    elif state in ["AD_LEAD_NAME", "AD_LEAD_EMAIL", "AD_LEAD_PHONE", "AD_LEAD_COURSE_SELECT"]:
        return handle_admissions_lead(msg)

    elif state in ["UPCOMING_ASK", "UP_LEAD_NAME", "UP_LEAD_EMAIL", "UP_LEAD_PHONE", "UP_LEAD_COURSE_SELECT"]:
        return handle_upcoming_flow(msg)

    elif state == "ASK_ANYTHING":
        return handle_ask_anything(msg)

    elif state in ["FEES_INFO", "CONTACT_INFO", "STUDENT_INFO"]:
        # Only back button is used there
        return "Use **Back to Main Menu** button below."

    else:
        return go_to_main_menu()


# ============ STREAMLIT UI ============
init_state()

# 1) Handle any pending button action BEFORE rendering chat
pending_action = st.session_state.pending_action
pending_label = st.session_state.pending_label
st.session_state.pending_action = None
st.session_state.pending_label = None

if pending_action is not None:
    # user bubble
    st.session_state.chat_history.append({"role": "user", "content": pending_label})
    # bot reply
    reply = handle_message(pending_action)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

# 2) Title
st.title("IPE Chatbot 🎓")
st.caption("Menu-based chatbot for IPE – Institute of Professional Excellence")

# 3) Show chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# first welcome
if not st.session_state.chat_history:
    first = go_to_main_menu()
    st.session_state.chat_history.append({"role": "assistant", "content": first})
    with st.chat_message("assistant"):
        st.markdown(first)

# 4) Now render buttons based on UPDATED state
state = st.session_state.state

st.markdown("---")
st.subheader("Options")

if state == "MAIN_MENU":
    c1, c2, c3 = st.columns(3)
    with c1:
        st.button("1️⃣ Course Details", on_click=set_action, args=("1", "Course Details"))
        st.button("4️⃣ Contact IPE", on_click=set_action, args=("4", "Contact IPE"))
    with c2:
        st.button("2️⃣ Admissions Guidance", on_click=set_action, args=("2", "Admissions Guidance"))
        st.button("5️⃣ Student Support", on_click=set_action, args=("5", "Student Support"))
    with c3:
        st.button("3️⃣ Fees & Duration", on_click=set_action, args=("3", "Fees & Duration"))
        st.button("6️⃣ Upcoming Courses", on_click=set_action, args=("6", "Upcoming Courses"))
    st.button("7️⃣ Ask Anything", on_click=set_action, args=("7", "Ask Anything"))

elif state == "COURSE_MENU":
    st.write("**Select a course:**")
    cols = st.columns(3)
    cols[0].button("Digital Marketing", on_click=set_action, args=("1", "Digital Marketing"))
    cols[1].button("IELTS", on_click=set_action, args=("2", "IELTS"))
    cols[2].button("TOEFL", on_click=set_action, args=("3", "TOEFL"))
    cols[0].button("PTE", on_click=set_action, args=("4", "PTE"))
    cols[1].button("LanguageCert", on_click=set_action, args=("5", "LanguageCert"))
    cols[2].button("AI Learning (Python/DS/ML)", on_click=set_action,
                   args=("6", "AI Learning (Python/DS/ML)"))
    st.button("Nebosh / IOSH (Coming Soon)", on_click=set_action,
              args=("7", "Nebosh / IOSH (Coming Soon)"))
    st.button("⬅ Back to Main Menu", on_click=set_action, args=("menu", "Back to Main Menu"))

elif state in ["FEES_INFO", "CONTACT_INFO", "STUDENT_INFO"]:
    st.button("⬅ Back to Main Menu", on_click=set_action, args=("menu", "Back to Main Menu"))

elif state == "UPCOMING_ASK":
    st.write("Would you like to be notified?")
    c1, c2 = st.columns(2)
    c1.button("✅ Yes", on_click=set_action, args=("yes", "Yes"))
    c2.button("❌ No", on_click=set_action, args=("no", "No"))
    st.button("⬅ Back to Main Menu", on_click=set_action, args=("menu", "Back to Main Menu"))

# show Nebosh / IOSH buttons once we reached the course-select step
elif state in ["UP_LEAD_COURSE_SELECT"]:
    st.write("Select the **course you are interested in**:")
    c1, c2 = st.columns(2)
    c1.button("Nebosh", on_click=set_action, args=("nebosh", "Nebosh"))
    c2.button("IOSH", on_click=set_action, args=("iosh", "IOSH"))

elif state == "AD_LEAD_COURSE_SELECT":
    st.write("Select the **course you are interested in**:")
    cols = st.columns(3)
    cols[0].button("Digital Marketing", on_click=set_action, args=("c1", "Digital Marketing"))
    cols[1].button("IELTS", on_click=set_action, args=("c2", "IELTS"))
    cols[2].button("TOEFL", on_click=set_action, args=("c3", "TOEFL"))
    cols[0].button("PTE", on_click=set_action, args=("c4", "PTE"))
    cols[1].button("LanguageCert", on_click=set_action, args=("c5", "LanguageCert"))
    cols[2].button("AI Learning (Python/DS/ML)", on_click=set_action,
                   args=("c6", "AI Learning (Python/DS/ML)"))
    st.button("Nebosh / IOSH (Coming Soon)", on_click=set_action,
              args=("c7", "Nebosh / IOSH (Coming Soon)"))

# 5) Text input (for lead fields + Ask Anything)
user_input = st.chat_input("Type here (for name, email, phone, questions, etc.)...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    reply = handle_message(user_input)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        st.markdown(reply)
