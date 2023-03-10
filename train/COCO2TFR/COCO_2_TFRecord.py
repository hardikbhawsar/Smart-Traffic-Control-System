# This Fill is meant to be executed on Google Colab Environment.

# !pip install -q pycocotools

from sys import exit
from numpy.core import records
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pylab
pylab.rcParams['figure.figsize'] = (8.0, 10.0)
import skimage.io as io
from pycocotools.coco import COCO
import os
from tqdm import tqdm


class COCO2TFRecord:
    def __init__(self, img_dir, annotations_file_path) -> None:
        self.annotations_file = annotations_file_path
        self.img_dir = img_dir

        try:
            self.coco=COCO(annotations_file_path)
            self.imgIds = self.coco.getImgIds()
        except:
            exit()

    def loadExample(self):
        self.imgIds = self.coco.getImgIds()
        print("Total images: {}".format(len(self.imgIds)))

        rand=np.random.randint(0,len(self.imgIds))
        img = self.coco.loadImgs(self.imgIds[rand])[0]

        print("Image example:")
        print(img)

        annIds=self.coco.getAnnIds()
        print("\nTotal annotations: {}".format(len(annIds)))

        ann=self.coco.loadAnns(self.coco.getAnnIds(imgIds=img['id']))
        print("Annotation example:")
        print(ann[0])

        I = io.imread(img['coco_url'])
        plt.imshow(I); plt.axis('off')
        annIds = self.coco.getAnnIds(imgIds=img['id'])
        anns = self.coco.loadAnns(annIds)
        self.coco.showAnns(anns)

    def listCategories(self):
        cats = self.coco.loadCats(self.coco.getCatIds())
        print("Number of categories: {}".format(len(cats)))

        nms=[cat['name'] for cat in cats]
        print('\nCOCO categories: \n{}\n'.format(', '.join(nms)))

    def get_annotations(self, imgId):
        annIds = self.coco.getAnnIds(imgIds=imgId)
        anns = self.coco.loadAnns(annIds)

        segmentations=[]
        segmentation_lengths=[]
        bboxes=[]
        catIds=[]
        iscrowd_list=[]
        area_list=[]
        annotation_ids=[]

        for ann in anns:
            try:
                catId=ann['category_id']
                bbox=ann['bbox']
                segmentation=ann['segmentation'][0]
                iscrowd=ann['iscrowd']
                area=ann['area']
                annotation_id=ann['id']
            except:
                continue

            if((not None in bbox) and (None!=catId)):
                catIds.append(catId)
                segmentations.append(segmentation)
                segmentation_lengths.append(len(segmentation))
                bboxes.append(bbox)
                iscrowd_list.append(iscrowd)
                area_list.append(area)
                annotation_ids.append(annotation_id)
        return len(anns),catIds,segmentation_lengths,sum(segmentations,[]),sum(bboxes,[]),iscrowd_list,area_list,annotation_ids

    def convert(self, records_path):
        #Size of each TFRecord file will be 100MB for improving performance
        n=len(self.imgIds)
        imgids=self.imgIds[0:n]
        size=0
        for i in imgids:
            img=self.coco.loadImgs(i)
            fn=img[0]['file_name']
            size+=os.path.getsize(self.img_dir+fn)
        avg_size=size/n
        limit=int(104857600//avg_size)
        total_tfrecords=int(len(self.imgIds)//limit)
        print(f"{total_tfrecords} TFRecord files will be created", flush=True)

        for i in tqdm(range(0,total_tfrecords)):
            examples=[]
            start=i*limit
            end=start+limit
            imgids=self.imgIds[start:end]
            
            for img in self.coco.loadImgs(imgids):
                with open(str(self.img_dir)+img['file_name'],'rb') as f:
                    image_string=f.read()

                objects,catIds,segmentation_lengths,segmentations,bboxes,iscrowd,area,annotation_ids=self.get_annotations(img['id'])

                # Create a Features message using tf.train.Example.
                example = tf.train.Example(features=tf.train.Features(feature={
                    'image': tf.train.Feature(bytes_list=tf.train.BytesList(value=[image_string])),
                    'height': tf.train.Feature(int64_list=tf.train.Int64List(value=[img['height']])),
                    'width': tf.train.Feature(int64_list=tf.train.Int64List(value=[img['width']])),
                    'id': tf.train.Feature(int64_list=tf.train.Int64List(value=[img['id']])),
                    'license': tf.train.Feature(int64_list=tf.train.Int64List(value=[img['license']])),
                    'file_name': tf.train.Feature(bytes_list=tf.train.BytesList(value=[tf.compat.as_bytes(img['file_name'])])),
                    'coco_url': tf.train.Feature(bytes_list=tf.train.BytesList(value=[tf.compat.as_bytes(img['coco_url'])])),
                    'flickr_url': tf.train.Feature(bytes_list=tf.train.BytesList(value=[tf.compat.as_bytes(img['flickr_url'])])),
                    'date_captured': tf.train.Feature(bytes_list=tf.train.BytesList(value=[tf.compat.as_bytes(img['date_captured'])])),
                    #objects-Number of objects in the image
                    'objects': tf.train.Feature(int64_list=tf.train.Int64List(value=[objects])),
                    #Follwing features hold all the annotations data given for the image
                    #category_ids-List of aannotation category ids
                    'category_ids': tf.train.Feature(int64_list=tf.train.Int64List(value=catIds)),
                    #segmentation_lengths-List of segmentation lengths
                    'segmentation_lengths': tf.train.Feature(int64_list=tf.train.Int64List(value=segmentation_lengths)),
                    #segmention lists flattened into 1D list
                    'segmentations': tf.train.Feature(float_list=tf.train.FloatList(value=segmentations)),
                    #bboxes flattened into 1D list
                    'bboxes': tf.train.Feature(float_list=tf.train.FloatList(value=bboxes)),
                    #List of iscrowd values
                    'iscrowd': tf.train.Feature(int64_list=tf.train.Int64List(value=iscrowd)),
                    #List of area values
                    'area': tf.train.Feature(float_list=tf.train.FloatList(value=area)),
                    #List of annotation ids 
                    'annotation_ids': tf.train.Feature(int64_list=tf.train.Int64List(value=annotation_ids)),
                }))
                examples.append(example)
            
            with tf.io.TFRecordWriter(records_path+'coco'+str(i)+'.tfrecord') as writer:
                for j in examples:
                    writer.write(j.SerializeToString())
            examples.clear()
            # print("file {} created".format(i))

    def parse(self, feature):
        features = tf.io.parse_single_example(
            feature,
            features={
            'image': tf.io.FixedLenFeature([], tf.string),
            'height': tf.io.FixedLenFeature([], tf.int64),
            'width': tf.io.FixedLenFeature([], tf.int64),
            'id': tf.io.FixedLenFeature([], tf.int64),
            'license': tf.io.FixedLenFeature([], tf.int64),
            'file_name': tf.io.FixedLenFeature([], tf.string),
            'coco_url': tf.io.FixedLenFeature([], tf.string),
            'flickr_url': tf.io.FixedLenFeature([], tf.string),
            'date_captured': tf.io.FixedLenFeature([], tf.string),
            'objects': tf.io.FixedLenFeature([], tf.int64),
            'category_ids': tf.io.VarLenFeature(tf.int64),
            'segmentation_lengths': tf.io.VarLenFeature(tf.int64),
            'segmentations': tf.io.VarLenFeature(tf.float32),
            'bboxes': tf.io.VarLenFeature(tf.float32),
            'iscrowd': tf.io.VarLenFeature(tf.int64),
            'area': tf.io.VarLenFeature(tf.float32),
            'annotation_ids': tf.io.VarLenFeature(tf.int64),  
        })

        
        print('Image id:')
        print(features['id'])
        print('\nlicense:')
        print(features['license'])
        print('\nfile_name:')
        print(features['file_name'])
        print('\ncoco_url:')
        print(features['coco_url'])
        print('\nflickr_url:')
        print(features['flickr_url'])
        print('\ndate_captured:')
        print(features['date_captured'])
        print("\nobjects:")
        print(features['objects'])
        print("\nheight:")
        print(features['height'])
        print("\nwidth:")
        print(features['width'])
        print("\ncategory ids:")
        print(features['category_ids'])
        print("\niscrowd:")
        print(features['iscrowd'])
        print("\narea:")
        print(features['area'])
        print("\nannotation_ids:")
        print(features['annotation_ids'])
        

        objects = features['objects']
        bboxes = features['bboxes']
        bboxes = tf.sparse.to_dense(bboxes)
        bboxes = tf.reshape(bboxes, [objects, 4])
        
        print("\nbboxes:")
        print(bboxes)
        
        print("\nsegmentation lengths:")
        print(features['segmentation_lengths'])
        
        segmentations = features['segmentations']
        segmentations = tf.sparse.to_dense(segmentations)
        segmentation_lengths=tf.sparse.to_dense(features['segmentation_lengths'])
        

        segs=[]
        start=0
        for i in segmentation_lengths:
            segs.append(tf.slice(segmentations,[start,],[i,]))
            start+=i
        print("\nSegmentations:")    
        print(segs)
        
        image = tf.image.decode_jpeg(features['image'], channels=3)
        plt.imshow(image); plt.axis('off')
        
        anns=[]
        for i in range(0,len(segs)):
            #plt.gca().add_patch(Rectangle((i[0],i[1]),i[2],i[3],linewidth=1,edgecolor='r',facecolor='none'))
            ann={}
            ann['segmentation']=[segs[i].numpy().tolist()]
            ann['bbox']=bboxes[i].numpy().tolist()
            anns.append(ann)
        #print(anns)
        self.coco.showAnns(anns,draw_bbox=True)