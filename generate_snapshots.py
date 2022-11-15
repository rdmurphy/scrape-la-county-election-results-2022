from csv import DictReader
import subprocess

def generate_snapshots():
    """
    Generates a snapshot of results.json and counter_data.json at certain points
    in time.

    These two are generated separately because they do not consistently update
    together in a single commit, causing them to have different commit hashes.
    """

    # results.json
    with open('results_snapshots.csv') as f:
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

    # counter_data.json
    with open('counter_snapshots.csv') as f:
        rows = [row for row in DictReader(f)]
    
    for row in rows:
        date = row['date']
        commit_sha = row['commit_sha']

        process = subprocess.run(
            ['git', 'show', f'{commit_sha}:counter_data.json'],
            capture_output=True,
            text=True,
        )

        with open(f'counter_data/{date}.json', 'w') as outfile:
            outfile.write(process.stdout)


if __name__ == '__main__':
    generate_snapshots()