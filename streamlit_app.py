import streamlit as st
import qrcode
import io

st.set_page_config(page_title="Binary to Decimal", layout="centered")
st.title("🔢 Binary to Decimal")

# Sidebar with QR code
st.sidebar.header("Scan This QR Code to Access the App")
qr_link = "https://divide-by-2.streamlit.app"
qr = qrcode.make(qr_link)
buf = io.BytesIO()
qr.save(buf)
buf.seek(0)
st.sidebar.image(buf, width=300, caption=qr_link)

# Session state setup
if "started" not in st.session_state:
    st.session_state.started = False
if "number" not in st.session_state:
    st.session_state.number = 0
if "current" not in st.session_state:
    st.session_state.current = 0
if "steps" not in st.session_state:
    st.session_state.steps = []
if "binary" not in st.session_state:
    st.session_state.binary = []
if "completed" not in st.session_state:
    st.session_state.completed = False
if "ready_for_remainder" not in st.session_state:
    st.session_state.ready_for_remainder = False

def reset():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Startup
if not st.session_state.started:
    num = st.number_input("Enter a decimal number to convert (1–255):", min_value=1, max_value=255, step=1)
    if st.button("Start"):
        st.session_state.number = num
        st.session_state.current = num
        st.session_state.started = True
        st.rerun()

else:
    st.markdown(f"### Converting **{st.session_state.number}** to Binary")

    # Show previous steps
    if st.session_state.steps:
        st.markdown("#### Steps so far:")
        for i, (n, q, r) in enumerate(st.session_state.steps, 1):
            st.markdown(f"### {i}. **{n} / 2 = {q} R {r}**")

    if not st.session_state.completed:
        step_num = len(st.session_state.steps) + 1
        st.markdown(f"### Step {step_num}")

        if not st.session_state.ready_for_remainder:
            user_n = st.number_input("Enter the number to divide by 2:", min_value=0, max_value=255, step=1, key=f"n_{step_num}")
            if user_n != st.session_state.current:
                st.warning(f"⚠️ Please enter the correct number: {st.session_state.current}")
            else:
                st.session_state.ready_for_remainder = True
                st.rerun()
        else:
            current = st.session_state.current
            quotient = current // 2
            correct_r = current % 2

            # Inline division and remainder input
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                st.markdown(f"### {current} / 2 =")
            with col2:
                st.markdown(f"### {quotient} R")
            with col3:
                user_r = st.number_input("", min_value=0, max_value=1, step=1, key=f"r_{step_num}")
            with col4:
                if st.button("✅ Submit Step"):
                    if user_r == correct_r:
                        st.success("✅ Correct!")
                        st.session_state.steps.append((current, quotient, correct_r))
                        st.session_state.binary.insert(0, str(correct_r))
                        st.session_state.current = quotient
                        st.session_state.ready_for_remainder = False
                        if quotient == 0:
                            st.session_state.completed = True
                        st.rerun()
                    else:
                        st.error("❌ Incorrect remainder. Try again.")

    if st.session_state.completed:
        st.markdown("---")
        st.markdown("### ✅ Final Step")
        binary_str = ''.join(st.session_state.binary)
        st.markdown("Now type the complete binary number (from bottom to top):")
        user_binary = st.text_input("Binary Answer")

        if user_binary:
            if user_binary.strip() == binary_str:
                st.balloons()
                st.success(f"🎉 Correct! {st.session_state.number} = **{binary_str}** in binary.")
                st.button("🔁 Try Another Number", on_click=reset)
            else:
                st.error("❌ That’s not the correct binary. Check your remainders again!")
