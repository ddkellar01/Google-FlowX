import git
import subprocess

class ShadowBrancher:
    """Creates isolated Git feature branches and deploys shadow testing environments."""
    
    def __init__(self, repo_path: str = "."):
        self.repo = git.Repo(repo_path)

    def create_and_push_shadow_feature(self, feature_name: str, modified_files: dict):
        branch_name = f"shadow/feature-{feature_name}"
        current = self.repo.create_head(branch_name)
        current.checkout()

        for file_path, code in modified_files.items():
            with open(file_path, "w") as f:
                f.write(code)
            self.repo.index.add([file_path])

        self.repo.index.commit(f"Auto-generated feature patch: {feature_name}")
        print(f"Checked out and committed shadow feature branch: {branch_name}")
        
        # Trigger isolated Cloud Build shadow run
        subprocess.run(["gcloud", "builds", "submit", f"--config=cloudbuild-shadow.yaml", f"--substitutions=_BRANCH={branch_name}"])
