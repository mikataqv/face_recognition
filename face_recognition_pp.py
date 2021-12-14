import face_recognition
import cv2
import numpy as np
import os
import glob
faces_encodings = []
faces_names = []
cur_direc = os.getcwd()
path = os.path.join(cur_direc, 'faces/')
list_of_files = [f for f in glob.glob(path+'*.jpg')]
number_files = len(list_of_files)
names = list_of_files.copy()
for i in range(number_files):
    globals()['image_{}'.format(i)] = face_recognition.load_image_file(list_of_files[i])
    globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]
    faces_encodings.append(globals()['image_encoding_{}'.format(i)])
# Create array of known names
    names[i] = names[i].replace(cur_direc, "")  
    faces_names.append(names[i])

    
    
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

video_capture = cv2.VideoCapture(0)
while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    if process_this_frame:
        #Oncherche ou sont les visages
        face_locations = face_recognition.face_locations( rgb_small_frame,3,"hog")
        face_encodings = face_recognition.face_encodings( rgb_small_frame, face_locations)
        
        face_names = []
        for face_encoding in face_encodings:
            #compare une liste d'images encondés de référence et une liste d'images actuelles
            matches = face_recognition.compare_faces (faces_encodings, face_encoding)
            #par défaut
            name = "Unknown"
            #calcul de la distance euclidienne qui montre le niveau de similitudes entre des images de ref et une autre image
            face_distances = face_recognition.face_distance( faces_encodings, face_encoding)
            #on cherche parmis la dataset de reférence l'image qui correspond le plus en fct de la distance euclidienne
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = faces_names[best_match_index]
    
            
            face_names.append(name)
    process_this_frame = not process_this_frame
        # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        if("mich" in name):
            name="michael"
        elif("jerry" in name):
            name="jerry"
        elif("maud" in name):
            name="maud"
        elif("than" in name):
            name="thanushan"
        elif("thom" in name):
            name="thomas"
        elif("suho" in name):
            name="suho"
        elif("alex" in name):
            name="Alexandre"
        elif("rayan" in name):
            name="Rayan"
        else:
            name="error"
            
        if(name=="error"):
            frame_temp=frame.copy()
            actual_frame=frame.copy()
            print("top "+str(top)+"left "+str(left) + "right "+str(right) +"bottom "+ str(bottom)+"taille image "+str(actual_frame))
            cropped_pic=frame_temp[top-right:top+right,left-bottom:left+bottom]
            # Draw a rectangle around the face
            cv2.rectangle(frame_temp, (left, top), (right, bottom), (0, 255, 0), 2)
            # Input text label with a name below the face
            cv2.rectangle(frame_temp, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame_temp, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            validation = False
            print("Press y to save this picture or any other letter to continue")
            while(validation ==False ):
                cv2.imshow('img1',frame_temp) #display the captured image


                if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
                    cv2.imwrite('ERROR.png',cropped_pic)
                    cv2.imshow('machin_cropped', cropped_pic)
                    validation = True
                    cv2.destroyWindow('img1')
    
                elif cv2.waitKey(1) & 0xFF == ord('n'):
                    validation =True
                    cv2.destroyWindow('img1')
                else:
                    validation= False
        else:
            
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # Input text label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            validation = False

        
    
       # Display the resulting image
        cv2.imshow('Video', frame)
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break