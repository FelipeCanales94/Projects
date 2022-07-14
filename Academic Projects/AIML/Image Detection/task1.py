"""
Character Detection

The goal of this task is to implement an optical character recognition system consisting of Enrollment, Detection and Recognition sub tasks

Please complete all the functions that are labelled with '# TODO'. When implementing the functions,
comment the lines 'raise NotImplementedError' instead of deleting them.

Do NOT modify the code provided.
Please follow the guidelines mentioned in the project1.pdf
Do NOT import any library (function, module, etc.).
"""


import argparse
import json
import os
import glob
import cv2
import numpy as np
import sys


# This implementation is based off of https://www.researchgate.net/publication/235708759_Optimizing_two-pass_connected-component_labeling_algorithms
class UnionArray:
    def __init__(self):
        self.equivilances = []
        self.label = 0
    
    def createLabel(self):
        single = self.label
        self.label += 1
        self.equivilances.append(single)
        return single
    
    def parent(self, node, parent):
        while self.equivilances[node] < node:
            next_node = self.equivilances[node]
            self.equivilances[node] = parent
            node = next_node
        self.equivilances[node] = parent
    
    def findParent(self, node):
        while self.equivilances[node] < node:
            node = self.equivilances[node]
        return node
    
    def findNode(self, node):
        node_parent = self.findParent(node)
        self.parent(node, node_parent)
        return node_parent
    
    def union(self, node1, node2):
        if node1 != node2:
            node1_parent = self.findParent(node1)
            node2_parent = self.findParent(node2)
            if node2_parent < node1_parent:
                node1_parent = node2_parent
            self.parent(node2, node1_parent)
            self.parent(node1, node1_parent)

        

def read_image(img_path, show=False):
    """Reads an image into memory as a grayscale array.
    """
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    if show:
        show_image(img)

    return img

def show_image(img, delay=1000):
    """Shows an image.
    """
    cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('image', img)
    cv2.waitKey(delay)
    cv2.destroyAllWindows()

def parse_args():
    parser = argparse.ArgumentParser(description="cse 473/573 project 1.")
    parser.add_argument(
        "--test_img", type=str, default="./data/test_img.jpg",
        help="path to the image used for character detection (do not change this arg)")
    parser.add_argument(
        "--character_folder_path", type=str, default="./data/characters",
        help="path to the characters folder")
    parser.add_argument(
        "--result_saving_directory", dest="rs_directory", type=str, default="./",
        help="directory to which results are saved (do not change this arg)")
    args = parser.parse_args()
    return args

def ocr(test_img, characters):
    """Step 1 : Enroll a set of characters. Also, you may store features in an intermediate file.
       Step 2 : Use connected component labeling to detect various characters in an test_img.
       Step 3 : Taking each of the character detected from previous step,
         and your features for each of the enrolled characters, you are required to a recognition or matching.

    Args:
        test_img : image that contains character to be detected.
        characters_list: list of characters along with name for each character.

    Returns:
    a nested list, where each element is a dictionary with {"bbox" : (x(int), y (int), w (int), h (int)), "name" : (string)},
        x: row that the character appears (starts from 0).
        y: column that the character appears (starts from 0).
        w: width of the detected character.
        h: height of the detected character.
        name: name of character provided or "UNKNOWN".
        Note : the order of detected characters should follow english text reading pattern, i.e.,
            list should start from top left, then move from left to right. After finishing the first line, go to the next line and continue.
        
    """
    # TODO Add your code here. Do not modify the return and input arguments

    
    char_names = [] # for character names
    sep_images, final = detection(test_img) # detect first
    match = [] # for matches

    # separates each character in image and gets its bound box coords while separating the actual character name
    for i in characters:
        enroll_img, enroll_kp, enroll_desc = enrollment(i[1])
        
        coords = recognition(enroll_img, enroll_kp, enroll_desc, sep_images, final)
        match.append(coords)
        char_names.append(i[0])
    
    # append character name to matching image coords
    for i in range(len(char_names)):
        match[i].append(char_names[i])
    
    # update arrays
    for i in match:
        if len(i) == 1:
            continue
        for j in range(len(i)-1):
            i[j].append(i[len(i)-1])
            f = i[j]
            
    arr = []
    # format for json
    for p in final:
        #print(p)
        if len(p) == 4:
            arr.append({"bbox": [p[0]+2, p[1]+2, (p[2]-2)-(p[0]+2), (p[3]-2)-(p[1]+2)], "name": ("UNKNOWN")})
        if len(p) > 5:
            arr.append({"bbox": [p[0]+2, p[1]+2, (p[2]-2)-(p[0]+2), (p[3]-2)-(p[1]+2)], "name": (p[len(p)-1])})
        if len(p) == 5:
            arr.append({"bbox": [p[0]+2, p[1]+2, (p[2]-2)-(p[0]+2), (p[3]-2)-(p[1]+2)], "name": (p[4])})
    return arr
        
    #raise NotImplementedError

