import cv2
import os
import numpy as np
#TRAINING
folder_name = 'faces data' 
images = os.listdir(folder_name)                                    # list semua path data wajah pada folder train data

face_cascade_file = 'Cascade Classifier/face-detect.xml'
face_cascade = cv2.CascadeClassifier(face_cascade_file)            # Load cascade classifiernya
recognizer = cv2.face.LBPHFaceRecognizer_create()                    # Create recognizer object
# recognizer = cv2.reco


image_arrays = []                                                   # Containes semua array data wajah
image_ids = []                                                      # Container semua ID data wajah
for image_path in images:                                           # Looping semua path data wajah
    splitted_path = image_path.split('.')
    print(splitted_path)
    image_id = int(splitted_path[1])                                # Ambil ID data wajah
    
    image = cv2.imread(os.path.join(folder_name, image_path))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    image_array = np.array(image, 'uint8')                          # Ambil array data wajah
    
    image_arrays.append(image_array)                                # Store array data wajah ke list/container
    image_ids.append(image_id)                                      # Store ID data wajah ke list/container


recognizer.train(image_arrays, np.array(image_ids))                 # Train recognizer
recognizer.save('recognizer/faces_data.yml')                        # Save model recognizer 
print('[INFO] TRAIN RECOGNIZER SUCCESS!')

#TESTING
recognizer.read('recognizer/faces_data.yml')                        # Load recognizer      
font = cv2.FONT_HERSHEY_SIMPLEX                                     # Specify jenis font dari OpenCV

known_names = ['Iqbal Maulana']                                     # List untuk nama yang ada di model

cam = cv2.VideoCapture(0)                                           # Akses Kamera
while True:
    ret, frame = cam.read()                                         # Membaca setiap frame dari stream kamera 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                  # Mengubah mode BGR ke GRAY (hitam putih)
    
                                                                    # Proses pencarian wajah 
    faces = face_cascade.detectMultiScale(gray, 1.3, 3)             # <cascade_file>.detectMultiScale(<frame>, <scale_factor>, <min_neighbors>)
    for x, y, w, h in faces:                                        # Looping semua wajah yang terdeteksi
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)    # Gambar box untuk setiap wajah
        
        roi_gray = gray[y:y+h, x:x+w]
        ids, dist = recognizer.predict(roi_gray)                     # Prediksi wajah siapoa
        cv2.putText(frame, f'{known_names[ids-1]} {round(dist, 2)}', 
                    (x-20, y-20), font, 1 ,(255, 255, 0), 3)         # Menaruh text pada frame

    
    cv2.imshow('Face Recognition Video', frame)                     # Jendela untuk menampilkan hasil
    
    if cv2.waitKey(1) & 0xff == ord('x'):                           # Exit dengan tombol x
        break

cam.release()                                                       # Menyudahi akses kamera
cv2.destroyAllWindows()                                             # Menutup jendela
