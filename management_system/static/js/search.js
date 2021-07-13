function search_All() {
    $.get(
        '/search', {
            search_query: $('#overlay_search').val(),
        },
        function(data) {
            let search_result = document.getElementById('search_result');

            search_result.innerText = "";

            for (i = 0; i < data.search_list.length; i++) {

                let search_object = data.search_list[i];
                let search_card = document.createElement('div');
                let search_card_img = document.createElement('div');
                let img = document.createElement('img');
                let search_card_text = document.createElement('div');
                let key_link = document.createElement('a');
                let name = document.createElement('h3');
                let para = document.createElement('p');
                let search_card_text_value = document.createElement('span');

                search_card.className = "search_card";
                search_card_img.className = "search_card_img";
                search_card_text.className = "search_card_text";
                search_card_text_value.className = "search_card_text_value";

                img.src = search_object['image'];
                search_card_img.appendChild(img);

                search_card_text_value.textContent = search_object['owner'];
                para.innerText = " ";
                para.appendChild(search_card_text_value);
                key_link.href = search_object['key'] + "/";
                name.innerText = search_object['name'];
                key_link.appendChild(name);

                search_card_text.appendChild(key_link);
                search_card_text.appendChild(para);

                search_card.appendChild(search_card_img);
                search_card.appendChild(search_card_text);

                search_result.append(search_card);

            }
        }
    );
}

function get_search_objects_list(search_class) {
    let search_objects_list = document.getElementsByClassName(search_class);
    //console.log(search_objects_list);
    return search_objects_list;
}

function compute_lps(pattern) {

    let lps = new Array(pattern.length).fill(0);

    let prefix = 0;

    for (let i = 1; i < pattern.length; i++) {
        while (prefix && pattern[i] != pattern[prefix]) {
            prefix = lps[prefix - 1];
        }

        if (pattern[prefix] == pattern[i]) {
            prefix += 1;
            lps[i] = prefix;
        }
    }
    return lps;
}

function* enumerate(it, start = 0) {
    let i = start;
    for (const x of it)
        yield [i++, x];
}

function kmp(pattern, text) {
    //console.log(pattern);
    //console.log(text);
    let match_indices = new Array(0);
    let pattern_lps = compute_lps(pattern);

    let patterni = 0;

    for (const [i, ch] of enumerate(text)) {
        //console.log(i + " " +ch);
        while (patterni && pattern[patterni] != ch) {
            patterni = pattern_lps[patterni - 1];
        }
        if (pattern[patterni] == ch) {
            if (patterni == (pattern.length - 1)) {
                match_indices.push(i - patterni);
                break;
            } else
                patterni += 1;
        }

    }
    //console.log("Match indices "+match_indices.length);
    return match_indices;
}

function create_pair(index, search_string) {
    this.index = index;
    this.search_string = search_string;
}

function compare(a, b) {
    if (a.index < b.index)
        return -1;
    if (a.index > b.index)
        return 1;
    return 0;
}

function search_pattern(pattern_id, query_parameter, display_type, search_class, parent_class) {
    //console.log(query_parameter);
    //console.log(search_class);
    let pattern = document.getElementById(pattern_id).value;
    //console.log(pattern);
    let pairs = new Array();
    let search_objects_list = get_search_objects_list(search_class);
    let parent_objects_list = get_search_objects_list(parent_class);
    //console.log(search_objects_list);
    for (i = 0; i < search_objects_list.length; i++) {
        search_object = search_objects_list[i];
        let search_string;
        if (query_parameter == '')
            search_string = search_object.innerText;
        else
            search_string = search_object.querySelector(query_parameter).innerText;
        //console.log(search_string);
        let match_indices = kmp(pattern.toLowerCase().replace(/\s+/g, ''), search_string.toLowerCase().replace(/\s+/g, ''));
        let child_object = search_object;
        let parent_card = parent_objects_list[i];
        //console.log(parent_card);
        /*for (let i = level_of_parent; i > 0; i--) {
            parent_card = child_object.parentNode;
            child_object = parent_card;
        }*/
        //console.log(parent_card);
        //console.log(catalog_card);
        if (match_indices.length > 0 || pattern == "") {
            parent_card.className = parent_class;
            parent_card.className += " " + display_type;
        } else {
            parent_card.className = parent_class;
            parent_card.className += " " + 'display_none';
        }

    }
    //pairs.sort(compare);
    // let return_search_list = new Array();
    // pairs.forEach((element) => {
    //     return_search_list.push(element.search_string);
    // });

    // return return_search_list;
}