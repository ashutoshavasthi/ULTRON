# Runs behind reports/words_g0.md

- `run1/`: the first full run of gate G0-b. `flip_h` met the target; `recolour_all` and `outline`
  were learned but matched 81% and 88%. It was stopped during `fill_enclosed` (log kept), once it
  could no longer reach 3 of 5 families. `gravity` was not run.
- `run2/`: the second run, after the one round of fixes the kill rule allows. This is the run
  the report shows.
- `gravity_diagnosis_step20000.log`: the two measurements that explained why gravity is hard,
  taken on the interpreter as saved at step 20,000.

One file per hidden family, as written by `ultron.words.experiments.rediscovery`.
