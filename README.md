# L.A. County Election Results 2022

A repo for the running of a GitHub Action that retrieves and stores the L.A. County's 2022 general election results feed from [lavote.gov](https://results.lavote.gov/#year=2022&election=4300).

See this data put to use in [this Observable notebook](https://observablehq.com/@rdmurphy/la-county-2022-general-election-results-trends)!

## What's here

| File/Directory  | Notes |
| ------------- | ------------- |
| `results.json`  | A snapshot of the [JSON results file RR/CC makes available](https://www.lavote.gov/home/voting-elections/current-elections/election-results-file-downloads).   |
| `election_data.json` | This file is loaded on the [dynamic updating results page](https://results.lavote.gov/#year=2022&election=4300). It gives every contest and candidate a unique ID. Despite having slots for vote counts, these are always zeroed out.   |
| `counter_data.json` | This file is loaded on the [dynamic updating results page](https://results.lavote.gov/#year=2022&election=4300). It provides the vote values (and other totals) found on a results page. The IDs that appear in this file sync up with the ones in `election_data.json`. |
| `results/*.json` | These files represent each copy of `results.json` collected on a given day. |
| `counter_data/*.json` | These files represent each copy of `counter_data.json` collected on a given day. |
| `timeframes.json` | This file is where all the historical data here is brought together. It includes historical vote totals and changes for every single contest and candidate. |

## Notes

- The results for **Nov. 8** represents the initial ballot count release of the night. This means all of these votes are mail-in ballots tabulated prior to polls closing.
- The results for **Nov. 9** represent the final ballot count release of election night. This means these totals include (at minimum) all the mail-in ballots tabulated prior to polls closing and all Election Day ballots cast. Technically this release happened on Nov. 9 at nearly 4 a.m., so these totals "belong" to this day just to keep this sane.

## License

MIT
