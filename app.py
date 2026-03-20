import streamlit as st
import pickle
import pandas as pd

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Passenger Satisfaction Predictor",
    page_icon="✈️",
    layout="centered"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
}

.main {
    background-color: #0a0f1e;
    color: #f0f0f0;
}

.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1b3e 50%, #0a1628 100%);
}

/* Header banner */
.hero-banner {
    background: linear-gradient(90deg, #1a3a6e, #0e2a5a);
    border: 1px solid #2a4a8e;
    border-radius: 12px;
    padding: 2rem;
    margin-bottom: 2rem;
    text-align: center;
}

.hero-banner h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #e8f0ff;
    margin: 0;
    letter-spacing: -0.5px;
}

.hero-banner p {
    color: #8aaad4;
    margin-top: 0.5rem;
    font-size: 0.95rem;
}

/* Section headers */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #4a7fcb;
    margin-bottom: 0.8rem;
    margin-top: 1.5rem;
    border-left: 3px solid #4a7fcb;
    padding-left: 10px;
}

/* Result boxes */
.result-satisfied {
    background: linear-gradient(135deg, #0d3d1f, #1a5c2e);
    border: 1px solid #2ecc71;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    text-align: center;
    margin-top: 1.5rem;
}

.result-dissatisfied {
    background: linear-gradient(135deg, #3d0d0d, #5c1a1a);
    border: 1px solid #e74c3c;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    text-align: center;
    margin-top: 1.5rem;
}

.result-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    margin: 0.3rem 0;
}

.result-subtitle {
    font-size: 0.9rem;
    opacity: 0.75;
}

/* Divider */
.divider {
    border: none;
    border-top: 1px solid #1e2d50;
    margin: 1.5rem 0;
}

/* Streamlit widget label overrides */
label {
    color: #c0d0ee !important;
    font-size: 0.88rem !important;
}

.stSlider > div > div {
    background-color: #1e3060 !important;
}

.stSelectbox > div > div {
    background-color: #111d3a !important;
    color: #e0e8ff !important;
    border: 1px solid #2a3f6e !important;
}

.stNumberInput > div > div > input {
    background-color: #111d3a !important;
    color: #e0e8ff !important;
    border: 1px solid #2a3f6e !important;
}

/* Predict button */
.stButton > button {
    background: linear-gradient(90deg, #1a56c4, #2a7bd4);
    color: white;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 1px;
    border: none;
    border-radius: 8px;
    padding: 0.65rem 2.5rem;
    width: 100%;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #2266d4, #3a8be4);
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(42, 123, 212, 0.4);
}
</style>
""", unsafe_allow_html=True)

# ── Load model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    with open('best_model.pkl', 'rb') as f:
        return pickle.load(f)

model = load_model()

# ── Hero banner ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <h1>✈️ Passenger Satisfaction Predictor</h1>
    <p>Fill in the passenger details below to predict their satisfaction level</p>
</div>
""", unsafe_allow_html=True)

# ── Passenger Profile ─────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Passenger Profile</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("Gender", ["Female", "Male"])
    customer_type = st.selectbox("Customer Type", ["Loyal Customer", "Disloyal Customer"])
with col2:
    type_of_travel = st.selectbox("Type of Travel", ["Personal Travel", "Business Travel"])
    travel_class = st.selectbox("Class", ["Eco", "Eco Plus", "Business"])

col3, col4 = st.columns(2)
with col3:
    age = st.slider("Age", 1, 100, 30)
with col4:
    flight_distance = st.number_input("Flight Distance (miles)", min_value=0, value=500)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Delay Info ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Flight Delays</div>', unsafe_allow_html=True)

col5, col6 = st.columns(2)
with col5:
    departure_delay = st.number_input("Departure Delay (minutes)", min_value=0, value=0)
with col6:
    arrival_delay = st.number_input("Arrival Delay (minutes)", min_value=0, value=0)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Service Ratings ───────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Service Ratings  (0 = Not Applicable, 1–5 scale)</div>', unsafe_allow_html=True)

col7, col8 = st.columns(2)
with col7:
    wifi             = st.slider("Inflight Wifi Service", 0, 5, 3)
    online_booking   = st.slider("Ease of Online Booking", 0, 5, 3)
    gate_location    = st.slider("Gate Location", 0, 5, 3)
    food_drink       = st.slider("Food and Drink", 0, 5, 3)
    online_boarding  = st.slider("Online Boarding", 0, 5, 3)
    seat_comfort     = st.slider("Seat Comfort", 0, 5, 3)
with col8:
    entertainment    = st.slider("Inflight Entertainment", 0, 5, 3)
    onboard_service  = st.slider("On-board Service", 0, 5, 3)
    leg_room         = st.slider("Leg Room Service", 0, 5, 3)
    baggage          = st.slider("Baggage Handling", 0, 5, 3)
    checkin          = st.slider("Check-in Service", 0, 5, 3)
    online_support   = st.slider("Online Support", 0, 5, 3)
    cleanliness      = st.slider("Cleanliness", 0, 5, 3)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Predict ───────────────────────────────────────────────────────────────────
if st.button("PREDICT SATISFACTION"):

    # Build input in exact column order the model was trained on
    input_data = {
        'age':                                  age,
        'flight_distance':                      flight_distance,
        'seat_comfort':                         seat_comfort,
        'departure/arrival_time_convenient':    0,
        'food_and_drink':                       food_drink,
        'gate_location':                        gate_location,
        'inflight_wifi_service':                wifi,
        'inflight_entertainment':               entertainment,
        'online_support':                       online_support,
        'ease_of_online_booking':               online_booking,
        'on-board_service':                     onboard_service,
        'leg_room_service':                     leg_room,
        'baggage_handling':                     baggage,
        'checkin_service':                      checkin,
        'cleanliness':                          cleanliness,
        'online_boarding':                      online_boarding,
        'departure_delay_in_minutes':           departure_delay,
        'arrival_delay_in_minutes':             arrival_delay,
        'gender_male':                          1 if gender == 'Male' else 0,
        'customer_type_loyal customer':         1 if customer_type == 'Loyal Customer' else 0,
        'type_of_travel_personal travel':       1 if type_of_travel == 'Personal Travel' else 0,
        'class_eco':                            1 if travel_class == 'Eco' else 0,
        'class_eco plus':                       1 if travel_class == 'Eco Plus' else 0,
    }

    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)[0]

    if prediction == 1:
        st.markdown("""
        <div class="result-satisfied">
            <div style="font-size:2.5rem;">😊</div>
            <div class="result-title" style="color:#2ecc71;">SATISFIED</div>
            <div class="result-subtitle" style="color:#a8e6c3;">
                This passenger is likely to be satisfied with their experience.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="result-dissatisfied">
            <div style="font-size:2.5rem;">😞</div>
            <div class="result-title" style="color:#e74c3c;">NOT SATISFIED</div>
            <div class="result-subtitle" style="color:#f0a8a8;">
                This passenger is likely neutral or dissatisfied with their experience.
            </div>
        </div>
        """, unsafe_allow_html=True)
