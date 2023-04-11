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

try:
    if authenticator.register_user('Register user', preauthorization=True):
        st.success('User registered successfully')
        update_config()
except Exception as e:
        st.error(e)
