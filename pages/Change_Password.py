# Imports
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

def update_config():
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)    

with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"]
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    try:
        if authenticator.reset_password(username, 'Change password'):
            st.success('Password modified successfully')
            update_config()
    except Exception as e:
        st.error(e)

elif authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")




    