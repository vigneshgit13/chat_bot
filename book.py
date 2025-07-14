import streamlit as st
import datetime

# Page Configuration
st.set_page_config(page_title="Cinema Ticket Booking Bot", page_icon="🎬")

# Movie data
movies = {
    "Avatar 2": ["12:00 PM", "3:00 PM", "6:00 PM", "9:00 PM"],
    "The Flash": ["12:00 PM", "3:00 PM", "6:00 PM", "9:00 PM"],
    "Mission Impossible": ["12:00 PM", "3:00 PM", "6:00 PM", "9:00 PM"],
    "Spiderman: No Way Home": ["12:00 PM", "3:00 PM", "6:00 PM", "9:00 PM"]
}

movie_to_screen = {
    "Avatar 2": 1,
    "The Flash": 2,
    "Mission Impossible": 3,
    "Spiderman: No Way Home": 4
}

# Session State Initialization
if 'step' not in st.session_state:
    st.session_state.step = 1

for key in ['movie', 'date', 'time', 'tickets', 'seats', 'screen']:
    if key not in st.session_state:
        st.session_state[key] = None

if 'seats' not in st.session_state or st.session_state.seats is None:
    st.session_state.seats = []

if 'screens' not in st.session_state:
    st.session_state.screens = {
        1: list(range(1, 101)),
        2: list(range(1, 101)),
        3: list(range(1, 101)),
        4: list(range(1, 101)),
    }

# Step 1: Movie Selection
if st.session_state.step == 1:
    st.title("🎟️ Cinema Ticket Booking Chatbot")
    st.write("Hi! I'm your assistant for booking movie tickets. Let's get started!")
    
    selected = st.selectbox("🎥 Choose a movie", list(movies.keys()))
    
    if st.button("Next to Date"):
        st.session_state.movie = selected
        st.session_state.screen = movie_to_screen[selected]
        st.session_state.step = 2

# Step 2: Date Selection (100% Working)
elif st.session_state.step == 2:
    st.title("📅 Select a Date")

    min_date = datetime.date.today()
    max_date = min_date + datetime.timedelta(days=10)

    # Use a temp key to hold selection until "Next" is clicked
    if 'temp_date' not in st.session_state:
        st.session_state.temp_date = st.session_state.date or min_date

    st.session_state.temp_date = st.date_input(
        "Choose a date",
        value=st.session_state.temp_date,
        min_value=min_date,
        max_value=max_date,
        key="date_input_key"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back to Movie"):
            st.session_state.step = 1
    with col2:
        if st.button("Next to Time"):
            st.session_state.date = st.session_state.temp_date
            st.session_state.step = 3

    st.write(f"✅ Selected date: {st.session_state.temp_date.strftime('%B %d, %Y')}")

# Step 3: Time Selection
elif st.session_state.step == 3:
    st.title("⏰ Select Showtime")
    if st.session_state.movie:
        if st.session_state.time is None:
            st.session_state.time = movies[st.session_state.movie][0]

        selected_time = st.selectbox(
            "Choose a showtime", 
            movies[st.session_state.movie], 
            index=movies[st.session_state.movie].index(st.session_state.time)
        )

        st.write(f"Selected time: {selected_time}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Back to Date"):
                st.session_state.step = 2
        with col2:
            if st.button("Next to Seats"):
                st.session_state.time = selected_time
                st.session_state.step = 4
    else:
        st.warning("Please select a movie first.")

# Step 4: Seat and Ticket Selection
elif st.session_state.step == 4:
    st.title("🎟️ Select Your Seats")

    available_seats = st.session_state.screens[st.session_state.screen]
    max_tickets = len(available_seats)

    num = st.number_input("How many tickets?", min_value=1, max_value=max_tickets, value=1)
    selected_seats = st.multiselect("Choose your seats", options=available_seats, max_selections=num)

    invalid_selection = any(seat not in available_seats for seat in selected_seats)

    if len(selected_seats) == num and not invalid_selection:
        if st.button("✅ Confirm Booking"):
            st.session_state.tickets = num
            st.session_state.seats = selected_seats
            st.session_state.step = 5

    if st.button("⬅️ Back to Time"):
        st.session_state.step = 3

    if invalid_selection:
        st.error("⚠️ One or more selected seats are no longer available. Please re-select.")

# Step 5: Booking Confirmation
elif st.session_state.step == 5:
    st.title("✅ Booking Confirmed!")

    for seat in st.session_state.seats or []:
        if seat in st.session_state.screens[st.session_state.screen]:
            st.session_state.screens[st.session_state.screen].remove(seat)

    st.success("Your booking is confirmed!")
    st.balloons()

    st.markdown(f"""
    **Movie:** {st.session_state.movie}  
    **Date:** {st.session_state.date.strftime('%B %d, %Y')}  
    **Time:** {st.session_state.time}  
    **Screen:** {st.session_state.screen}  
    **Seats:** {', '.join(map(str, st.session_state.seats))}
    """)

    if st.button("🎬 Book Another Ticket"):
        for key in ['movie', 'date', 'time', 'tickets', 'screen']:
            st.session_state[key] = None
        st.session_state.seats = []
        st.session_state.step = 1
