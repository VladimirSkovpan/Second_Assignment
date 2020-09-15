import dtlpy as dl
import os

def main():

    # parse the input argument
    parser = argparse.ArgumentParser()
    parser.add_argument('--path')
    args = parser.parse_args()

    if dl.token_expired():
        dl.login()
    project = dl.projects.create(project_name='Second_Assigment')
    project = dl.projects.get(project_name='Second_Assigment')



    for filename in os.listdir(args.path):
        if filename.endswith(".json"):
            dataset = project.datasets.get(dataset_name='os.path.join(directory, filename)')
            converter = dl.Converter()
            converter.convert_dataset(dataset=dataset, to_format='coco', local_path=r'directory')
            # what file format to save to
            converter.save_to_format = '.json'
            # save
            converter.save_to_file(save_to=r'directory', to_format='coco')
            continue
        else:
            continue

if __name__ == '__main__':
     main()