from json import dump, load
from pathlib import Path

def collect_votes(id, lookups):
    # Collect the votes for a given candidate
    return [lookup[id]['Value'] for lookup in lookups]

def prepare():
    # The file with all the election metadata
    with open('election_data.json') as infile:
        contest_groups = load(infile)['Data']['ContestGroups']
        contest_groups = sorted(contest_groups, key=lambda x: x['Order'])
    
    # The directory where the counter data is stored
    counter_data_dir = Path('counter_data')
    counter_data_files = sorted(counter_data_dir.glob('*.json'))

    lookups = []
    dates = []

    for file in counter_data_files:
        date = file.stem
        dates.append(date)

        with open(file) as infile:
            counter_data = load(infile)['Data']
        
        # The counter data contains the lookup table
        lookups.append(
            {d["ReferenceID"]: d for d in counter_data if d["ReferenceID"]}
        )

    output = []
    
    for group in contest_groups:
        contest_group = group['Name']
        contests = group['Contests']

        for contest in contests:
            id = contest['ID']
            name = contest['Title']
            contest_type = contest['Type']
            candidates = contest['Candidates']

            candidates_output = []

            for candidate in candidates:
                candidate_id = candidate['ID']
                candidate_name = candidate['Name']
                party = candidate['Party']
                votes = collect_votes(candidate_id, lookups)

                candidates_output.append({
                    'id': candidate_id,
                    'name': candidate_name,
                    'party': party,
                    'votes': votes
                })

            output.append({
                'id': id,
                'name': name,
                'type': contest_type,
                'group': contest_group,
                'candidates': candidates_output,
            })

    with open('snapshots.json', 'w') as outfile:
        dump({'snapshots': dates, 'contests': output}, outfile, indent=2)



if __name__ == '__main__':
    prepare()