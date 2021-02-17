from github import Github
import os
import base64
from pathlib import Path
from github import GithubException
import datetime as dt
import shutil

#Remove Last Month data and Parent Directory Get Directory....

path_rm_mk = "C:\project\download"   
shutil.rmtree(path_rm_mk) 
os.makedirs(path_rm_mk)
print("data get truncated successfully for :", path_rm_mk)

now = dt.datetime.now()
check_in_dt=now-dt.timedelta(days=5)

g = Github('3015d4949839ffc3914da369e363ce9afabf8058')  # pls generate your token if not worked

token = '3015d4949839ffc3914da369e363ce9afabf8058'

#g = Github(base_url="https://github.com/CenturyLink/271LIT_NEWSTAT/api/v3", login_or_token=token)

#g = Github('AC79308', 'ctli@1122')

#------------------------------------------

token = os.getenv('GITHUB_TOKEN', token)
owner = "rahulbhusari"
repo = "test2"
#query_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
#-----------------------------------------------------------------
user = g.get_user()
repository = g.get_repo("rahulbhusari/Test2", lazy=False)
print(repo)
#file_content = repo.get_contents('or_config.sas')
print("----------------------------------------------------------------")
#organization = g.get_user().get_orgs()[0]
#repository_name = "Test2"
#repository = organization.get_repo(repository_name)


def get_sha_for_tag(repository, tag):
    """
    Returns a commit PyGithub object for the specified repository and tag.
    """
    branches = repository.get_branches()
    matched_branches = [match for match in branches if match.name == tag]
    if matched_branches:
        return matched_branches[0].commit.sha

    tags = repository.get_tags()
    matched_tags = [match for match in tags if match.name == tag]
    if not matched_tags:
        raise ValueError('No Tag or Branch exists with that name')
    return matched_tags[0].commit.sha
#------------------------------------------------------------------
def bloob_dwn(p_content):
    try:
        blob =repository.get_git_blob(p_content.sha)
        file_data = base64.b64decode(blob.content)           
        dest =Path()/ "C:/project/download" / p_content.path           
        file_out = open(dest, "wb")                   
        file_out.write(file_data)               
        print("try :", dest)            
        file_out.close()
    except (GithubException, IOError) as exc:
        print(GithubException)

def non_blob_dwn(p_content, p_sha, p_repository):
    try:
        path = p_content.path
        commits = p_repository.get_commits(path=path)
        if commits.totalCount:
            global commit_date
            commit_date=(commits[0].commit.committer.date)
            print("commit_date : ", commit_date)
            if commit_date > check_in_dt:  
                file_content = p_repository.get_contents(path, ref=p_sha)
                file_data = base64.b64decode(file_content.content)          
                dest =Path()/ "C:/project/download" / p_content.path           
                file_out = open(dest, "wb")                   
                file_out.write(file_data)               
                print("try :", dest)               
                file_out.close()
    except (GithubException, IOError) as exc:
        bloob_dwn(p_content)    
#-----------------------------------------------------------------        
def download_directory(repository, sha, server_path):
    """
    Download all contents at server_path with commit tag sha in
    the repository.
    """
   
    contents = repository.get_contents("")
    #print(contents)

    for content in contents:
        #print("dir content" ,content.name)
        
        if content.type == 'dir':
             print (content.path)
             contents.extend(repository.get_contents(content.path))
             dest =Path()/ "C:/project/download" / content.path
             if not os.path.exists(dest):
                 os.makedirs(dest)
                 print(dest)
             else:
                 non_blob_dwn(content, sha, repository)
            #print(content.name)
        else:
            non_blob_dwn(content, sha, repository)

#sha = get_sha_for_tag(repo, 'demo')
#file_content = repo.get_contents('or_config.sas', ref=sha)
#repository=repo
                
branch_or_tag_to_download = "main"
sha = get_sha_for_tag(repository, branch_or_tag_to_download)

directory_to_download = "test2"
download_directory(repository, sha, directory_to_download)


print("done pls check once")


now = dt.datetime.now()
check_in_dt=now-dt.timedelta(days=1)






