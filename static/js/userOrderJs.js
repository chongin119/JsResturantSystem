$(document).ready(function(){
    chooseResturantControl();
    carFunc();
    carClickControl();
    initTable();
});

function carEvent(id){
    let json;
    let _thisId = id;
    $.ajax({
        url:"/user/getCarSession",
        method:"post",
        data:"",
        async:false,
        success:function(resp){
            //console.log(resp);
            try{
                json = JSON.parse(resp);
            }catch (e){
                json = "";
            }
            //console.log("json",json);
            if(json === "" || json === null){
                json = {};
                json[`${_thisId}`] = 1;
            }else if (json.hasOwnProperty(`${_thisId}`) === false){
                json[`${_thisId}`] = 1;
            }else{
                json[`${_thisId}`] += 1;
            }
        }
    });

    //console.log(json);

    $.ajax({
        url:"/user/setCarSession",
        method:"post",
        data:{"string":JSON.stringify(json)},
        async:false,
        success:function(resp){
            carFunc(JSON.parse(resp));
        }
    });
}

function picEvent(id,name){
    $.ajax({
        url:"/user/getFoodPic",
        method:"post",
        data:{"id":id},
        success:function(resp){
            let imageSRC = 'data:image/jpeg;base64,' + resp;
            $('#ModalPic>img').attr('src',imageSRC);
            $('#exampleModalLabel').html(name);
        }
    });
}

function initTable(obj = "empty"){
    let columns = [{
            title:'食品名称',
            field:'name',
            align:'center',
            valign:'middle',
        },{
            title:'售卖地方',
            field:'rName',
            align:'center',
            valign:'middle',
            cellStyle:function (value, row, index){
                return {classes: 'text-primary'}
            },
        },{
            title:'价格',
            field:'price',
            align:'center',
            valign:'middle',
            sortable:true,
            cellStyle:function (value, row, index){
                return {classes: 'text-success'}
            },
        },{
            field:'optionFunc',
            align:'center',
            valign:'middle',
            events:{
                'click .pic': function(e,value,row,index){
                    picEvent(row.id,row.name);
                },
                'click .car': function(e,value,row,index){
                    carEvent(row.id);
                }
            },
            formatter:function() {
                return [
                    '<button type="button" class="btn btn-info mb-0 me-3 pic" data-bs-toggle="modal" data-bs-target="#exampleModal">视图</button>',
                    '<button type="button" class="btn btn-warning mb-0 me-3 car" >加入购物车</button>'
                ].join('')
            },
        },{
            title:'食物ID',
            field:'id',
            align:'center',
            valign:'middle',
        }];
    let _table = $('#foodTable');

    if(obj === "empty"){
        _table.bootstrapTable('destroy').bootstrapTable({
            height:550,
            locale: 'zh-CN',
            columns: columns,
        });
        _table.bootstrapTable('hideColumn','id');
    }else{
        _table.bootstrapTable('destroy').bootstrapTable({
            height:550,
            locale: 'zh-CN',
            columns: columns,
            url:"/user/getFoodCardHvPages",
            method:"post",
            sidePagination: 'server',
            pagination:'true',
            pageNumber:1,
            pageSize:10,
            pageList:"",
            dataType:"json",
            queryParams:function (params){
                let req = {
                    pageSize:params.limit,
                    pageNumber:params.offset,
                    data:JSON.stringify(obj),
                }
                return req;
            },
            queryParamsType: "limit",
            onLoadSuccess:function(){
                const ele = document.getElementById('foodTable');
                ele.scrollIntoView();
                //scroll(0,document.documentElement.clientHeight)

            },
        });
        _table.bootstrapTable('hideColumn','id');

    }
}

function chooseResturantControl(){
    let _restA = $('#resturantLst').children().children();
    _restA.on('click',function(){
        let _this = $(this);
        _restA.removeClass('myactive');
        _this.addClass('myactive');

        let _thisId = _this.attr('id');
        _thisId = _thisId.substr(1,this.length);

        let _req = {"categoryIds":{},"resturantId":""};
        $('#Categorys').children().children('input[type="checkbox"]').each(function (){
           let checked = $(this).prop('checked');
           let id = $(this).attr('id');
           id = id.substr(1,id.length);
           _req['categoryIds'][`${id}`] = checked;
        });

        _req.resturantId = _thisId;
        clearCategoryEvent();
        addCategoryEvent();

        initTable(_req);

    });
}

function clearCategoryEvent(){
    let _category = $('#Categorys').children();

    _category.children('input').each(function() {
        let _this = $(this);

        _this.off();
    });
}

function addCategoryEvent(){
    let _category = $('#Categorys').children();

    _category.children('input').each(function(){
        let _this = $(this);
        let _resturantId = $('#resturantLst').children().children('button.myactive').attr('id');
        _resturantId = _resturantId.substr(1,_resturantId.length);

        _this.on('click',function(){

            let _req = {"categoryIds":{},"resturantId":""};
            $('#Categorys').children().children('input[type="checkbox"]').each(function (){
               let checked = $(this).prop('checked');
               let id = $(this).attr('id');
               id = id.substr(1,id.length);
               _req['categoryIds'][`${id}`] = checked;
            });

            _req.resturantId = _resturantId;
            //console.log(_resturantId);

            clearCategoryEvent();
            addCategoryEvent();

            initTable(_req);
        })
    });
}