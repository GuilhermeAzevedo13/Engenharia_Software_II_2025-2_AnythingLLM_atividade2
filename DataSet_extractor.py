import json
import subprocess
from pathlib import Path
from datetime import datetime


class GitStrategyExtractorEssential:
    """
    Versão ESSENCIAL:
    - Branches: overview + amostra dos últimos N commits por branch
    - Releases: tags timeline + git describe
    Saídas:
    - dataset.jsonl com os dados estruturados
    - alguns .txt mínimos para conferência humana
    """

    def __init__(self, repo_path: str, output_dir: str = "git_strategy_output", recent_commits_per_branch: int = 10):
        self.repo = Path(repo_path)
        self.out = Path(output_dir)
        self.out.mkdir(parents=True, exist_ok=True)
        self.n = int(recent_commits_per_branch)

        if not (self.repo / ".git").exists():
            raise ValueError(f"Isso não parece um repositório Git: {self.repo}")

        self.dataset_path = self.out / "dataset.jsonl"
        self.dataset_path.write_text("", encoding="utf-8")

    def git(self, args) -> str:
        cmd = ["git"] + list(args)
        r = subprocess.run(
            cmd,
            cwd=self.repo,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        return (r.stdout or "").strip()

    def save_txt(self, filename: str, content: str):
        (self.out / filename).write_text((content or "").rstrip() + "\n", encoding="utf-8")

    def append_jsonl(self, obj: dict):
        with self.dataset_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    def _repo_id(self) -> str:
        return "github.com/Mintplex-Labs/anything-llm"


    def _list_local_branches(self):
        raw = self.git(["for-each-ref", "refs/heads", "--format=%(refname:short)"])
        return [b.strip() for b in raw.splitlines() if b.strip()]

  
    # ESSENCIAL: Branch strategy
    # -----------------------
    def extract_branches_overview(self):
        # No formato branch | last_commit_date | author | subject para jogar na LLM
        overview_raw = self.git([
         "for-each-ref", "refs/heads", "refs/remotes/origin",
         "--sort=-committerdate",
         "--format=%(refname:short)|%(committerdate:short)|%(authorname)|%(subject)"
                ])

        
        self.save_txt("branches_overview.txt", overview_raw)

        for line in overview_raw.splitlines():
            parts = line.split("|", 3)
            if len(parts) < 4:
                continue
            branch, date, author, subject = parts
            self.append_jsonl({
                "type": "branch_overview",
                "repo": self._repo_id(),
                "branch": branch,
                "last_commit": {
                    "date": date,
                    "author": author,
                    "subject": subject
                }
            })

    def extract_recent_commits_sample(self):
        # amostra: últimos N commits por branch
        branches = self._list_local_branches()

        txt_lines = ["branch|hash|date|author|subject"]

        for b in branches:
            log_raw = self.git([
                "log", f"-n{self.n}",
                "--date=short",
                "--pretty=format:%h|%ad|%an|%s",
                b
            ])
            if not log_raw:
                continue

            for row in log_raw.splitlines():
                row = row.strip()
                if not row:
                    continue

                parts = row.split("|", 3)
                if len(parts) < 4:
                    continue

                h, d, a, s = parts
                txt_lines.append(f"{b}|{h}|{d}|{a}|{s}")

                self.append_jsonl({
                    "type": "commit_sample",
                    "repo": self._repo_id(),
                    "branch": b,
                    "hash": h,
                    "date": d,
                    "author": a,
                    "subject": s
                })

        self.save_txt("branches_recent_commits_sample.txt", "\n".join(txt_lines))

    # ESSENCIAL: Release strategy
    # -----------------------
    def extract_tags_timeline(self):
        # tag | date | subject
        tags_timeline = self.git([
            "for-each-ref", "refs/tags",
            "--sort=creatordate",
            "--format=%(refname:short)|%(creatordate:short)|%(subject)"
        ])
        self.save_txt("tags_timeline.txt", tags_timeline)

        for line in tags_timeline.splitlines():
            parts = line.split("|", 2)
            if len(parts) < 3:
                continue
            tag, date, subject = parts
            self.append_jsonl({
                "type": "tag",
                "repo": self._repo_id(),
                "tag": tag,
                "date": date,
                "subject": subject
            })

    def extract_git_describe(self):
        describe = self.git(["describe", "--tags", "--long", "--always"])
        self.save_txt("git_describe.txt", describe)

        self.append_jsonl({
            "type": "describe",
            "repo": self._repo_id(),
            "describe": describe
        })

    def extract_all(self):
        # Ordem simples: branches -> commits -> tags -> describe
        self.extract_branches_overview()
        self.extract_recent_commits_sample()
        self.extract_tags_timeline()
        self.extract_git_describe()


if __name__ == "__main__":
    REPO = r"ADICIONE AQUI O CAMIHNO PARA O REPOSITÓRIO GIT LOCAL"
    N_COMMITS_PER_BRANCH = 20  
    extractor = GitStrategyExtractorEssential(
        repo_path=REPO,
        output_dir="git_strategy_output",
        recent_commits_per_branch=N_COMMITS_PER_BRANCH
    )
    extractor.extract_all()

    print(f"Concluído. Saída em: {Path('git_strategy_output').resolve()}")
    print(f"Dataset JSONL: {Path('git_strategy_output/dataset.jsonl').resolve()}")
