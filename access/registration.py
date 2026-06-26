import requests
import json

BASE_URL = "http://4.224.186.213/evaluation-service"
REGISTRATION_URL = f"{BASE_URL}/register"
AUTH_URL = f"{BASE_URL}/auth"

# TODO: Replace these placeholder values with YOUR real information
MY_DETAILS = {
    "companyName": "AffordMed", #  company name
    "ownerName": "Raunak Pandey", 
    "rollNo": "2301921520147", 
    "ownerEmail": "csai23067@glbitm.ac.in",
    "accessCode": "xxkJnk"
}

# Values required by the specific API block provided in the image
REGISTRATION_PAYLOAD = {
    "email": "csai23067@glbitm.ac.in",       
    "name": "Raunak Pandey",
    "mobileNo": "8303609789",
    "githubUsername": "Raunak08-code",    
    "rollNo": "2301921520147",
    "accessCode": "xxkJnk" 
}

def register_and_authenticate():
    # ---- STEP 1: REGISTRATION ----
    print("Sending registration request...")
    try:
        reg_response = requests.post(
            REGISTRATION_URL, 
            json=REGISTRATION_PAYLOAD, 
            headers={"Content-Type": "application/json"}
        )
        
        if reg_response.status_code in [200, 201]:
            reg_data = reg_response.json()
            print("\n✅ Registration Successful!")
            print("========================================")
            print(f"Client ID:     {reg_data.get('clientID')}")
            print(f"Client Secret: {reg_data.get('clientSecret')}")
            print("========================================")
            print("⚠️ SAVE THESE CREDENTIALS! You cannot retrieve them again.\n")
            
            client_id = reg_data.get('clientID')
            client_secret = reg_data.get('clientSecret')
            
        else:
            print(f"❌ Registration Failed (Status Code: {reg_response.status_code})")
            print(reg_response.text)
            return

    except Exception as e:
        print(f"An error occurred during registration: {e}")
        return

    # ---- STEP 2: AUTHENTICATION ----
    print("Attempting to get Authorization Token...")
    
    # Building the payload exactly like Image 3
    auth_payload = {
        "email": REGISTRATION_PAYLOAD["email"],
        "name": REGISTRATION_PAYLOAD["name"],
        "rollNo": REGISTRATION_PAYLOAD["rollNo"],
        "accessCode": REGISTRATION_PAYLOAD["accessCode"],
        "clientID": client_id,
        "clientSecret": client_secret
    }
    
    try:
        auth_response = requests.post(
            AUTH_URL, 
            json=auth_payload, 
            headers={"Content-Type": "application/json"}
        )
        
        if auth_response.status_code == 200:
            auth_data = auth_response.json()
            print("✅ Authentication Successful!")
            print(f"Token Type:  {auth_data.get('token_type')}")
            print(f"Access Token: {auth_data.get('access_token')}")
            print(f"Expires In:   {auth_data.get('expires_in')}")
        else:
            print(f"❌ Authentication Failed (Status Code: {auth_response.status_code})")
            print(auth_response.text)
            
    except Exception as e:
        print(f"An error occurred during authentication: {e}")

if __name__ == "__main__":
    register_and_authenticate()