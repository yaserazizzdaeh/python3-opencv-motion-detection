"""
File Description--------------------------------------------------   ------------ --        --     --------------
Project Name: Motion Detection (PYTHON EYE)----------------------   -----------    --      --     -------------
Date: 2020-03-30------------------------------------------------   --               --    --     --
By: Yaser Azizzadeh Shah Tapeh---------------------------------   ------             --  --     ------
E_mail: yas.0110.az@gmail.com---------------------------------   ------               ----     ------
Phone: +98 914 868 69 80-------------------------------------   --                     --     --
University: TVU of West Azarbayjan-Urmia--------------------   ------------            --    ------------
-----------------------------------------------------------   --------------           --   --------------
"""
import cv2
import numpy as np
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

kernel = np.ones((3, 3), np.uint8)

message = MIMEMultipart()   # create message object
# message parameters setup
password = "motiondetection"                    #your email pass
message['From'] = "mail@gmail.com"              #email address as mail sender
message['To'] = "mail@gmail.com"                #email address to send capture
message['Subject'] = "Motion Detection Frame"

try:
    # create server
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    # login to gmail accuont
    server.login(message['From'], password)
except:
    print("Error: Can not connect to server!")

def main():                     # main function
    
    cap = cv2.VideoCapture(0)   # define cap object for start live stream video with cv2.VideoCapture(has one argument for select input)

    cap.set(3, 640)  # set frame width on 800 px  / defult on 640 px
    cap.set(4, 480)  # set frame height on 600 px / defult on 480 px
    check, frame1 = cap.read()     # frame cpture
    check, frame2 = cap.read()     # frame cpture
    
    while cap.isOpened():                                       # Infinite loop / if check is True
        
        d = cv2.absdiff(frame1, frame2)              # abslute diffrence between frame1 & frame2
        
        grey = cv2.cvtColor(d, cv2.COLOR_BGR2GRAY)   # color scale convert from BGR to Gray
        
        blur = cv2.GaussianBlur(grey, (5, 5), 0)     # apply blur filter on gray frame for removing noise /frame ,kernel dimension,deviation sigmaX equal sigmaY
        
        limit, th = cv2.threshold( blur, 20, 255, cv2.THRESH_BINARY)    # (only gray scale),limit=20(treshold limit),treshold max value,treshold mode
    
        dilated = cv2.dilate(th, kernel, iterations=1 ) # image expand///frame,kernel,repeat 
        
        eroded = cv2.erode(dilated, kernel, iterations=1 )   # image Erosion ///frame,kernel,repeat
        
        image, contours, hierarchy = cv2.findContours(eroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)   # find contours //frame,mode,methode

        cv2.drawContours(frame1, contours, -1, (23, 88, 195), 2)       # frame,python list of contours, drow all contour point, drow color,drow line thickness

        
        cv2.imshow("Motion Detection", frame1)      # frame show
    
        if cv2.waitKey(1) & 0xFF == ord('q'):  # exit on 'q'
            break
        
        frame1 = frame2            # replace frame2 on frame1////now, refrence frame1 is frame2
        ret, frame2 = cap.read()   # capture new frame and put on frame2

        if len(contours) > 150:
            
            date = str(datetime.datetime.now())  # date & time now
            
            print(date,"\n","motion detected successfully", len(contours))
            
            cv2.putText(frame1, date, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (23, 88, 195), 2, cv2.LINE_AA)
            cv2.imwrite("motion.jpg",frame1)
            try:
                message.attach(MIMEImage(open("motion.jpg", 'rb').read()))
                server.sendmail(message['From'], message['To'], message.as_string())
                print("----mail sent successfully----")
            except:
                pass


    try:
        server.quit()        # quite from server
    except NameError:
        pass
    
    cap.release()                  # release capturing     
    cv2.destroyAllWindows()        # destroy all windows
    
    
if __name__ == "__main__":
    main()
