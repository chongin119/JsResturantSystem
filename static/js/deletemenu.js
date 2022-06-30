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