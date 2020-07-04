import os
import sys
import time
# import numpy as np
import cv2

def clahe(in_img):
    clip_limit = 2.0
    grid_size = (2, 2)

    print("[STATUS] Performing CLAHE with clip limit " + str(clip_limit) + " and grid size " + str(grid_size) + ".")
    return cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid_size).apply(in_img)

fps = 24
first_img = 0

input_directories = os.listdir()
target_dir = "compilation"

# output = ""
collection = "everything/"
output_directory_name = "frames/"

# Current directory name
dir_name = os.path.basename(os.getcwd())

# Directory for every frame
output_directory = "everything/"

if(os.path.isdir(output_directory)):
    print("[WARNING] Output directory '" + output_directory + "' Already exists. Overwrite? [y/n]")
    choice = input()
    # first_dir += 1
    while(choice != 'y' and choice != 'n'):
        print("[ERROR] Invalid choice. Please try again. Options: 'y' or 'n'")
        choice = input()
    if(choice != 'y'):
        print("[STATUS] Aborting...")
        exit()
else:
    print("[OK] No output directory found.")
    print("[STATUS] Creating output directory...")
    try:
        os.mkdir(output_directory)
    except OSError:
        print("[ERROR] Creation of the directory '" + output_directory + "' failed")
    else:
        print("[OK] Successfully created the directory '" + output_directory + "'.")

output = dir_name

print("-" * 30)
print("[INFO] ---Excecution start---")
if(dir_name != target_dir):
    print("[WARNING] Working directory '" + dir_name + "' is not the target directory. Continue? [y/n]")
    # choice = input()
    choice = 'y'
    while(choice != 'y' and choice != 'n'):
        print("[ERROR] Invalid choice. Please try again. Options: 'y' or 'n'")
    if(choice != 'y'):
        print("[STATUS] Aborting...")
        exit()
else:
    print("[OK] Working directory is target directory...")

print("-" * 30)
print("[STATUS] ---Begin Processing---")

start_time = time.time()

print("[INFO] Directories to process: " + str(os.listdir()))
print("-"*30)
for current_directory in input_directories:
    # Check if it is a directory
    if(not(os.path.isdir(current_directory)) or current_directory == collection[:-1]):
        continue

    output_directory = current_directory + "/" + output_directory_name

    if(os.path.isdir(output_directory)):
        print("[WARNING] Output directory '" + output_directory + "' Already exists. Overwrite? [y/n]")
        choice = input()
        first_img += 1
        while(choice != 'y' and choice != 'n'):
            print("[ERROR] Invalid choice. Please try again. Options: 'y' or 'n'")
            choice = input()
        if(choice != 'y'):
            print("[STATUS] Aborting...")
            exit()
    else:
        print("[OK] No output directory found.")
        print("[STATUS] Creating output directory...")
        try:
            os.mkdir(output_directory)
        except OSError:
            print("[ERROR] Creation of the directory '" + output_directory + "' failed")
        else:
            print("[OK] Successfully created the directory '" + output_directory + "'.")

    
    inputs = os.listdir(current_directory + "/")[first_img:]
    print("Inputs from directory '" + str(current_directory) + "': " + str(inputs))

    cnt = 0.0

    for img_path in inputs:
        print("[STATUS] Got image: '" + str(img_path) + "'.")
    
    print("-" * 30)

    print(str(">"*10) + "F: " + str(first_img))
    cur_img_path = current_directory + "/" + inputs[first_img]
    print(str(">"*10) + "F1: " + str(first_img))

    print("[STATUS] Loading image '" + cur_img_path + "'.")
    cur_img = cv2.imread(cur_img_path)

    print("[STATUS] Getting frame dimensions...")
    height, width, c = cur_img.shape

    print("[OK] Got frame dimensions")

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter("clahe_" + dir_name + ".mp4", fourcc, fps, (round(width),round(height)))

    for relative_img_path in inputs:
        print("[--INFO] Path: '" + img_path + "'.")
        img_path = current_directory + "/" + relative_img_path
        print("[INFO] Path: '" + img_path + "'.")

        print("[" + str(round(cnt/len(inputs)*100)) + "%] Performing CLAHE on: \"" + img_path + "\"")
        try:
            cnt += 1

            print("[STATUS] Loading image...")
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            print("[OK] Loaded image.")
            
            print("[STATUS] Performing CLAHE...")
            out_img = clahe(img)
            print("[OK] Finished performing CLAHE.")

            print("[OK] Processed image ready.")

            # Write to image
            print(">"*5 + "[INFO] '" + (output_directory + relative_img_path) + "' ...")
            print("[STATUS] Writing image to '" + (output_directory + relative_img_path) + "' ...")
            cv2.imwrite(output_directory + relative_img_path, out_img)
            print("[OK] Successfully written image")

            print("[STATUS] Writing image to '" + (collection + output + "_" + relative_img_path) + "' ...")
            cv2.imwrite(collection + "/" + output + "_" + relative_img_path, out_img)
            print("[OK] Successfully written image")

            # Write to video
            print("[STATUS] Writing to frame...")
            out.write(out_img)
            print("[OK] Successfully written image to frame")

            if((cnt - 1) % 100 == 0):
                elapsed = round(time.time() - start_time, 1)
                cal_fps = round(elapsed/cnt, 4)
                estimated = round(cal_fps * (len(inputs) - cnt), 1)

                print("[STATUS] Time elapsed: " + str(elapsed) + " seconds. Calculation FPS: " + str(cal_fps) + ". Estimated remaining time: " + str(estimated) + "seconds. Frame " + str(cnt) + " (" + str(round((float(cnt)/len(inputs))*100)) + "%)")

                # Pause for CPU cooloff
                if(cnt >= 100):
                    print("[STATUS] Pausing 5 seconds for CPU cooloff...")
                    time.sleep(5)
        except:
            print("[ERROR] Failed on image '" + img_path + "' with message '" + str(sys.exc_info()[1]) + "'.")
            print("[STATUS] Aborting...")
            exit()

    print("[STATUS] Releasing output stream")
    try:
        out.release()
        print("[OK] Successfully released output stream")
    except:
        print("[ERROR] Failed with message '" + str(sys.exc_info()[0]) + "'.\n")
    
    print("[INFO] --- Finished processing directory '" + current_directory + "'.---\n" + "-"*30)

elapsed = round(time.time() - start_time, 1)
cal_fps = round(elapsed/cnt, 4)
estimated = round(cal_fps * (len(inputs) - cnt), 1)
print("[STATUS] Execution finished. Total time elapsed: " + str(elapsed) + " seconds. Processed " + str(cnt) + " frames. Calculation FPS: " + str(cal_fps) + ".")
print("[STATUS] ---DONE---")