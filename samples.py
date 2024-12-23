import streamlit as st

name = "Alice"
age = 30

multiline_string = f"""
Hello, my name is {name}.
I am {age} years old.
I love Python programming!
"""

st.write(multiline_string)
st.text(multiline_string)
st.markdown(multiline_string)


with st.container():
    st.header("Section 1")
    st.write("This is some content.")