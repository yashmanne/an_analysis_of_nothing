"""
This script contains the contents of the About Us page
and is called by the main app.py script.

This script requires that Streamit is installed.
"""

import streamlit as st

def main():
    """
    This function executes the Streamlit formatted HTML
    displayed on the About Us webpage.

    Arguments: None
    Returns: None
    """
    st.markdown("""<h2 style='text-align: center; color: white;'>
                About Us<br></h2>""",
                unsafe_allow_html=True)

    st.markdown("""<h5 style='text-align: center; color: white;'><br>
                For DATA515 Software Design for Data Scientists
                course at the University of Washington, we created a
                web application for Seinfeld fans to explore
                and query dialogue snippets, identify correlations between
                character appearances and audience ratings, and chronicle
                appearances of various characters across the series.</h5>""",
                unsafe_allow_html=True)

    st.markdown("""<h3 style='text-align: left; color: white;'><br>
                Creators:</h3>""",
                unsafe_allow_html=True)

    left_2, right_2 = st.columns(2)
    with left_2:
        st.image('./static/images/kramer_.jpg', width=314)
        st.markdown("""<h6 style='text-align: center; color: white;'>
                Yash Manne<br>
                Project Manager</h6>""",
                unsafe_allow_html=True)
    with right_2:
        st.image('./static/images/elaine_.jpg', width=345)
        st.markdown("""<h6 style='text-align: center; color: white;'>
                Aditi Shrivastava<br>
                Developer<br><br></h6>""",
                unsafe_allow_html=True)

    left_3, right_3 = st.columns(2)
    with left_3:
        st.image('./static/images/newman_.jpg', width=314)
        st.markdown("""<h6 style='text-align: center; color: white;'>
                Yamina Katariya<br>
                UX Designer<br><br></h6>""",
                unsafe_allow_html=True)
    with right_3:
        st.image('./static/images/george_.jpg', width=345)
        st.markdown("""<h6 style='text-align: center; color: white;'>
                Chandler Audlt<br>
                Quality Assurance<br><br></h6>""",
                unsafe_allow_html=True)
