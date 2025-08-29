import streamlit as st
import qrcode
import io

st.set_page_config(page_title="Binary to Decimal", layout="centered")
st.title("🔢 Binary to Decimal")

# Sidebar with QR code
st.sidebar.header("Scan This QR Code to Access the App")

qr_link = "https://divide-by-2.streamlit.app"  # Replace with your actual URL
qr = qrcode.make(qr_link)
buf = io.BytesIO()
qr.save(buf)
buf.seek(0)

st.sidebar.image(buf, width=300, caption=qr_link)

# Initialize session state
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

def reset():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Get input number
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
        current = st.session_state.current
        st.markdown(f"### Step {len(st.session_state.steps)+1}")

        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            user_n = st.number_input("Enter the number to divide by 2:", min_value=0, max_value=255, step=1, key=f"n_{len(st.session_state.steps)}")
        correct_q = current // 2
        with col2:
            st.markdown(f"### / 2 = {correct_q} R")
        with col3:
            user_r = st.number_input("Enter remainder (0 or 1):", min_value=0, max_value=1, step=1, key=f"r_{len(st.session_state.steps)}")

        if st.button("✅ Check Answer"):
            if user_n != current:
                st.error(f"❌ Incorrect number to divide. You should enter {current}.")
            else:
                correct_r = current % 2
                if user_r == correct_r:
                    st.success("Correct!")
                    st.session_state.steps.append((current, correct_q, correct_r))
                    st.session_state.binary.insert(0, str(correct_r))
                    st.session_state.current = correct_q
                    if correct_q == 0:
                        st.session_state.completed = True
                    st.rerun()
                else:
                    st.error("❌ Incorrect remainder — try again.")

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
