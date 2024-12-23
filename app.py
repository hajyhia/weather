import streamlit as st

def main():
    # Access secrets
    # api_key = st.secrets["general"]["api_key"]
    # db_username = st.secrets["general"]["db_username"]
    # db_password = st.secrets["general"]["db_password"]
    #
    # # Example usage
    # st.write(f"API Key: {api_key}")

    # Set the title of the app
    st.title("Welcome to My Streamlit App")

    # Add a subtitle or description
    st.subheader("This is a simple interactive app built with Streamlit.")

    # Get user input for name
    name = st.text_input("What's your name?", placeholder="Enter your name here")

    # Get user input for age
    age = st.number_input("How old are you?", min_value=0, max_value=120, value=25)

    # Add a button
    if st.button("Submit"):
        # Display a personalized message
        if name:
            st.success(f"Hello, {name}! You are {age} years old.")
        else:
            st.warning("Please enter your name to see the message!")

    # Add an additional feature
    st.sidebar.title("About This App")
    st.sidebar.info(
        "This is a demo application built with Streamlit to showcase its interactive capabilities. "
        "Streamlit makes it easy to create web apps for machine learning and data science projects."
    )

if __name__ == "__main__":
    main()
