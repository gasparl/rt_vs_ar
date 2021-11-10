/*jshint esversion: 6 */

let subj_id, guilt, cit_order, block_order, probe_set, item_sets, item_cats, filename_to_dl;

all_items = {
    1: {
        "banks": ["Phoenix Community Trust", "Citizen Union Finances", "Vertex Corporation Banks", "Goldward Credit Union", "Springwell Bank Group", "Elysium Holding Company"],
        "surnames": ["Phil Jenks", "Tim Howe", "Ray Snell", "Neil Rand", "Gene Falk", "Ralph Croft"],
        "forenames": ["kocht57", "langen92", "mullf29", "kugerh83", "hornm64", "bohml56"]
    },
    2: {
        "banks": ["Elysium Holding Company", "Citadel Syndicate Group", "Zenith National Holdings", "Vanguard Savings Bank", "Bulwarks Credit Union", "Phoenix Community Trust"],
        "surnames": ["Dale Spence", "Wayne Bryant", "Glenn Platt", "Walt Rusk", "Tod Ames", "Earl Dade"],
        "forenames": ["nowakp36", "huberm94", "mullerf27", "schrobh84", "kugele41", "bohmej58"]
    }
};

function subj_info() {
    subj_id = document.getElementById('subj_num').value;
    let subj_num = parseInt(subj_id) - 1;
    let type_ans = 'polygraph based';
    let type_rt = 'response time based';
    if (subj_id != '' && subj_num > -1 && subj_num < 300) {
        if (Math.floor(subj_num) % 2 == 0) {
            guilt = 'guilty';
        } else {
            guilt = 'innocent';
        }
        if (Math.floor(subj_num / 2) % 2 == 0) {
            cit_order = 'first RT then ANS';
            document.getElementById('cit1').textContent = type_rt;
            document.getElementById('cit11').textContent = type_rt;
            document.getElementById('cit2').textContent = type_ans;
            document.getElementById('cit22').textContent = type_ans;
        } else {
            cit_order = 'first ANS then RT';
            document.getElementById('cit1').textContent = type_ans;
            document.getElementById('cit11').textContent = type_ans;
            document.getElementById('cit2').textContent = type_rt;
            document.getElementById('cit22').textContent = type_rt;
        }
        if (Math.floor(subj_num / 4) % 2 == 0) {
            set_order = 'set 1 first';
            item_sets = [1, 2];
        } else {
            set_order = 'set 2 first';
            item_sets = [2, 1];
        }
        if (Math.floor(subj_num / 8) % 2 == 0) {
            block_order = 'first banks then personal names';
            item_cats = ['banks', 'forenames', 'surnames'];
        } else {
            block_order = 'first personal names then banks';
            item_cats = ['forenames', 'surnames', 'banks'];
        }
        document.getElementById('subj_num_re').textContent = subj_id;
        document.getElementById('guilt').textContent = guilt;
        document.getElementById('cit_order').textContent = cit_order;
        document.getElementById('set_order').textContent = set_order;
        document.getElementById('block_order').textContent = block_order;
        if (subj_num < 40) {
            probe_set = 1;
        } else if (subj_num < 80) {
            probe_set = 2;
        } else if (subj_num < 120) {
            probe_set = 3;
        } else if (subj_num < 160) {
            probe_set = 4;
        } else {
            probe_set = 5;
        }
        document.getElementById('start_btn').style.display = 'block';
    }
}

function start() {
    filename_to_dl = 'rt_vs_ar_' + subj_id + '_' + neat_date() + '.txt';
    if (guilt == 'innocent') {
        let els = document.getElementsByClassName('g_only');
        for (var i = 0; i < els.length; i++) {
            els[i].style.display = 'none';
        }
    }
    document.getElementById('outro_start').style.display = 'none';
    document.getElementById('outro_main').style.display = 'block';
    create_stim_base();
}

let all_probes = [];
let words_lists = [];

function create_stim_base() {

    item_sets.forEach((it_set, num1) => {
        words_lists.push([]);
        item_cats.forEach((itemskey, num2) => {
            itemlist = all_items[it_set][itemskey];
            words_lists[num1].push([]);
            itemlist.forEach((item, indx) => {
                if ((probe_set - 1) === indx) {
                    words_lists[num1][num2].push(item);
                    all_probes.push(item);
                } else if (probe_set !== indx) {
                    words_lists[num1][num2].push(item);
                }
            });
            words_lists[num1][num2] = words_lists[num1][num2].sort(function(a, b) {
                return a.localeCompare(b);
            });
            words_lists[num1][num2].push("I don't know.");
        });
    });
    words_lists.forEach((wbase, ind1) => {
        wbase.forEach((wlist, ind2) => {
            let radopts = "";
            wlist.forEach(function(word) {
                radopts += word + ' <input type="radio" name="pch' + (ind1 + 1) + ind2 + '" value="' + word + '"><br>';
            });
            let el = document.getElementById('div_pcheck' + (ind1 + 1) + ind2);
            el.innerHTML += radopts;
        });
    });
}

