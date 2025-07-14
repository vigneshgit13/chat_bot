import streamlit as st

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

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
    
for key in ['movie', 'date', 'time', 'tickets', 'seats', 'screen']:
    if key not in st.session_state:
        st.session_state[key] = None

if 'seats' not in st.session_state:
    st.session_state.seats = []

if 'screens' not in st.session_state:
    st.session_state.screens = {
        1: list(range(1, 101)),
        2: list(range(1, 101)),
        3: list(range(1, 101)),
        4: list(range(1, 101)),
    }

# Debugging output to check session state values
st.write(f"Current step: {st.session_state.step}")
st.write(f"Movie: {st.session_state.movie}")
st.write(f"Date: {st.session_state.date}")
st.write(f"Time: {st.session_state.time}")

st.title("🎟️ Cinema Ticket Booking Chatbot")
st.write("Hi! I'm your assistant for booking movie tickets. Let's get started!")

# Step 1: Movie Selection
if st.session_state.step == 1:
    selected = st.selectbox("🎥 Choose a movie", list(movies.keys()))
    if st.button("Next"):
        st.session_state.movie = selected
        st.session_state.screen = movie_to_screen[selected]
        st.session_state.step = 2

# Step 2: Date Selection
elif st.session_state.step == 2:
    # Reset time when changing date
    if st.session_state.date != None and st.session_state.date != st.session_state.get('date', None):
        st.session_state.time = None  # Reset time when date changes

    selected_date = st.date_input("📅 Choose a date", key="date_input", value=None)

    if selected_date:
        if st.session_state.date != selected_date:
            st.session_state.date = selected_date
            st.session_state.time = None  # Reset time on date change
            st.session_state.step = 3  # Proceed to time selection
    else:
        st.warning("Please select a date.")

# Step 3: Time Selection
elif st.session_state.step == 3:
    if st.session_state.movie:
        if st.session_state.time is None:
            st.session_state.time = movies[st.session_state.movie][0]  # Default to first time slot
        
        selected_time = st.selectbox(
            "⏰ Choose a showtime", 
            movies[st.session_state.movie], 
            index=movies[st.session_state.movie].index(st.session_state.time)
        )

        # Debug output to see what time is selected
        st.write(f"Selected time: {selected_time}")

        if st.button("Next"):
            st.session_state.time = selected_time  # Update the time in session state
            st.session_state.step = 4  # Proceed to seat selection
            st.write(f"Updated session time: {st.session_state.time}")
    else:
        st.warning("Please select a movie first.")

# Step 4: Seat and Ticket Selection
elif st.session_state.step == 4:
    available_seats = st.session_state.screens[st.session_state.screen]
    max_tickets = len(available_seats)

    num = st.number_input("🎟️ How many tickets?", min_value=1, max_value=max_tickets, value=1)
    selected_seats = st.multiselect("Choose your seats", options=available_seats, max_selections=num)

    invalid_selection = any(seat not in available_seats for seat in selected_seats)

    if len(selected_seats) == num and not invalid_selection:
        if st.button("Proceed"):
            st.session_state.tickets = num
            st.session_state.seats = selected_seats
            st.session_state.step = 5
    elif invalid_selection:
        st.error("⚠️ One or more selected seats are no longer available. Please re-select.")

# Step 5: Booking Confirmation
elif st.session_state.step == 5:
    for seat in st.session_state.seats or []:
        if seat in st.session_state.screens[st.session_state.screen]:
            st.session_state.screens[st.session_state.screen].remove(seat)

    st.success("✅ Your booking is confirmed!")
    st.markdown(f"""
    **Movie:** {st.session_state.movie}  
    **Date:** {st.session_state.date.strftime('%B %d, %Y')}  
    **Time:** {st.session_state.time}  
    **Screen:** {st.session_state.screen}  
    **Seats:** {', '.join(map(str, st.session_state.seats))}
    """)

    if st.button("Book Another Ticket"):
        # Reset all necessary session states to start a new booking
        for key in ['step', 'movie', 'time', 'tickets', 'seats', 'screen']:
            st.session_state[key] = None
        st.session_state.date = None  # Explicitly reset the date value
        st.session_state.step = 1  # Restart the flow