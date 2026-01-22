import streamlit as st 

def card(title,content):
    st.markdown(
        f"""
        <div class="card">
        <div class="title">{title}</div>
        <br>
        {content}
        </div>
        """,
        unsafe_allow_html=True
    )

def skill_list(skills):
    if not skills:
        return "<p>None</p>"
    return "<ul>" + "".join(f"<li>{skill}</li>" for skill in skills) + "</ul>"
 