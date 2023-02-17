# Single Image Mode
# '0':'person',

classes={'1':'bicycle','2':'car','3':'bike','5':'bus','7':'truck'}
list_of_classes=[1,2,3,5,7]
def image_detect(ip_path, op_path):
    with tf.Session() as sess:
        sess.run(model.pretrained())

        frame = cv2.imread(ip_path, cv2.IMREAD_COLOR)
        # ret, frame = cap.read()
        img=cv2.resize(frame,(416,416))
        imge=np.array(img).reshape(-1,416,416,3)
        start_time=time.time()

        preds = sess.run(model.preds, {inputs: model.preprocess(imge)})

        # print("--- %s seconds ---" % (time.time() - start_time)) 
        boxes = model.get_boxes(preds, imge.shape[1:3])

        boxes1=np.array(boxes, dtype=object)
        for j in list_of_classes:
            count =0
            if str(j) in classes:
                lab=classes[str(j)]

            if len(boxes1) !=0:
                
                for i in range(len(boxes1[j])):
                    box=boxes1[j][i]
                    
                    if boxes1[j][i][4]>=.40: 
                        count += 1    

                        cv2.rectangle(img,(box[0],box[1]),(box[2],box[3]),(0,255,0),1)
                        cv2.putText(img, lab, (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), lineType=cv2.LINE_AA)
            # print(lab,": ",count)
        
        cv2.imwrite(op_path, img)
