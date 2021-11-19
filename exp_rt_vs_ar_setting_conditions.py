subj_id = 1 # here I specify any subject number that will be saved as subject ID

subj_num = subj_id - 1 # i subject number for the calculations below
# (Minus one is needed for easier handling of divisibility.)

# Below are all possible items, for now only English examples.
# For each participant, one set (either "1" or "2") will be used for ANS CIT,
# and the other set is used for RT-CIT ("2" or "1", respectively).
# The probe item within each category depends on the subject number; see below.
all_items = {
    1: { # set 1
        "banks": ["Phoenix Community Trust", "Citizen Union Finances", "Vertex Corporation Banks", 
        "Goldward Credit Union", "Springwell Bank Group", "Elysium Holding Company"],
        "forenames": ["Jenks", "Howe", "Snell", "Rand", "Falk", "Croft"],
        "surnames": ["Phil", "Tim", "Ray", "Neil", "Gene", "Ralph"]
    },
    2: { # set 2
        "banks": ["Elysium Holding Company", "Citadel Syndicate Group", "Zenith National Holdings", "Vanguard Savings Bank", "Bulwarks Credit Union", "Phoenix Community Trust"],
        "forenames": ["Spence", "Bryant", "Platt", "Rusk", "Ames", "Dade"],
        "surnames": ["Dale", "Wayne", "Glenn", "Walt", "Tod", "Earl"]
    }}

# Guilt:
# If subject number is divisible by 2, the participant is guilty.
# This is just for information, and not needed for the task.
if ((subj_num) % 2 == 0): 
    guilt = 'guilty'
else:
    guilt = 'innocent'
    

# CIT order:
# If the subject number is in each first set of 2, RT-CIT comes first, ANS-CIT second.
# Otherwise the reverse.
if ((subj_num // 2) % 2 == 0):
    cit_order = 'RT_ANS'
    rt_item_set = 1
    ans_item_set = 2
else:
    cit_order = 'ANS_RT' 
    rt_item_set = 2
    ans_item_set = 1
   
# Set order: 
# If in each first set of 4, set 1 comes first, set 2 comes second.
# Otherwise the reverse.
# (So if e.g. RT-CIT and set 1 both come first, RT-CIT will have set 1 items.)
if ((subj_num // 4) % 2 == 0):
    items_order = '1_2'
    item_sets = [1, 2]
else:
    items_order = '2_1'
    item_sets = [2, 1]



# Block order:
# If in each first set of 8, bank names comes first, names second.
# Otherwise the reverse.
# (Name order is always: first forenames, then surnames.)
if ((subj_num // 8) % 2 == 0):
    block_order = 'banks_names'
    item_cats = ['banks', 'forenames', 'surnames']
else:
    block_order = 'names_banks'
    item_cats = ['forenames', 'surnames', 'banks']
    
# Probe choice:    
# Depending on subject number as specified below, participants may get 
# a certain one of the 5 probes within each category.
# For example, those with subject number below or equal to 40, 
# they get the first item in each category (e.g. "Phoenix Community Trust", "Jenks", "Phil").
# If they are between 41 and 80, they get the second item in each category. And so forth.
# (The "target" in the RT-CIT is always the item that comes after the probe.
# This item is simply skipped in case of ANS-CIT.)
if (subj_num <= 40):
    probe_set = 1
elif (subj_num <= 80):
    probe_set = 2
elif (subj_num <= 120):
    probe_set = 3
elif (subj_num <= 160):
    probe_set = 4
else:
    probe_set = 5
    
# Below is an example of how to select the given participant's items programmatically.

words_base = all_items[item_sets[rt_item_set-1]] # select correct item set
# (Note: in Python, indexing starts at zero, hence the minus one.)
ans_probes = []
ans_controls = []
for categ in item_cats: # iterate through each category
    count = 1
    for item in words_base[categ]: # get the item index within category
        if count == probe_set: # if probe, add to probes
            ans_probes.append(item)
        elif not count == (probe_set + 1): # unless target, add to controls
            ans_controls.append(item)
        count = count + 1

subj_info = '\n-- '.join(['ID: ' + str(subj_num), 'Guilt: ' + guilt, 'CIT order: ' + cit_order,
                          'Set order: ' + items_order, 'Block order: ' + block_order, 
                          'Probe set: ' + str(probe_set)])

print(subj_info)
print('The probes:', ans_probes)
print('The controls:', ans_controls)