import xml.etree.cElementTree as ET
import os
import shutil
import random

classes = []#这里是类别名称
TASKDIR = 'train'#总文件目录
XMLDIR = 'label'#xml文件目录
IMGDIR = 'img'#图片目录
split_scale=0.8#训练 测试 比例
trains = os.listdir(TASKDIR)
#遍历下 获取所有数据的文件夹
imglist=[]
def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

for train in trains:

    xmlpath = TASKDIR+'/'+train+'/'+XMLDIR
    xmls = os.listdir(xmlpath)
    for xml in xmls:

        xmlfile = open(xmlpath+'/'+xml,encoding='utf-8')
        root = ET.parse(xmlfile).getroot()

        #过滤 如果有目标 复制图片 并进行处理
        if (root.find('labeled').text=='true'):
            #获取图片路径
            imgname = root.find('path').text.split('/')[-1]
            imgpath = TASKDIR+'/'+train+'/img/'+imgname
            #复制图片到指定文件夹
            size = root.find('size')
            imgpath_new = 'data/img/{0}-{1}'.format(train,imgname)
            imglist.append(imgpath_new)
            shutil.copy(imgpath,imgpath_new)

            out_file = open('data/label/{0}-{1}'.format(train,imgname.replace('jpg','txt')), 'w')
            w = int(size.find('width').text)
            h = int(size.find('height').text)
            #
            for obj in root.iter('item'):

                cls = obj.find('name').text
                if cls not in classes:
                    continue
                cls_id = classes.index(cls)
                xmlbox = obj.find('bndbox')
                b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                     float(xmlbox.find('ymax').text))
                bb = convert((w, h), b)
                out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
            out_file.close()
        else:
            continue
random.shuffle(imglist)
count = len(imglist)
train = imglist[:int(split_scale*count)]
test = imglist[int(split_scale*count):]
with open('data/train.txt','w') as f:
    for i in train:
        f.writelines(i)
        f.writelines('\n')
with open('data/test.txt','w') as f:
    for i in test:
        f.writelines(i)
        f.writelines('\n')
