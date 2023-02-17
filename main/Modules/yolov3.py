# Necessary packages...
import tensornets as nets
import cv2
import numpy as np
import dlib
import tensorflow.compat.v1 as tf
import os

# Decrease tensorflow verbosity.
tf.logging.set_verbosity(tf.logging.ERROR)

# Use verion 1 apis from tensorflow
import tensorflow.compat.v1 as tf 
tf.disable_v2_behavior()

# Set input placeholder frame and initialize yolo versio 3 detector.
inputs = tf.placeholder(tf.float32, [None, 416, 416, 3]) 
model = nets.YOLOv3COCO(inputs, nets.Darknet19, reuse=tf.AUTO_REUSE)

# Target classes...
classes={'1':'bicycle','2':'car','3':'bike','5':'bus','7':'truck'}
list_of_classes=[1,2,3,5,7]

print("Ready!")

# Function to detect the objects in passed image.
def detect(frame, min_confidence = 0.4):
    with tf.Session() as sess:
        sess.run(model.pretrained())
        # reshape the image
        image = np.array(frame).reshape(-1,416,416,3)

        # start_time = time.time()
        # Pass image to detection.
        preds = sess.run(model.preds, {inputs: model.preprocess(image)})

        # get boxes for detected objects
        boxes = model.get_boxes(preds, image.shape[1:3])
        boxes = np.array(boxes, dtype=object)

        # create a dict to store 
        class_counts = {}

        # iterate over all detected object boxes
        for j in list_of_classes:
            count = 0

            # save the label if its in targer class
            if str(j) in classes:
                label = classes[str(j)]

            # Check if there are any boxes available
            if len(boxes) != 0:
                for i in range(len(boxes[j])):
                    # store bounding box co-ordinates
                    box = boxes[j][i]
                    # increase class count if confidence above threshold...
                    if boxes[j][i][4] >= min_confidence: 
                        count += 1

                        if label not in class_counts:
                            class_counts[label] = [count, [(box, boxes[j][i][4])]]
                        else:
                            class_counts[label][0] = count
                            class_counts[label][1].append((box, boxes[j][i][4]))

    return class_counts


# Function to detect the objects in passed image.
def detect_multiple(frames, min_confidence = 0.4):
    with tf.Session() as sess:
        sess.run(model.pretrained())
        
        results = []

        for frame in frames:
            # reshape the image
            image = np.array(frame).reshape(-1,416,416,3)

            # start_time = time.time()
            # Pass image to detection.
            preds = sess.run(model.preds, {inputs: model.preprocess(image)})

            # get boxes for detected objects
            boxes = model.get_boxes(preds, image.shape[1:3])
            boxes = np.array(boxes, dtype=object)

            # create a dict to store 
            class_counts = {}

            # iterate over all detected object boxes
            for j in list_of_classes:
                count = 0

                # save the label if its in targer class
                if str(j) in classes:
                    label = classes[str(j)]

                # Check if there are any boxes available
                if len(boxes) != 0:
                    for i in range(len(boxes[j])):
                        # store bounding box co-ordinates
                        box = boxes[j][i]
                        # increase class count if confidence above threshold...
                        if boxes[j][i][4] >= min_confidence: 
                            count += 1

                            if label not in class_counts:
                                class_counts[label] = [count, [(box, boxes[j][i][4])]]
                            else:
                                class_counts[label][0] = count
                                class_counts[label][1].append((box, boxes[j][i][4]))

            results.append(class_counts)

    return results