$(document).ready(function(){
    chooseResturantControl();
});

function chooseResturantControl(){
    let _restA = $('#resturantLst').children().children();
    _restA.on('click',function(){

        let _this = $(this);
        _restA.removeClass('myactive');
        _this.addClass('myactive');

        let _thisId = _this.attr('id');
        _thisId = _thisId.substr(1,this.length);

        let categoryId = {};
        $('#Categorys').children().children('input[type="checkbox"]').each(function (){
           let checked = $(this).prop('checked');
           let id = $(this).attr('id');
           id = id.substr(1,id.length);
           categoryId[`${id}`] = checked;
        });

        categoryId.resturantId = _thisId

        clearCategoryEvent();
        addCategoryEvent();

        $.ajax({
            url:"/user/getFoodCard",
            method:"post",
            data:categoryId,
            success:function(resp){
                $('#foodLst').empty();


                let content = "";
                for(let i of resp.foods){
                    content += `
                        <li class="list-group-item" id=F${i.id}>
                            <div class="d-flex flex-row align-items-center mb-0">
                                <h5 class="me-3 mb-0">${i.name}</h5>
                                <h5 class="text-primary me-auto mb-0">${i.rName}</h5>
                                <h5 class="text-success mb-0 me-3">价格：${i.price}</h5>
                                <button type="button" class="btn btn-info mb-0 me-3 pic" data-bs-toggle="modal" data-bs-target="#exampleModal">视图</button>
                                <button type="button" class="btn btn-warning mb-0 me-3 car">加入购物车</button>
                            </div>
                        </li>                  
                    `;
                }
                $('#foodLst').append(content);

                clearShowPicEvent();
                addShowPicEvent();

                content = '';
                for(let i = 1 ;i<=resp.totalpage;i++){
                    if(i === 1){
                        content += `
                            <li class="page-item"><a class="page-link myactive">${i}</a></li>
                        `;
                    }else{
                        content += `
                            <li class="page-item"><a class="page-link">${i}</a></li>
                        `;
                    }

                }

                $('#pageLst').empty();
                $('#pageLst').append(content);

                document.getElementById('pageLst').scrollIntoView();
            }
        });
    });
}

function addShowPicEvent(){
    let _btns = $('#foodLst').children().children().children('button.pic');

    _btns.each(function (){
        let _this = $(this);
        let _thisId = _this.parent().parent().attr('id');
        //console.log(_thisId);
        _thisId = _thisId.substr(1,_thisId.length);

        _this.on('click',function (){
            $.ajax({
                url:"/user/getFoodPic",
                method:"post",
                data:{"id":_thisId},
                success:function(resp){
                    let imageSRC = 'data:image/jpeg;base64,' + resp;
                    $('#ModalPic>img').attr('src',imageSRC);
                    $('#exampleModalLabel').html(_this.parent().children('h5:eq(0)').html());
                }
            });
        });
    });
}

function clearShowPicEvent(){
    let _btns = $('#foodLst').children().children().children('button.pic');

    _btns.each(function (){
        let _this = $(this);
        let _thisId = _this.parent().parent().attr('id');
        //console.log(_thisId);
        _thisId = _thisId.substr(1,_thisId.length);

        _this.off();
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
        let _resturantId = $('#resturantLst').children().children('a.myactive').attr('id');
        _resturantId = _resturantId.substr(1,_resturantId.length);

        _this.on('click',function(){
            let categoryId = {};
            $('#Categorys').children().children('input[type="checkbox"]').each(function (){
               let checked = $(this).prop('checked');
               let id = $(this).attr('id');
               id = id.substr(1,id.length);
               categoryId[`${id}`] = checked;
            });

            categoryId.resturantId = _resturantId;
            //console.log(_resturantId);

            $.ajax({
                url:"/user/getFoodCard",
                method:"post",
                data:categoryId,
                success:function(resp){
                    $('#foodLst').empty();

                    //console.log(resp);
                    let content = "";
                    for(let i of resp.foods){
                        content += `
                            <li class="list-group-item" id=F${i.id}>
                                <div class="d-flex flex-row align-items-center mb-0">
                                    <h5 class="me-3 mb-0">${i.name}</h5>
                                    <h5 class="text-primary me-auto mb-0">${i.rName}</h5>
                                    <h5 class="text-success mb-0 me-3">价格：${i.price}</h5>
                                    <button type="button" class="btn btn-info mb-0 me-3 pic" data-bs-toggle="modal" data-bs-target="#exampleModal">视图</button>
                                    <button type="button" class="btn btn-warning mb-0 me-3 car">加入购物车</button>
                                </div>
                            </li>                  
                        `;
                    }
                    $('#foodLst').append(content);

                    clearShowPicEvent();
                    addShowPicEvent();

                    content = '';
                    for(let i = 1 ;i<=resp.totalpage;i++){
                        if(i === 1){
                            content += `
                                <li class="page-item"><a class="page-link myactive" style="cursor:pointer;">${i}</a></li>
                            `;
                        }else{
                            content += `
                                <li class="page-item"><a class="page-link" style="cursor:pointer;">${i}</a></li>
                            `;
                        }

                    }

                    $('#pageLst').empty();
                    $('#pageLst').append(content);

                    document.getElementById('pageLst').scrollIntoView();
                }
            });
        })
    });
}