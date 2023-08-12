# ctrl + shift + P

# Python: select interpreter 
import cv2

cap = cv2.VideoCapture(0)

def find_red_mask(frame):

    # красный - ORANGE 
    clr_low_ro = (0, 20, 20)
    clr_high_ro = (15, 255, 255)
    # красный - purpur
    clr_low_rp  = (150, 20, 20)
    clr_high_rp= (180, 255, 255)
    
    mask_ro = cv2.inRange(frame_hsv, clr_low_ro, clr_high_ro)
    mask_rp = cv2.inRange(frame_hsv, clr_low_rp, clr_high_rp)
    mask_ro[mask_rp==255] = mask_rp[mask_rp==255]
    return mask_ro

def find_yellow_mask(frame):
    clr_low  = (10, 30, 40)
    clr_high = (45, 255, 255)
    mask_yellow = cv2.inRange(frame_hsv, clr_low, clr_high)
    return mask_yellow

def max_hue(masks, colors, default=None):
    biggest_conts_area = []
    biggest_conts_area_dict = {} 
    for mask, color in zip(masks, colors):
       
        cont, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cont = sorted( cont, key=cv2.contourArea, reverse=True)
        try:
            biggest_conts_area.append(  cv2.contourArea(cont[0] ) )
        except IndexError:
            biggest_conts_area.append(  0 )
            biggest_conts_area_dict[ 0 ] = color
            continue
        biggest_conts_area_dict[ cv2.contourArea(cont[0]) ] = color

    if max(biggest_conts_area) == 0:
        return default
    return biggest_conts_area_dict[max(biggest_conts_area)]
    
while True:
    tr, frame = cap.read()
    
    if not tr:
        print('camera err')
        cap = cv2.VideoCapture(0)
        continue
    # отзеркалили
    frame = cv2.flip(frame, 3)
    frame_blur = cv2.blur(frame, (5, 5) )
    
    frame_hsv = cv2.cvtColor( frame_blur, cv2.COLOR_BGR2HSV)    
    
    # желтый
    clr_low  = (10, 30, 40)
    clr_high = (45, 255, 255)

    mask_red = find_red_mask(frame_hsv)
    
    mask_yellow = find_yellow_mask(frame_hsv)
    
    result = max_hue([mask_red, mask_yellow], ['red', 'yellow'], 'no color')

    print(result)
    #cv2.drawContours(frame, cont, 0, (100,250,0), 2 ) 
    ###
    frame[mask_red==255, 1] +=50
    
    cv2.imshow('camera', frame)
    cv2.imshow('camera mask', mask_red)
    cv2.imshow('camera blur', frame_blur)
    key = cv2.waitKey( 1 )

    if key == 27: # esc
        break 

cap.release()
cv2.destroyAllWindows()
