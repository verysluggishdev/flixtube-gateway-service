from passlib.context import CryptContext
from datetime import datetime
from PIL import Image
from moviepy.video.io.VideoFileClip import VideoFileClip
import base64
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def generate_unique_file_name(filename):
    current_time = str(datetime.now())
    unique_file_name = f"{filename}@{current_time}"
    return base64.b64encode(unique_file_name.encode()).decode()

def generate_video_thumbnail(input_video_path, output_thumbnail_path):
    # Open the video file
    clip = VideoFileClip(input_video_path)

    # Get the duration of the video
    duration = clip.duration

    # Calculate the time point for the middle of the video
    middle_time_point = duration / 2

    # Capture the frame at the middle time point
    frame = clip.get_frame(middle_time_point)

    # Convert the frame to a PIL Image
    pil_image = Image.fromarray(frame)

    # Save the thumbnail
    pil_image.save(output_thumbnail_path, "JPEG")

    # Close the video clip
    clip.close()

def handleVideoUpload(video):

    try:
        
        if not os.path.exists('../uploads'):
            os.mkdir('../uploads')
        
        video_data = video.file.read()
        video_file_name = generate_unique_file_name(video.filename)

        
        try:
            extension = video.filename.split('.')[-1]
        except IndexError:
            extension = ""
        
        video_upload_path = f'../uploads/{video_file_name}.{extension}'
        
        with open(video_upload_path, 'wb') as f:
            f.write(video_data)
        
        thumbnail_file_name = generate_unique_file_name(f'thumbnail_{video.filename}.jpeg')
        
        thumbnail_upload_path = f'../uploads/{thumbnail_file_name}.jpeg'

        generate_video_thumbnail(video_upload_path, thumbnail_upload_path)


    except Exception as e:
        print(e)
        return {"message": "There was an error uploading the file"}
    
    finally:
        video.file.close()
    
    return f'{video_file_name}.{extension}', f'{thumbnail_file_name}.jpeg'

