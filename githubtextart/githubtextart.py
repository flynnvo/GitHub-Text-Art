#!/usr/bin/env python3

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


from github_api import GitHub
import patterns

CLIENT_ID = ''
CLIENT_SECRET = ''
REPO_NAME = 'Commit-History-Art'

def main():
    username = input('Enter your GitHub username: ')
    password = input('Enter your GitHub password: ')
    github = GitHub(username, password, CLIENT_ID, CLIENT_SECRET)
    github.get_auth_token()
    if not github.has_repo(REPO_NAME):
        github.create_repo(REPO_NAME)
    github.set_active_repo(REPO_NAME)
    text_to_draw = input('Enter your desired text to show on the contributions history: ')
    text_to_draw = text_to_draw.upper()
    tree_sha, commit_sha = github.get_tree_and_commit_sha()
    draw_dates = patterns.get_draw_dates(text_to_draw)
    for date in draw_dates:
        commit_sha = github.create_commit('Commit', tree_sha, commit_sha, date)


main()