let pchosen = [];
let pcount = 0;

function submit() {
    let len = 9;
    let pfeed = '';
    if (guilt == 'guilty') {
        ['pch10', 'pch11', 'pch12', 'pch20', 'pch21', 'pch22'].forEach((prob) => {
            let p_chk = document.querySelector('input[name="' + prob + '"]:checked');
            pchosen.push(p_chk ? p_chk.value : undefined);
        });
        len = pchosen.filter((v) => {
            return v !== undefined;
        }).length;
        pchosen.forEach((seldprobe, idx) => {
            theprob = all_probes[idx];
            if (seldprobe == theprob) {
                pfeed += seldprobe + ' -> <b>correct (' + theprob + ')</b><br>';
                pcount += 1;
            } else {
                pfeed += '<span style="color:red">' + seldprobe + ' -> <b>INCORRECT (' + theprob + ')</b></span><br>';
            }
        });
        pfeed += '<br>Correct count: ' + pcount + ' out of all 6.';
    } else {
        pfeed = "(Not guilty.)";
        all_probes = [];
        pcount = '';
    }
    document.getElementById('probsfeed').innerHTML = pfeed;
    if (len < 6) {
        alert('Please select an option in each of the 6 lists of items!');
    } else {
        document.getElementById('outro_main').style.display = 'none';
        window.scrollTo(0, 0);
        document.getElementById('outro_end').style.display = 'block';
    }
}

function moveon() {
    document.getElementById('outro_end').style.display = 'none';
    if (guilt == 'guilty') {
        document.getElementById('outro_check_g').style.display = 'block';
    } else {
        document.getElementById('outro_check_i').style.display = 'block';
    }
}

let outro_data = '';

function end_save() {
    show_check = document.getElementById('show_check').value;
    if (guilt == 'innocent' || ['0', '1', '2', '3', '4', '5', '6'].includes(show_check)) {
        document.getElementById('outro_check_g').style.display = 'none';
        document.getElementById('outro_check_i').style.display = 'none';
        let gend_chk = document.querySelector('input[name="gender"]:checked');
        let gender = gend_chk ? gend_chk.value : 'NA';
        let age = document.getElementById('age').value;

        let scales = ['realism', 'anxiety', 'excitement',
            'detected1', 'detected2', 'accuracy1', 'accuracy2'
        ];
        let rats = [];
        scales.forEach((scl) => {
            if (document.getElementById(scl).classList.contains("slider_hide_thumb")) {
                rats.push('NA');
            } else {
                rats.push(document.getElementById(scl).value);
            }
        });

        outro_data += ['subject_id', 'age', 'gender', 'selected_probes', 'actual_probes', 'correct_selected', 'correct_noted', 'attention'].join('\t') + '\t' + scales.join('\t') + '\n' + [subj_id, age, gender, pchosen.join('|'), all_probes.join('|'), pcount, show_check, attcount].join('\t') + '\t' + rats.join('\t');

        console.log(outro_data);
        document.getElementById('data_display').innerHTML = filename_to_dl + "\n" + outro_data;
        dl_as_file();
    }
}

function dl_as_file() {
    data_to_dl = outro_data;
    let blobx = new Blob([data_to_dl], {
        type: 'text/plain'
    });
    let elemx = window.document.createElement('a');
    elemx.href = window.URL.createObjectURL(blobx);
    elemx.download = filename_to_dl;
    document.body.appendChild(elemx);
    elemx.click();
    document.body.removeChild(elemx);
}

function copy_to_clip() {
    let textarea = document.createElement("textarea");
    textarea.textContent = filename_to_dl + "\n" + outro_data;
    textarea.style.position = "fixed";
    document.body.appendChild(textarea);
    textarea.select();
    try {
        return document.execCommand("copy");
    } catch (ex) {
        console.warn("Copy to clipboard failed.", ex);
        return false;
    } finally {
        document.body.removeChild(textarea);
    }
}

function neat_date() {
    let m = new Date();
    return m.getFullYear() + "_" +
        ("0" + (m.getMonth() + 1)).slice(-2) + "" +
        ("0" + m.getDate()).slice(-2) + "_" +
        ("0" + m.getHours()).slice(-2) + "" +
        ("0" + m.getMinutes()).slice(-2);
}


//only allow number in input field
function validate(evt) {
    var theEvent = evt || window.event;
    var key = theEvent.keyCode || theEvent.which;
    key = String.fromCharCode(key);
    var regex = /[0-9]/;
    if (!regex.test(key)) {
        theEvent.returnValue = false;
        if (theEvent.preventDefault) theEvent.preventDefault();
    }
}


let attcount = 0;

function attchecks() {
    document.getElementById("attcheck_id").classList.remove("slider_hide_thumb");
    attcount++;
    if (attcount > 2) {
        document.getElementById('attdiv').innerHTML = "<br><b>Good! Thanks for paying attention! You can continue.</b><br><br>";
    }
}
