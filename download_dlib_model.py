import requests

# URL of the .dat.bz2 file
url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"

# Path to save the downloaded file
output_path = "C:/Users/zeels/PycharmProjects/pythonProject1/models/shape_predictor_68_face_landmarks.dat.bz2"

# Download and save the file
response = requests.get(url)
with open(output_path, "wb") as f:
    f.write(response.content)

print("Download completed!")
