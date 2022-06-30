$(document).ready(function(){
    carFunc();
    carClickControl();
    initTable();
});

function initTable(){
    let icons = {
        detailOpen: 'fa fa-plus',
        detailClose: 'fa fa-minus'
    };
    let columns = [{
            title:'訂单号',
            field:'id',
            align:'center',
            valign:'middle',
        },{
            title:'食品',
            field:'orderFood',
            align:'center',
            valign:'middle',
        },{
            title:'下单时间',
            field:'time',
            align:'center',
            valign:'middle',
            cellStyle:function (value, row, index){
                return {classes: 'text-primary'}
            },
        },{
            title:'总价',
            field:'sumOfPrice',
            align:'center',
            valign:'middle',
            cellStyle:function (value, row, index){
                return {classes: 'text-success'}
            },
        },{
            title:'状态',
            field:'status',
            align:'center',
            valign:'middle',
            formatter:function (value, row, index){
                if(row.status === 0 ){
                    return '<button class="btn btn-warning disabled">没有完成</button>'
                }else{
                    return '<button class="btn btn-success disabled">已完成</button>'
                }
            },
        }];
    let _table = $('#historyTable');

    _table.bootstrapTable('destroy').bootstrapTable({
        height:550,
        locale: 'zh-CN',
        columns: columns,
        url:"/user/getHistoryOrder",
        method:"post",
        sidePagination: 'server',
        pagination:'true',
        pageNumber:1,
        pageSize:10,
        pageList:"",
        detailView:true,
        icons:icons,
        detailFormatter:function (index,row){
            let html =[];
            html.push(`<h5 class='text-danger'>取货地点:</h5><span>${row.resturant}</span>`);
            html.push(`<br><br><h5 class='text-danger'>订单备注:</h5><span>${row.comment}</span>`);
            return html.join('');
        },
        dataType:"json",
            queryParams:function (params){
                let req = {
                    pageSize:params.limit,
                    pageNumber:params.offset,
                }
                return req;
            },
            queryParamsType: "limit",
    });
}