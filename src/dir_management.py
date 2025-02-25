import os
import shutil

def delete_all_dir_contents(path):
    path_exists = os.path.exists(path)
    
    if path_exists:
        path_list = os.listdir(path)
        if len(path_list) == 0:
            return
        print(f"Removing directory at {path}")
        shutil.rmtree(path)
        print(f"Creating directory at {path}")
        os.mkdir(path)
    else:
        print(f"Creating directory at {path}")
        os.mkdir(path)
    
def copy_from_static_to_public(source, dest, show_success_message=0):
    if show_success_message == 0:
        show_message = {"main": False, "sub": False}
    if show_success_message == 1:
        show_message = {"main": True, "sub": False}
    if show_success_message == 2:
        show_message = {"main": True, "sub": True}
    source_exists = os.path.exists(source)

    if source_exists:
        path_list = os.listdir(source)

        if len(path_list) == 0:
            return

        for path in path_list:
            source_path = os.path.join(f"{source}/{path}")
            destination_path = os.path.join(f"{dest}/{path}")

            if os.path.isfile(source_path):
                shutil.copy(source_path, destination_path)
            else:
                os.mkdir(destination_path)
                if show_message["sub"]:
                    copy_from_static_to_public(source_path, destination_path, 2)
                else:
                    copy_from_static_to_public(source_path, destination_path)
        
    else:
        raise Exception(f"source directory at {source} doesn't exist at the path")
    
    if show_message["main"]:
        print(f"All content successfully copied from {source} to {dest}")