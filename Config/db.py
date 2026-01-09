from mongoengine import connect
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()


connect(
    db=os.getenv("DATABASE_NAME"),
    host=os.getenv("DATABASE_URL")
)
