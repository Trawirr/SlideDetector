import cv2
import numpy as np

import os
os.add_dll_directory(r'C:\\Program Files\\VideoLAN\\VLC')
import vlc
from pyzbar.pyzbar import decode
import time

class VlcPlayer:
    def __init__(self) -> None:
        self.cap = cv2.VideoCapture(1)

        self.disp1 = vlc.Instance('--video-x=10', '--video-y=10') # main window
        self.disp2 = vlc.Instance('--video-x=2000', '--video-y=10') # window to the right

        self.media_player1 = self.disp1.media_player_new()
        self.media_player1.toggle_fullscreen()

        self.media_player2 = self.disp2.media_player_new()
        self.media_player2.toggle_fullscreen()

        self.last_time_qr = 0.0

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if frame is None: continue
            # print(len(frame), len(frame[0]))
            # try:
            barcode_data = self.decoder(frame)
            # print("barcodedata:", barcode_data)
            #print(media_player.get_state(), barcode_data)
            if barcode_data:
                print(f"-- QR detected --\nqr: {barcode_data}")
                self.last_time_qr = time.time()
                if barcode_data != self.current_movie:
                    self.play_movies(barcode_data)
                    # media = disp2.media_new(f"/movies/{barcode_data}.mp4")
                    # media_player.set_media(media)
                    # media_player.play()
                    # current_movie = barcode_data

                    #disp1 = vlc.Instance('--directx-device=\\\\.\\DISPLAY1')
                    # media_player = disp1.media_player_new()
                    # media_player.toggle_fullscreen()
                    # media = disp1.media_new(f"/movies/{barcode_data}.mp4")
                    # media_player.set_media(media)
                    # media_player.play()
                    print("end of playing")
            elif self.media_player1.get_state() == vlc.State.Ended or time.time() - self.last_time_qr > 2:
                self.media_player1.stop()
                self.media_player2.stop()
                self.current_movie = ""
                self.last_time_qr = 0.0
            # except Exception as e:
            #     print(f"qr detecting error: {e}\n")

    def decoder(self, image):
        gray_img = cv2.cvtColor(image,0)
        barcode = decode(gray_img)

        for obj in barcode:
            # points = obj.polygon
            # (x,y,w,h) = obj.rect
            # pts = np.array(points, np.int32)
            # pts = pts.reshape((-1, 1, 2))
            # cv2.polylines(image, [pts], True, (0, 255, 0), 3)

            barcodeData = obj.data.decode("utf-8")
            barcodeType = obj.type
            string = "Data " + str(barcodeData) + " | Type " + str(barcodeType)
            
            return barcodeData
        
    def play_movies(self, movie_number):
        print(f"Play: /movies/{movie_number}.mp4")
        media = self.disp1.media_new(f"/movies/{movie_number}.mp4")
        self.media_player1.set_media(media)
        self.media_player1.play()
        
        print(f"Play: /movies/1{movie_number}.mp4")
        media2 = self.disp2.media_new(f"/movies/1{movie_number}.mp4")
        self.media_player2.set_media(media2)
        self.media_player2.play()

        self.current_movie = movie_number
        
    # def play_movie(self, media_player, movie_name):
    #     print(f"Play: /movies/{movie_name}.mp4")
    #     media = disp2.media_new(f"/movies/{movie_name}.mp4")
    #     media_player.set_media(media)
    #     media_player.play()

if __name__ == "__main__":
    while True:
        try:
            print(f"Main loop - starting a new vlcplayer")
            vlc_player = VlcPlayer()
            vlc_player.run()
        except:
            continue

# cap = cv2.VideoCapture(1)

# disp1 = vlc.Instance('--video-x=10', '--video-y=10') # main window
# disp2 = vlc.Instance('--video-x=2000', '--video-y=10', '--play-and-exit') # window to the right

# media_player1 = disp1.media_player_new()
# media_player1.toggle_fullscreen()

# media_player2 = disp2.media_player_new()
# media_player2.toggle_fullscreen()

# current_movie = ""
# last_time_qr = 0.0
# while True:
#     ret, frame = cap.read()
#     if frame is None: continue
#     # print(len(frame), len(frame[0]))
#     try:
#         barcode_data = decoder(frame)
#         print("barcodedata:", barcode_data)
#         #print(media_player.get_state(), barcode_data)
#         if barcode_data:
#             print("-- QR detected --")
#             last_time_qr = time.time()
#             if barcode_data != current_movie:

#                 media = disp2.media_new(f"/movies/{barcode_data}.mp4")
#                 media_player.set_media(media)
#                 media_player.play()
#                 current_movie = barcode_data
#                 #disp1 = vlc.Instance('--directx-device=\\\\.\\DISPLAY1')
#                 # media_player = disp1.media_player_new()
#                 # media_player.toggle_fullscreen()
#                 # media = disp1.media_new(f"/movies/{barcode_data}.mp4")
#                 # media_player.set_media(media)
#                 # media_player.play()
#                 print("end of playing")
#         elif media_player.get_state() == vlc.State.Ended or time.time() - last_time_qr > 2:
#             media_player.stop()
#             current_movie = ""
#             last_time_qr = 0.0
#     except Exception as e:
#         print(f"qr detecting error: {e}\n")
#     try:
#         cv2.imshow('Image', frame)
#     except Exception as e:
#         print(f"imshow error: size: {len(frame), len(frame[0])}, {e}")
#         cap = cv2.VideoCapture(1)
#     code = cv2.waitKey(10)
#     if code == ord('q'):
#         break