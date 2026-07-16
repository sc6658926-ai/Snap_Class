from src.screens.database.config import supabase
import bcrypt

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd,hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())


def check_teacher_exist(username):
#check for unique username is already taken
 responce= supabase.table("teachers").select("username").eq("username", username).execute()
 return len(responce.data)> 0

def create_teacher(username,name,password):
    data = { "username": username,"name": name, "password": hash_pass(password) }
    response= supabase.table("teachers").insert(data).execute()
    return response.data

def teacher_login(username,password):
    response = supabase.table("teachers").select("*").eq("username",username).execute()
    if response.data:
     teacher = response.data[0]
      
     if check_pass(password,teacher["password"]):
      return teacher
     return None