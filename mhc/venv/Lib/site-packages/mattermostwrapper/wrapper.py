import logging
import time
import json
import requests

class MattermostAPI:
    def __init__(self, url, team, token=""):
        self.url = url
        self.token = token
        self.team = team
        self.team_id = ""


    def get(self, request):
        """
        Used to make get calls to mattermost api
        :param request:
        :return:
        """
        headers = {"Authorization": "Bearer " + self.token }
        g = requests.get(self.url + request, headers=headers)
        return json.loads(g.text)

    def post(self, request, data=None):
        """
        Used to make post calls to mattermost api
        :param request:
        :param data:
        :return:
        """
        headers = {"Authorization": "Bearer " + self.token }
        logging.debug(json.dumps(data, indent=4))
        p = requests.post(self.url + request, headers=headers, data=json.dumps(data))
        return json.loads(p.text)
    
    def login(self, login, password):
        """Login to the corresponding (self.url) mattermost instance."""
        props = {'login_id': login, 'password': password}
        p = requests.post(self.url + '/users/login', data=json.dumps(props))
        self.token = p.headers["Token"] # Store the token for further requests
        self.get_team_id()
        return json.loads(p.text)

    def get_team_id(self):
        teams = self.get('/teams')
        for team in teams:
            if team['name'].lower() == self.team:
                self.team_id = team['id']
    
    def get_teams(self):
        """
        Get team listing back
        :return:
        """
        return self.get('/teams')

    def get_team_members(self):
        """
        This will take in a name of a team and then get the list of team members.
        :param display_name:
        :return:
        """
        return self.get('/teams/' + self.team_id + '/members')

    def get_username_from_id(self, user_id):
        user_request = self.get('/users/' + user_id)
        username = user_request['username']
        return username

    def get_channel_listing(self):
        """
        This function takes in display_name of your team and gets the channel listing for that team.
        :param display_name:
        :return:
        """
        teams = self.get('/teams')
        for team in teams:
            if team['name'].lower() == self.team:
                channel_listing = self.get('/teams/' + team['id'] + '/channels')
                return channel_listing

    def post_channel(self, channel_id, message):
        """
        Creates a new post to a channel
        :param channel_id:
        :param message:
        :return:
        """
        print(f"The post channel token is: {self.token}")
        headers = {"Authorization": "Bearer " + self.token}
        props = {'channel_id': channel_id, 'message': message}
        p = requests.post(self.url + '/posts', headers=headers, data=json.dumps(props))
        print(f"The post channel results are: {p}")
        return p
