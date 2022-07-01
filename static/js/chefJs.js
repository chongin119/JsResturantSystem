$(document).ready(function(){
    logoutControl();
    initTable();
    initFeedBackTable();
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
            events:{
                'click .tofinish':function(e,value,row,index){
                    let _orderId = row.id;
                    $.ajax({
                       url:"/chef/finishOrder",
                       method:"post",
                       data:{"id":_orderId},
                       success:function(){
                            $('#chefTable').bootstrapTable('remove', {
                                field: 'id',
                                values: [_orderId]
                              })
                       }
                    });
                }
            },
            formatter:function (value, row, index){
                return '<button class="btn btn-warning tofinish">按此完成</button>'
            },
        }];
    let _table = $('#chefTable');

    _table.bootstrapTable('destroy').bootstrapTable({
        height:550,
        locale: 'zh-CN',
        columns: columns,
        url:"/chef/getHistoryOrder",
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

function logoutControl(){
    $('#logout').on('click',function(){
        $.ajax({
            url:"/chef/logout",
            method:"POST",
            success:function(resp){
                console.log(resp);
                window.location.href = resp;
            }
        });
    });
}

function initFeedBackTable(){
    let icons = {
        detailOpen: 'fa fa-plus',
        detailClose: 'fa fa-minus'
    };
    let columns = [{
            title:'用户',
            field:'username',
            align:'center',
            valign:'middle',
        },{
            title:'反馈内容',
            field:'comment',
            align:'center',
            valign:'middle',
            cellStyle:function (value, row, index){
                return {classes: 'text-danger'}
            },
        }];
    let _table = $('#FeedBackTable');

    _table.bootstrapTable('destroy').bootstrapTable({
        height:550,
        locale: 'zh-CN',
        columns: columns,
        url:"/chef/getFeedBackComment",
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
            html.push(`<h5 class='text-danger'>用户联络资讯:</h5>
                        <span class="text-primary">电话：${row.phone}</span>
                        <br>
                        <span class="text-primary">电邮：${row.email}</span>`);
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