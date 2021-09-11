from pathlib import Path
import uuid


def download_file(message, bot) -> str:
    try:
        file_name = message.document.file_name
        file_id_info = bot.get_file(message.document.file_id)
    except:
        file_name = f"{str(uuid.uuid4().hex)}.jpg"
        fileID = message.photo[-1].file_id
        file_id_info = bot.get_file(fileID)

    downloaded_file = bot.download_file(file_id_info.file_path)

    cur_path = str(Path("../bot_files").absolute())
    Path(f"{cur_path}/{message.chat.id}").mkdir(parents=True, exist_ok=True)
    full_path = f"{cur_path}/{message.chat.id}/{file_name}"

    with open(full_path, "wb") as new_file:
        new_file.write(downloaded_file)

    return file_name
