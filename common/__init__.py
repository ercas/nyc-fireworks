import configparser
import os
import typing

import requests
import tqdm.auto as tqdm

T_Number = typing.Union[int, float]

config = configparser.ConfigParser()
config.read("config.ini")

def download_file(url: str,
                  output_path: str,
                  overwrite: bool = False,
                  show_progress: bool = True,
                  chunk_size: int = int(config["http"]["chunk_size"]),
                  estimated_size: T_Number = 0,
                  ) -> typing.Optional[bool]:
    if overwrite or (not os.path.isfile(output_path)):
        temp_path = output_path + ".part"
        response = requests.get(url, stream=True)
        response.raise_for_status()

        if show_progress:
            progress = tqdm.tqdm(
                total=int(
                    response.headers.get("content-length", estimated_size)
                ),
                unit="iB",
                unit_scale=True,
                desc=os.path.basename(output_path)
            )

        with open(temp_path, "wb") as output_fp:
            for chunk in response.iter_content(chunk_size):
                if show_progress:
                    progress.update(len(chunk))
                output_fp.write(chunk)

        progress.close()
        os.rename(temp_path, output_path)
        return True