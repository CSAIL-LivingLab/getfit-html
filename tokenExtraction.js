function getTokens() {
    var form_token_objects = document.getElementsByName('form_token');
    var form_tokens = [];
    for (var i = 0; i < form_token_objects.length; i++) {
        var value = form_token_objects[i].value;
        form_tokens.push(value);
    };
    return form_tokens;
}

function getBuildIds() {
    var form_build_id_objects = document.getElementsByName('form_build_id');
    var form_build_ids = [];
    for (var i = 0; i < form_build_id_objects.length; i++) {
        var value = form_build_id_objects[i].value;
        form_build_ids.push(value);
    };
    return form_build_ids;
}

function getFormIds() {
    var form_id_objects = document.getElementsByName('form_id');
    var form_ids = [];
    for (var i = 0; i < form_id_objects.length; i++) {
        var value = form_id_objects[i].value;
        form_ids.push(value);
    };
    return form_ids;
}

function getStartIndex() {
    var ids = getFormIds();
    for (var i = 0; i < ids.length; i++) {
        var id = ids[i];
        if (id == 'getfit_minutes_single_form_1') {
            return i;
        };
    };
}