def enrollment(img):
    """ Args:
        You are free to decide the input arguments.
    Returns:
    You are free to decide the return.
    """
    # TODO: Step 1 : Your Enrollment code should go here.


    # Use SIFT for keypoints and descriptors
    sift = cv2.SIFT_create()
    kp, desc = sift.detectAndCompute(img, None)

    # if no kp detected, move on
    if len(kp) == 0:
        return img, kp, desc

    img2 = cv2.drawKeypoints(img, kp, outImage=None, color=(0,255,0))

    return img2, kp, desc

    #raise NotImplementedError


def detection(img):
    """ 
    Use connected component labeling to detect various characters in an test_img.
    Args:
        You are free to decide the input arguments.
    Returns:
    You are free to decide the return.
    """


    connection = dict()
    c = []
    uf = UnionArray()


    # TODO: Step 2 : Your Detection code should go here.

    height = img.shape[1]
    width = img.shape[0]

    for j in range(height):
        for i in range(width):

            if img[i, j] >= 198: #thresholding -> colors above this messed up components
                img[i,j] = 255
                pass
            elif j > 0 and img[i, j-1] < 198:
                connection[i,j] = connection[(i, j-1)]
            elif i+1 < width and j > 0 and img[i+1, j-1] < 198:
                l = connection[(i+1,j-1)]
                connection[i, j] = l
                if i > 0 and img[i-1,j-1] < 198:
                    m = connection[(i-1, j-1)]
                    uf.union(l,m)
                elif i > 0 and img[i-1, j] < 198:
                    n = connection[(i-1,j)]
                    uf.union(l,n)
            elif i >0 and j > 0 and img[i-1,j-1] < 198:
                connection[i,j] = connection[(i-1,j-1)]
            elif i > 0 and img[i-1,j] < 198:
                connection[i,j] = connection[(i-1,j)]
            else:
                connection[i,j] = uf.createLabel()

    
    # Gets bounding box coords
    coords = dict()
    for (x,y) in connection:
        component = uf.findNode(connection[(x,y)])        
        connection[(x, y)] = component      
        if component not in coords:
            coords[component]=[x,y]
        else:
            coords[component].append([x,y])

    recCoords = dict()
    for i in coords:
        maxX = 0
        maxY = 0
        minX = coords[i][0]
        minY = coords[i][1]
        for x in range(2, len(coords[i])):
            if maxX < coords[i][x][0]:
                maxX = coords[i][x][0]
            if maxY < coords[i][x][1]:
                maxY = coords[i][x][1]

            if minX > coords[i][x][0]:
                minX = coords[i][x][0]
            if minY > coords[i][x][1]:
                minY = coords[i][x][1]
        recCoords[i] = [minY-2, minX-2, maxY+2, maxX+2]
#draw bounding boxes on image
    final = []
    for i in recCoords:
        final.append(recCoords[i])
        for x in recCoords[i]:
            color = (0, 255, 0)
            image = cv2.rectangle(img, (recCoords[i][0], recCoords[i][1]), (recCoords[i][2],recCoords[i][3]), color=color, thickness=0)
            

    separate_images = []
    # separate characters
    for i in final:
        separate_images.append(image[i[1]:i[3], i[0]:i[2]])
    return separate_images, final

    # raise NotImplementedError

def recognition(img_enrollment, kp_enrollment, descriptor_enrollment, detected_chars, coords):
    """ 
    Args:
        You are free to decide the input arguments.
    Returns:
    You are free to decide the return.
    """
    # TODO: Step 3 : Your Recognition code should go here.

    # train bfm -> go through key points from enrollment part -> if any matches do ratio test -> if pass append to good list -> return good list

    new_set = []
    fast = cv2.FastFeatureDetector_create()
    sift = cv2.SIFT_create()
    j = 0
    k = []    
    for i in detected_chars:
        
        op = fast.detect(i,None)
        kp, desc = sift.detectAndCompute(i, None)
        bf = cv2.BFMatcher()
        if descriptor_enrollment is None or desc is None:
            continue
        matches = bf.knnMatch(desc,descriptor_enrollment,k=2)
        # Retio test
        good = []
        for m,n in matches:
            if m.distance < 0.7*n.distance:
                good.append([m])        
        if len(good) > 2:
            k.append(coords[j])
        j+=1
    return k



    #raise NotImplementedError


def save_results(coordinates, rs_directory):
    """
    Donot modify this code
    """
    results = coordinates
    with open(os.path.join(rs_directory, 'results.json'), "w") as file:
        json.dump(results, file)
    


def main():

    args = parse_args()
    
    characters = []

    all_character_imgs = glob.glob(args.character_folder_path+ "/*")
    
    for each_character in all_character_imgs :
        character_name = "{}".format(os.path.split(each_character)[-1].split('.')[0])
        characters.append([character_name, read_image(each_character, show=False)])

    test_img = read_image(args.test_img)
    #print(plt.imshow(characters[0]))

    results = ocr(test_img, characters)

    save_results(results, args.rs_directory)


if __name__ == "__main__":
    main()
