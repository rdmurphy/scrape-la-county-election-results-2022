from csv import DictReader
import subprocess

def snapshot_results():
    with open('snapshots.csv') as f:
        rows = [row for row in DictReader(f)]
    
    for row in rows:
        date = row['date']
        commit_sha = row['commit_sha']

        process = subprocess.run(
            ['git', 'show', f'{commit_sha}:results.json'],
            capture_output=True,
            text=True,
        )

        with open(f'results/{date}.json', 'w') as outfile:
            outfile.write(process.stdout)

        process = subprocess.run(
            ['git', 'show', f'{commit_sha}:counter_data.json'],
            capture_output=True,
            text=True,
        )

        with open(f'counter_data/{date}.json', 'w') as outfile:
            outfile.write(process.stdout)


if __name__ == '__main__':
    snapshot_results()