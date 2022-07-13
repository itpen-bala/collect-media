import io

from ftplib import FTP, all_errors
from typing import Any, Optional
from loguru import logger

from app import config
from app.exceptions import InternalServerException


class FTPClient:
    def __init__(
            self,
            host: Optional[str] = None,
            user: Optional[str] = None,
            passwd: Optional[str] = None
    ):
        try:
            self.client = FTP(
                host=host or config.settings.ftp.host,
                user=user or config.settings.ftp.user,
                passwd=passwd or config.settings.ftp.passwd
            )
        except all_errors as err:
            raise InternalServerException from err

    def upload_opened_file(self, file, ftp_path: str) -> None:
        try:
            logger.info("Upload file to FTP path {}", ftp_path)
            self.client.storbinary('STOR ' + ftp_path, file)
        except all_errors as err:
            raise InternalServerException from err

    def get_opened_file(self, ftp_path) -> Any:
        f = io.BytesIO()
        try:
            logger.info("Opening file from FTP path {}", ftp_path)
            self.client.retrbinary('RETR ' + ftp_path, f.write)
        except all_errors as err:
            raise InternalServerException from err
        return f

    def move_file(self, src_file: str, dst_file: str) -> None:
        # TODO: check this method, when we want move a file to another file system
        try:
            logger.info(f"Moving file {src_file} to {dst_file}")
            self.client.rename(src_file, dst_file)
        except all_errors as err:
            raise InternalServerException from err

    def _is_dir_exist(self, directory):
        filelist = []
        self.client.retrlines('LIST', filelist.append)
        for f in filelist:
            if f.split()[-1] == directory and f.startswith('d'):
                return True
        return False

    def mkd(self, parent_dir, directory):
        # Need remove start slash if it exist, because method "_is_dir_exist" use FTP-command "LIST",
        # that show all files in current directory with start slash in file names
        if directory[0] == '/':
            directory = directory[1:]
        try:
            self.client.cwd(parent_dir)
            if self._is_dir_exist(directory) is False:
                logger.info(f"Creating directory: {directory}")
                self.client.mkd(directory)
        except all_errors as err:
            raise InternalServerException from err

    def get_size(self, file_path):
        return self.client.size(file_path)

    def delete(self, file_path) -> None:
        try:
            logger.info(f"Deleting file from FTP. Path: {file_path}")
            self.client.delete(file_path)
        except all_errors as err:
            raise InternalServerException() from err
