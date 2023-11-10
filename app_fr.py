import streamlit as st
import time
from PIL import Image

from streamlit_option_menu import option_menu
import pandas as pd
# Import the following modules
from pushbullet import PushBullet
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
import time
import cv2
import face_recognition
# archimage = Image.open('/mount/src/smartcampus/Architechture_Face_Recog.jpg')
# smartcampusimage = Image.open('/mount/src/smartcampus/SmartCampus.jpg')

with st.sidebar:
    
    selected = option_menu('Smart Campus Surveillance Module',
                          
                          ['About Project',
                           'Project Contributors',
                           'Architecture Diagram',
                           'Face Recognition'
                            ],
                          icons=['activity','activity','activity','activity'],
                          default_index=0)

if (selected == 'About Project'):
    # page title
    st.title('Smart Campus Surveillance & Guidance System')
    st.markdown('Aim of the project is to build a machine learning based Smart Campus Surveillance model which checks whether students are attending \
        the lectures or bunking the lectures based on the camera feed received from the camera installed in the campus. It will send a alert notification to respective HOD or Class Teacher about the bunks done by student')
    #st.image(smartcampusimage, caption='')
  

if (selected == 'Project Contributors'):
    st.title("1. Sanjana Marode")
    st.title("2. Hritika Belekar")
    st.title("3. Pallavi Kurve")

if (selected == 'Architecture Diagram'):
    #st.image(archimage, caption='Architecture Diagram for Face Recognition Module')
    # st.markdown("Architecture Diagram of the Entire Project")
    pass



import pandas as pd
from datetime import datetime, time
from pushbullet import PushBullet

def check_db_trigger():
    path_ = '/mount/src/smartcampus/Attendance.csv'

    data_set = pd.read_csv(path_)

    for index, row in data_set.iterrows():
        # Define the start and end timestamps for each row
        start_time = time(row['Start_Time'], 0)
        end_time = time(row['End_Time'], 0)

        # Create a datetime object for the current time
        current_time = time(datetime.now().hour, datetime.now().minute)

        # print('Current Time:', current_time)

        # Check if the current_time lies between start_time and end_time
        if start_time <= current_time <= end_time:
            access_token = 'o.LK4aelu6Qp5j7GN97Czoh0XCfOOdEu6P'
            data = 'Bunk'
            pb = PushBullet(access_token)
            push = pb.push_note(data, row['Student'] + ' is bunking the ' + row['Lecture'] + ' Lecture')
            # print('API Triggered')
        break  # This will exit the loop once the API is triggered

    print('Loop finished without triggering the API')

def identify_face():
    student_name='Hrtika Belekar'

    # Open the input movie file

    ##HRITIKA
    input_movie = cv2.VideoCapture("/mount/src/smartcampus/VID20231107160512_short2.mp4")
    length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create an output movie file (make sure resolution/frame rate matches input video!)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_movie = cv2.VideoWriter(student_name+'_output.avi', fourcc, 29.97, (640, 360))

    ## HRITIKA
    student_image = face_recognition.load_image_file("/mount/src/smartcampus/IMG20231106170435.jpg")

    student_face_encoding = face_recognition.face_encodings(student_image)[0]

    known_faces = [
        student_face_encoding
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    frame_number = 0
    # student_name=''
    while True:
        # Grab a single frame of video
        ret, frame = input_movie.read()
        frame_number += 1

        if not ret:
            break

        rgb_small_frame = np.ascontiguousarray(frame[:, :, ::-1])
        face_locations = face_recognition.face_locations(rgb_small_frame)
        print('face_locations',face_locations)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.50)
    #         print('match',match)

            name = None
            
            if match[0]:
                name = student_name
                face_names.append(name)
                check_db_trigger()
    #             print('status',status)
    #         if status==200:
    #             break
    #         else:
    #             continue

        # Label the results
        try:
            for (top, right, bottom, left), name in zip(face_locations, face_names):

                if not name:
                    continue
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
    #             print('*')
                cv2.imwrite(student_name+'_1.jpg', frame)
        except Exceptipn as e:
            print(e)
                # Write the resulting image to the output video file
        print("Writing frame {} / {}".format(frame_number, length))
        output_movie.write(frame)

        # Display the resulting image
    # cv2.imshow('Video', frame)
    # cv2.waitKey(0) 
    # All done!
    input_movie.release()
    cv2.destroyAllWindows()
    # page title
# Heart Disease Prediction Page
if (selected == 'Face Recognition'):

# Set a title for your app
    st.title('Smart Campus Surveillance & Guidance System')

    st.title("Upload Video File")

    # Create a file uploader widget
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "csv", "pdf", "jpg", "png","mp4","avi"])

    if st.button("Run Face Recognition Module"):
        # Display a spinner while some processing is happening
        # with st.spinner("Model Processing..."):
            # Simulate some time-consuming task (e.g., sleep for a few seconds)
            # time.sleep(3)
        identify_face()
# Remove the spinner after the task is done



# Call the function
# check_db_trigger()


