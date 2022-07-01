function deletemenu(object){
    var id = $(object).attr('id');
    $.ajax({
        url:'deletemenu',
        method:'POST',
        data:{'id': id},
    });
    var tr = object.parentNode.parentNode;
    table = tr.parentNode;
    var rowIndex = tr.rowIndex;
    table.deleteRow(rowIndex);
}

function deleteorder(object){
    var id = $(object).attr('id');
    $.ajax({
        url:'ordermanage',
        method:'POST',
        data:{'id': id},
    });
    var tr = object.parentNode.parentNode;
    table = tr.parentNode;
    var rowIndex = tr.rowIndex;
    table.deleteRow(rowIndex);
}

function acceptorder(object){
    var id = $(object).attr('id')
    $.ajax({
        url:'acceptorder',
        method:'POST',
        data:{'ac_id': id},
        async: false
    })
    window.location.href = window.location.href
}