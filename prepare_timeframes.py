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
            description = contest['MeasureText']
            vote_for = contest['VoteFor']
            candidates = contest['Candidates']

            candidates_output = []

            for candidate in candidates:
                candidate_id = candidate['ID']
                candidate_name = candidate['Name']
                party = candidate['Party']
                votes = collect_votes(candidate_id, lookups)
                adjusted_votes = [0] + votes
                changes = [adjusted_votes[i] - adjusted_votes[i-1] for i in range(1, len(adjusted_votes))]

                candidates_output.append({
                    'id': candidate_id,
                    'name': candidate_name,
                    'party': party,
                    'votes': votes,
                    'changes': changes,
                })

            totals = []

            for candidate in candidates_output:
                for i, change in enumerate(candidate['changes']):
                    if len(totals) < i + 1:
                        totals.append(0)
                    totals[i] += change

            for candidate in candidates_output:
                candidate['percent'] = []

                for i, change in enumerate(candidate['changes']):
                    if totals[i] > 0:
                        candidate['percent'].append(change / totals[i])
                    else:
                        candidate['percent'].append(0)

            output.append({
                'id': id,
                'name': name,
                'type': contest_type,
                'group': contest_group,
                "description": description,
                "vote_for": vote_for,
                "totals": totals,
                'candidates': candidates_output,
            })

    with open('timeframes.json', 'w') as outfile:
        dump({'dates': dates, 'contests': output}, outfile, indent=2)



if __name__ == '__main__':
    prepare()