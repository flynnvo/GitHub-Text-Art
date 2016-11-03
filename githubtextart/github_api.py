# Copyright 2016 Flynn van Os
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import urllib.request
import json
import base64
import http.client
import time

class GitHub(object):
    """Handles GitHub API requests

    This class is used as an abstraction of the GitHub API for use in other programs

    Attributes:
        username: User's GitHub username
        password: User's GitHub password
        client_id: The application's GitHub API OAuth Client ID
        client_secret: The application's GitHub API OAuth Client Secret
        oauth_token: The OAuth Token obtained during login
        active_repo: The repository to modify where applicable
        user_full_name: User's full name as found on GitHub
        user_email: User's email as found on GitHub
    """
    BASE_URL = 'https://api.github.com'

    def __init__(self, username, password, client_id, client_secret):
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret

    def get_auth_token(self):
        """Get the OAuth2 Token for the GitHub API functions"""
        params = {'scopes' : ['repo'], 'note' : 'Writing history', 'client_id' : self.client_id, 'client_secret' : self.client_secret}
        data = json.dumps(params).encode('UTF-8')
        header = {'Authorization' : 'Basic ' + self._get_basic_auth_string()}
        request = urllib.request.Request(self.BASE_URL + '/authorizations', data, header)
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as error:
            #TODO: Handle auth token error and 2FA
            self._handle_http_error(error)
            raise
        response_data = json.loads(response.read().decode('utf-8'))
        self.oauth_token = response_data['token']
        return

    def _get_basic_auth_string(self):
        """Form a Base64 Encoded string of the form username:password for HTTP Basic Authorization"""
        return base64.b64encode((self.username + ':' + self.password).encode('UTF-8')).decode('UTF-8')

    def set_active_repo(self, repo_name):
        self.active_repo = repo_name

    def _handle_http_error(self, error):
        """Hanlde HTTP Error by printing the error message."""
        #TODO: Handle the error better/more user-friendly
        print('Error', error.code, '\n')
        print(error.headers, '\n')
        print(error.read())
        return

    def _authorized_request(self, path, data = None):
        """Make requests to the GitHub API with our obtained OAuth token

        Args:
            path: the GitHub API path to make the request to
            data: optional parameters in the case of a HTTP POST request
        Returns:
            JSON encoded response to the request
        """
        url = self.BASE_URL + path
        header = {'Authorization' : 'token ' + self.oauth_token}
        if(data):
            data = json.dumps(data).encode('UTF-8')
        request = urllib.request.Request(url, data, header)
        response = urllib.request.urlopen(request)
        response_data = json.loads(response.read().decode('utf-8'))
        return response_data

    def get_respos(self):
        """Get all the active user's repositories"""
        response = self._authorized_request('/user/repos')
        return response

    def has_repo(self, repo_name):
        """Check if the active user has a repository with a given name"""
        path = '/repos/%s/%s' % (self.username, repo_name)
        try:
            response = self._authorized_request(path)
        except urllib.error.HTTPError as error:
            if error.code == 404:
                return False
            else:
                self._handle_http_error(error)
        return True

    def create_repo(self, name, private = False):
        """Create an empty repository, which is automatically initialised by GitHub"""
        params = {'name' : name, 'private' : private, 'has_wiki' : False, 'has_downloads' : False, 'has_issues' : False, 'auto_init' : True}
        response = self._authorized_request('/user/repos', params)
        return

    def create_commit(self, message, tree_sha, parent_commit_sha, date):
        """Create a new commit to the active repository in three steps

        Create a tree for some arbitrary file and contents
        Commit this tree with a set parent
        Update head/master to reference this commit

        Args:
            message: the commit message
            tree_sha: the SHA of the tree to commit to
            parent_commit_sha: the SHA of the commit which will parent our new commit
            date: the date we will set the commit to have
        """
        tree_params = {'base_tree' : tree_sha, 'tree' : [{'path' : 'drawing', 'content' : '1', 'mode' : '100644', 'type' : 'blob'}]}
        tree_path = '/repos/%s/%s/git/trees' % (self.username, self.active_repo)
        response = self._authorized_request(tree_path, tree_params)
        commit_tree_sha = response['sha']

        params = {'message' : message, 'tree' : commit_tree_sha, 'parent' : parent_commit_sha, 'author' : {'name' : self.user_full_name, 'email' : self.user_email, 'date' : date}}
        path = '/repos/%s/%s/git/commits' % (self.username, self.active_repo)
        response = self._authorized_request(path, params)
        new_commit_sha = response['sha']

        refs_params = {'sha' : new_commit_sha, 'force' : True}
        refs_path = '/repos/%s/%s/git/refs/heads/master' % (self.username, self.active_repo)
        try:
            response = self._authorized_request(refs_path, refs_params)
        except urllib.error.HTTPError as error:
            self._handle_http_error(error)
        return new_commit_sha

    def get_tree_and_commit_sha(self):
        """Get the SHA of the tree and commit created by GitHub's auto initialisation of the created repository"""
        path = '/repos/%s/%s/commits' % (self.username, self.active_repo)
        response = self._authorized_request(path)
        first_commit = response[0]
        commit_sha = first_commit['sha']
        user_info = first_commit['commit']['author']
        self.user_full_name = user_info['name']
        self.user_email = user_info['email']
        tree_sha = first_commit['commit']['tree']['sha']
        return tree_sha, commit_sha
