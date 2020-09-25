#!/usr/bin/env python3
import sys
import json
from copy import deepcopy
import numpy as np
import os
import glob


def set_coordinates_and_area(dataloop_sections, coco_annotation):
    if dataloop_sections['type'] == 'box':
        # COCO Bounding box: (x-top left, y-top left, width, height)
        coco_annotation['bbox'].append(deepcopy(round(dataloop_sections['coordinates'][0]['x'], 2)))
        coco_annotation['bbox'].append(deepcopy(round(dataloop_sections['coordinates'][0]['y'], 2)))
        coco_annotation['bbox'].append(
            deepcopy(round(dataloop_sections['coordinates'][1]['x'] - dataloop_sections['coordinates'][0]['x'], 2)))
        coco_annotation['bbox'].append(
            deepcopy(round(dataloop_sections['coordinates'][1]['y'] - dataloop_sections['coordinates'][0]['y'], 2)))
        # Calculate the bbox area:
        coco_annotation['area'] = deepcopy(coco_annotation['bbox'][2] * coco_annotation['bbox'][3])
    elif dataloop_sections['type'] == 'segment':
        polygon_x_coordinates = []
        polygon_y_coordinates = []
        for subsections in dataloop_sections['coordinates'][0]:
            coco_annotation['segmentation'][0].append(deepcopy(round(subsections['x'], 2)))
            coco_annotation['segmentation'][0].append(deepcopy(round(subsections['y'], 2)))
            polygon_x_coordinates.append(round(subsections['x'], 2))
            polygon_y_coordinates.append(round(subsections['y'], 2))
        # Polygon area calculation according to Shoelace formula:
        coco_annotation['area'] = 0.5 * np.abs(np.dot(polygon_x_coordinates, np.roll(polygon_y_coordinates, 1)) -
                                               np.dot(polygon_y_coordinates, np.roll(polygon_x_coordinates, 1)))


def convert_dataloop_to_cocojson(path):
    # Define output COCO JSON format:
    output_coco_json_dict = {
        "info": {},
        "images": [],
        "type": "instances",
        "annotations": [],
        "categories": [{},
                       {
                           "supercategory": "animal",
                           "id": 2,
                           "name": "dog"
                       },
                       {
                           "supercategory": "body parts",
                           "id": 3,
                           "name": "ear"
                       }],
        "licenses": [],

    }

    # Input .JSON files only from directory:
    for filename in glob.glob(os.path.join(path, '*.json')):
        with open(filename, encoding='utf-8', mode='r') as dataloop_json_file:
            dataloop_data = json.load(dataloop_json_file)

        # Define COCO JSON image section format:
        coco_image = {
            'file_name': dataloop_data['filename'].replace("/", ""),
            'height': dataloop_data['metadata']['system']['height'],
            'width': dataloop_data['metadata']['system']['width'],
            'id': dataloop_data['_id']
        }

        # Add COCO JSON image section to the output COCO JSON sections
        output_coco_json_dict['images'].append(coco_image)

        # Define COCO JSON annotation sections format:
        coco_annotation = {
            'segmentation': [[]],
            'area': "",
            'iscrowd': "",
            'image_id': "",
            'bbox': [],
            'category_id': "",
            'id': ""
        }

        # Iterate on each section in dataloop annotation
        for dataloop_sections in dataloop_data['annotations']:

            # Set id
            coco_annotation['id'] = deepcopy(dataloop_sections['id'])

            # Set image_id
            coco_annotation['image_id'] = deepcopy(dataloop_sections['datasetId'])

            # Set category_id:
            for cat in output_coco_json_dict['categories']:
                if len(cat) != 0 and cat['name'] == dataloop_sections['label']:
                    coco_annotation['category_id'] = cat['id']

            #Set bbox/segment coordinates and area:
            set_coordinates_and_area(dataloop_sections, coco_annotation)

            # Add COCO JSON annotation section to the output COCO JSON annotations sections array:
            output_coco_json_dict['annotations'].append(deepcopy(coco_annotation))

            # Clear all values for the next dataloop annotation section:
            coco_annotation = {
                'segmentation': [[]],
                'area': "",
                'iscrowd': "",
                'image_id': "",
                'bbox': [],
                'category_id': "",
                'id': ""
            }

    # Print COCO JSON file
    print(json.dumps(output_coco_json_dict, indent=4, sort_keys=True))

    # Save the output COCO JSON data to a file
    with open('coco.json', 'w', encoding='utf-8') as f:
        json.dump(output_coco_json_dict, f, ensure_ascii=False, indent=4)


def main():
    # Path format for mac: python3 main.py "/Users/***/Documents/dataloop"
    # Path format for win: python3 main.py "C:\New folder"
    path = sys.argv[1]
    convert_dataloop_to_cocojson(path)


if __name__ == '__main__':
    main()