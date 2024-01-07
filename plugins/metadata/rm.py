import shutil
import aiofiles.os

async def rm_dir(root: str = f"./Downloads"):
    """
    Delete a Folder.

    :param root: Pass DIR Path
    """

    try:
        shutil.rmtree(root)
    except Exception as e:
        logging.getLogger(__name__).error(e)


async def rm_file(file_path: str):
    """
    Delete a File.

    :param file_path: Pass File Path
    """
    try:
        await aiofiles.os.remove(file_path)
    except:
        pass
