# Second_Assignment

Dataloop JSON format to COCO JSON format convertor.
The solution iterates through all the .JSON files in the given directory and creates one .JSON COCO format file in the same directory as a main.py script.
The given Dataloop sections are partially converted to COCO format (annotations, images).
Other COCO format sections are created as an empty values/arrays (i.e. info,licenses).
In order to set correctly category_id in COCO annotations section, categories section was pre-defined.
The bbox coordinates are set in accordance with the COCO format (x-top left, y-top left, width, height).
The bbox/segment(polygon) areas are calculated separately (width*height for bbox, Shoelace formula is used for segment(polygon) coordinates).

To run the script, please enter the Dataloop JSON files directory:

Win:
python3 main.py "C:\New folder"

Mac:
python3 main.py "/Users/***/Documents/dataloop"