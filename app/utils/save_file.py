from fastapi import HTTPException, UploadFile


def save_file_image(file: UploadFile, file_path: str):
    try:
        file_name = file.filename
        file_extension = file_name.split(".")[-1]
        file_extension = file_extension.lower()

        if file_extension not in ["jpg", "jpeg", "png"]:
            raise HTTPException(status_code=400, detail="Invalid image file")

        file_path = f".{file_path}"

        with open(file_path, "wb") as f:
            f.write(file.file.read())
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Invalid image file")
