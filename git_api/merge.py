import os

if __name__ == '__main__':
    path_merge = "./merge"
    path_repos = "data/repos"
    path_commits = "data/commits"

    if not os.path.exists(path_merge):
        os.mkdir(path_merge)

    merge_repos_file = os.path.join(path_merge, "merge_repos.json")
    with open(merge_repos_file, "w") as f0:
        for file in os.listdir(path_repos):
            with open(os.path.join(path_repos, file), "r") as f1:
                for line in f1:
                    f0.write(line)
                f1.close()
        f0.close()

    merge_commits_file = os.path.join(path_merge, "merge_commits.json")
    with open(merge_commits_file, "w") as f0:
        for file in os.listdir(path_commits):
            with open(os.path.join(path_commits, file), "r") as f1:
                for line in f1:
                    f0.write(line)
                f1.close()
        f0.close()
