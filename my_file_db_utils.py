import datetime
from pathlib import Path


# db_file_path = "/Users/klsnkv/coding/python/status_db"

# status_object = {
#     "time": datetime.datetime.now(),
#     "payload": "fucking amazing",

#     "photos_subfolder_path": "/Volumes/Untitled/",
#     "photos_finished": True,

#     "videos_subfolder_path": "/Volumes/Untitled/",
#     "videos_finished": False,

#     'path': Path(db_file_path),
#     "finished": True,
# }


def put_status_in_db(status_obj, db_file_path):
    db_file_path = Path(db_file_path)
    with open(db_file_path, "w") as f:
        for key in status_obj:
            if type(status_obj[key]) == datetime.datetime:
                f.write(f"{key}: {status_obj[key].strftime('%Y_%m_%d %H:%M:%S')}\n")
            elif type(status_obj[key]) == bool:
                f.write(f"{key}: {status_obj[key]}\n")
            elif type(status_obj[key]) == Path:
                f.write(f"{key}: {str(status_obj[key].resolve())}\n")
            else:
                f.write(f"{key}: {status_obj[key]}\n")

def get_status_from_db(db_file_path):
    db_file = Path(db_file_path)
    if not db_file.exists():
        return {}
    with open(db_file, "r") as f:
        lines = f.readlines()
    status_obj = {}
    for line in lines:
        key, value = line.strip().split(": ")
        status_obj[key] = value
        if value == "True":
            status_obj[key] = True
        elif value == "False":
            status_obj[key] = False
    if "time"  in status_obj:
        status_obj["time"] = datetime.datetime.strptime(status_obj["time"], "%Y_%m_%d %H:%M:%S")
    return status_obj