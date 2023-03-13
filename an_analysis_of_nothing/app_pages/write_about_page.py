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
    st.markdown("""<h2 style='text-align: center; color: #031B28;'>
                About Us<br></h2>""",
                unsafe_allow_html=True)

    st.markdown("""<h5 style='text-align: center; color: white;'><br>
                For DATA515 Software Design for Data Scientists
                course at the University of Washington, we created a
                web application for Seinfeld fans to explore
                and query dialogue snippets, identify correlations between
                character appearances and audience ratings, and chronicle
                appearances of various characters across the series.
                <br><br></h5>""",
                unsafe_allow_html=True)

    left_2, middle_2, right_2 = st.columns([1, 0.09, 1])
    with left_2:
        st.image('./static/images/kramer_.jpg', width=314)
        st.markdown("""<h5 style='text-align: center; color: #031B28;'>
                Yash Manne<br>
                <p style='color: white;'>Project Manager<p></h5>""",
                unsafe_allow_html=True)
    with right_2:
        st.image('./static/images/elaine_.jpg', width=326)
        st.markdown("""<h5 style='text-align: center; color: #031B28;'>
                Aditi Shrivastava<br>
                <p style='color: white;'>Developer<p></h5>""",
                unsafe_allow_html=True)
    with middle_2:
        pass

    left_3, middle_3, right_3 = st.columns([1, 0.069, 1])
    with left_3:
        st.image('./static/images/newman_.jpg', width=314)
        st.markdown("""<h5 style='text-align: center; color: #031B28;'>
                Yamina Katariya<br>
                <p style='color: white;'>UX Designer<p></h5>""",
                unsafe_allow_html=True)
    with right_3:
        st.image('./static/images/george_.jpg', width=330)
        st.markdown("""<h5 style='text-align: center; color: #031B28;'>
                Chandler Ault<br>
                <p style='color: white;'>Quality Assurance<p></h5>""",
                unsafe_allow_html=True)
    with middle_3:
        pass
