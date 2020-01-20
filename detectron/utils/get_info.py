import json
import os

def id(elem):
    return elem['image_id']

def get_info(path, dataset_name):
    with open(path) as openjason:
        Detectron_boxes = json.load(openjason)
        
    human_det=[]
    for m in range(len(Detectron_boxes)):
        for i in range(len(Detectron_boxes[m]['classes'])):
            info_1 = {}
            if Detectron_boxes[m]['classes'][i] == 1:
                info_1['bbox']=Detectron_boxes[m]['boxes'][i][0:4]
                info_1['bbox'][2] = info_1['bbox'][2]-info_1['bbox'][0]
                info_1['bbox'][3] = info_1['bbox'][3]-info_1['bbox'][1]
                for t in range(4):
                    info_1['bbox'][t]=round(info_1['bbox'][t])
                info_1['category_id']=Detectron_boxes[m]['classes'][i]
                info_1['image_id']=Detectron_boxes[m]['image_id']
                info_1['score']=Detectron_boxes[m]['boxes'][i][-1]
                info_1['score']=round(info_1['score'],2)
                if info_1['score'] > 0.8:
                    human_det.append(info_1)
                if info_1['score'] == 1:
                    info_1['score'] = 0.99


    human_det.sort(key=id)
    print(human_det)
    dir = '/home/tecnimaq/Gabriela/Detectron/human_detection/'+dataset_name
    file_name = 'human_detection.json'
    if not os.path.isdir(dir):
        os.mkdir(dir)
    with open(os.path.join(dir,file_name),'w') as thisfile:
        json.dump(human_det, thisfile)

    image_info={
        'images': [],
        'categories': [{'supercategory': 'person', 'id': 1, 'name': 'person'}]
    }

    for m in range(len(Detectron_boxes)):
        per_image_info={'file_name': 0,'id': 0}
        per_image_info['file_name'] = Detectron_boxes[m]['file_name'] 
        per_image_info['id'] = Detectron_boxes[m]['image_id']
        image_info['images'].append(per_image_info)

    #image_info.sort(key=id)
    dir = '/home/tecnimaq/Gabriela/Detectron/image_info/'+dataset_name
    file_name = 'image_info_test2017.json'
    if not os.path.isdir(dir):
        os.mkdir(dir)
    with open(os.path.join(dir,file_name),'w') as thisfile:
        json.dump(image_info, thisfile)
