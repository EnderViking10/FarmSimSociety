import requests
import xml.etree.ElementTree as ET


class FSSAPI:
    def __init__(self, base_url):
        """
        Initialize the API client.

        :param base_url: The base URL of the API, e.g., "http://192.168.1.100:8000".
        """
        self.base_url = base_url.rstrip("/")

    def send_command(self, action, params):
        """
        Send a command to the API.

        :param action: The action to perform, e.g., "add_money" or "rename_farm".
        :param params: A dictionary of parameters required for the action.
        :return: A tuple (success: bool, message: str).
        """
        if not isinstance(params, dict):
            return False, "Parameters must be provided as a dictionary."

        # Create the root <command> element
        command = ET.Element("command")
        action_element = ET.SubElement(command, "action")
        action_element.text = action

        # Create <parameters> and dynamically add sub-elements from params dictionary
        parameters = ET.SubElement(command, "parameters")
        for key, value in params.items():
            param_element = ET.SubElement(parameters, key)
            param_element.text = str(value)

        # Convert to XML string
        xml_data = ET.tostring(command, encoding="utf-8", method="xml")

        try:
            # Make the POST request
            response = requests.post(self.base_url, data=xml_data, headers={"Content-Type": "application/xml"})

            # Parse the response
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                status = root.find("status").text
                message = root.find("message").text
                if status == "success":
                    return True, message
                else:
                    return False, message
            else:
                return False, f"HTTP Error: {response.status_code} - {response.reason}"
        except requests.RequestException as e:
            return False, f"Request error: {str(e)}"
