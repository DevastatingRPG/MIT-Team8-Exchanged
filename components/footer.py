import streamlit as st

def render_footer():
    footer_html = """
    <style>
    .footer {
        position: relative;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #2C3E50; /* Darker background color */
        color: #ECF0F1; /* Light text color */
        text-align: center;
        padding: 20px 10px; /* Increased padding */
        font-size: 18px; /* Larger font size */
        font-family: 'Verdana', sans-serif; /* Different font */
        z-index: 1000;
    }
    .footer p {
        margin: 0;
    }
    .footer a {
        color: #ECF0F1; /* Consistent link color */
        text-decoration: none;
        margin: 0 15px; /* More space between links */
    }
    .footer a:hover {
        text-decoration: underline; /* Underline on hover */
        color: #3498DB; /* Change color on hover */
    }
    .footer-icons {
        margin-top: 15px; /* Increased spacing above icons */
    }
    .footer-icons img {
        width: 30px; /* Larger icon size */
        height: 30px; /* Larger icon size */
        margin: 0 10px; /* More space between icons */
        transition: transform 0.2s; /* Smooth scale on hover */
    }
    .footer-icons img:hover {
        transform: scale(1.1); /* Scale effect on hover */
    }
    </style>
    <div class="footer">
        <p>© 2024 Developed by Team 8</p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)
    