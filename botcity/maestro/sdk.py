from typing import Dict, List, Optional, Tuple

import requests
import urllib3

from . import model
from .impl import (BotMaestroSDKInterface, BotMaestroSDKV1, BotMaestroSDKV2,
                   ensure_access_token)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class BotMaestroSDK(BotMaestroSDKInterface):

    def __init__(self, server: Optional[str] = None, login: Optional[str] = None, key: Optional[str] = None):
        """
        Main class to interact with the BotMaestro web portal.

        This class offers methods to send alerts, messages, create log entries, post artifacts and more.

        Args:
            server: The server IP or name
            login: The username provided via server configuration. Available under `Dev. Environment`
            key: The access key provided via server configuration. Available under `Dev. Environment`

        Attributes:
            access_token (str): The access token obtained via login.
        """
        super().__init__(server=server, login=login, key=key)

    def login(self, server: Optional[str] = None, login: Optional[str] = None, key: Optional[str] = None):
        """
        Obtain an access token with the configured BotMaestro portal.

        Arguments are optional and can be used to configure or overwrite the object instantiation values.

        Args:
            server: The server IP or name
            login: The username provided via server configuration. Available under `Dev. Environment`
            key: The access key provided via server configuration. Available under `Dev. Environment`

        """

        if server:
            self.server = server
        self._login = login or self._login
        self._key = key or self._key
        if not self._server:
            raise ValueError('Server is required.')
        if not self._login:
            raise ValueError('Login is required.')
        if not self._key:
            raise ValueError('Key is required.')
        self.logoff()

        url = f'{self._server}/api/v2/maestro/version'

        with requests.get(url, verify=self.VERIFY_SSL_CERT) as req:
            try:
                if req.status_code == 200:
                    self._impl: BotMaestroSDKV2 = BotMaestroSDKV2(self.server, self._login, self._key)
            finally:
                if self._impl is None:
                    self._impl: BotMaestroSDKV1 = BotMaestroSDKV1(self.server, self._login, self._key)
        self._impl.login()
        self.access_token = self._impl.access_token

    @ensure_access_token()
    def alert(self, task_id: str, title: str, message: str, alert_type: model.AlertType) -> model.ServerMessage:
        """
        Register an alert message on the BotMaestro portal.

        Args:
            task_id: The activity label
            title: A title associated with the alert message
            message: The alert message
            alert_type: The alert type to be used. See [AlertType][botcity.maestro.model.AlertType]

        Returns:
            Server response message. See [ServerMessage][botcity.maestro.model.ServerMessage]
        """
        return self._impl.alert(task_id=task_id, title=title, message=message, alert_type=alert_type)

    @ensure_access_token()
    def message(self, email: List[str], users: List[str], subject: str, body: str,
                msg_type: model.MessageType, group: Optional[str] = None) -> model.ServerMessage:
        """
        Send an email message to the list of email and users given.

        Args:
            email: List of emails to receive the message.
            users: List of usernames registered on the BotMaestro portal to receive the message.
            subject: The message subject.
            body: The message body.
            msg_type: The message body type. See [MessageType][botcity.maestro.model.MessageType]
            group: The message group information.

        Returns:
            Server response message. See [ServerMessage][botcity.maestro.model.ServerMessage]
        """
        return self._impl.message(email=email, users=users, subject=subject, body=body, msg_type=msg_type,
                                  group=group)

    @ensure_access_token()
    def create_task(self, activity_label: str, parameters: Dict[str, object],
                    test: bool = False) -> model.AutomationTask:
        """
        Creates a task to be executed on the BotMaestro portal.

        Args:
            activity_label: The activity unique identified.
            parameters: Dictionary with parameters and values for this task.
            test: Whether or not the task is a test.

        Returns:
            Automation Task. See [AutomationTask][botcity.maestro.model.AutomationTask]
        """
        return self._impl.create_task(activity_label=activity_label, parameters=parameters, test=test)

    @ensure_access_token()
    def finish_task(self, task_id: str, status: model.AutomationTaskFinishStatus,
                    message: str = "") -> model.ServerMessage:
        """
        Finishes a given task.

        Args:
            task_id: The task unique identifier.
            status: The condition in which the task must be finished.
                See [AutomationTaskFinishStatus][botcity.maestro.model.AutomationTaskFinishStatus]
            message: A message to be associated with this action.

        Returns:
            Server response message. See [ServerMessage][botcity.maestro.model.ServerMessage]
        """
        return self._impl.finish_task(task_id=task_id, status=status, message=message)

    @ensure_access_token()
    def restart_task(self, task_id: str) -> model.ServerMessage:
        """
        Restarts a given task.

        Args:
            task_id: The task unique identifier.

        Returns:
            Server response message. See [ServerMessage][botcity.maestro.model.ServerMessage]
        """
        return self._impl.restart_task(task_id=task_id)

    @ensure_access_token()
    def get_task(self, task_id: str) -> model.AutomationTask:
        """
        Return details about a given task.

        Args:
            task_id: The task unique identifier.

        Returns:
            Automation Task. See [AutomationTask][botcity.maestro.model.AutomationTask]
        """
        return self._impl.get_task(task_id=task_id)

    @ensure_access_token()
    def new_log(self, activity_label: str, columns: List[model.Column]) -> model.ServerMessage:
        """
        Create a new log on the BotMaestro portal.

        Args:
            activity_label: The activity unique identifier.
            columns: A list of [Columns][botcity.maestro.model.Column]

        Returns:
            Server response message. See [ServerMessage][botcity.maestro.model.ServerMessage]
        """
        return self._impl.new_log(activity_label=activity_label, columns=columns)

    @ensure_access_token()
    def new_log_entry(self, activity_label: str, values: Dict[str, object]) -> model.ServerMessage:
        """
        Creates a new log entry.

        Args:
            activity_label: The activity unique identifier.
            values: Dictionary in which the key is the column label and value is the entry value.

        Returns:
            Server response message. See [ServerMessage][botcity.maestro.model.ServerMessage]
        """
        return self._impl.new_log_entry(activity_label=activity_label, values=values)

    @ensure_access_token()
    def get_log(self, activity_label: str, date: Optional[str] = "") -> List[Dict[str, object]]:
        """
        Fetch log information.

        Args:
            activity_label: The activity unique identifier.
            date: Initial date for log information in the format DD/MM/YYYY. If empty all information is retrieved.

        Returns:
            Log entry list. Each element in the list is a dictionary in which keys are Column names and values are
            the column value.
        """
        return self._impl.get_log(activity_label=activity_label, date=date)

    @ensure_access_token()
    def delete_log(self, activity_label: str) -> model.ServerMessage:
        """
        Fetch log information.

        Args:
            activity_label: The activity unique identifier.

        Returns:
            Log entry list. Each element in the list is a dictionary in which keys are Column names and values are
            the column value.
        """
        return self._impl.delete_log(activity_label=activity_label)

    @ensure_access_token()
    def post_artifact(self, task_id: int, artifact_name: str, filepath: str) -> model.ServerMessage:
        """
        Upload a new artifact into the BotMaestro portal.

        Args:
            task_id: The task unique identifier.
            artifact_name: The name of the artifact to be displayed on the portal.
            filepath: The file to be uploaded.

        Returns:
            Server response message. See [ServerMessage][botcity.maestro.model.ServerMessage]
        """
        return self._impl.post_artifact(task_id=task_id, artifact_name=artifact_name, filepath=filepath)

    @ensure_access_token()
    def list_artifacts(self) -> List[model.Artifact]:
        """
        List all artifacts available for the organization.

        Returns:
            List of artifacts. See [Artifact][botcity.maestro.model.Artifact]
        """
        return self._impl.list_artifacts()

    @ensure_access_token()
    def get_artifact(self, artifact_id: int) -> Tuple[str, bytes]:
        """
        Retrieve an artifact from the BotMaestro portal.

        Args:
            artifact_id: The artifact unique identifier.

        Returns:
            Tuple containing the artifact name and an array of bytes which are the binary content of the artifact.
        """
        return self._impl.get_artifact(artifact_id=artifact_id)

    def error(self, task_id: int, exception: Exception, screenshot=None, attachments=None, tags=None):
        """
        Creates a new artifact

        Args:
            task_id: The task unique identifier.
            name: The name of the artifact to be displayed on the portal.
            filename: The file to be uploaded.

        Returns:
            Server response message. See [ServerMessage][botcity.maestro.model.ServerMessage]
        """
        return self._impl.error(task_id, exception, screenshot, attachments, tags)
