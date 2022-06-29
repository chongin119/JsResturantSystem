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

                console.log(resp);
                let content = "";
                for(let i of resp.foods){
                    content += `
                        <li class="list-group-item" id=F${i.id}>
                            <div class="d-flex flex-row align-items-center mb-0">
                                <h5 class="me-auto mb-0">${i.name}</h5>
                                <h5 class="text-success mb-0 me-3">价格：${i.price}</h5>
                                <button type="button" class="btn btn-info mb-0 me-3">视图</button>
                                <button type="button" class="btn btn-warning mb-0 me-3">加入购物车</button>
                            </div>
                        </li>                  
                    `;
                }
                $('#foodLst').append(content);

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
            console.log(_resturantId);

            $.ajax({
                url:"/user/getFoodCard",
                method:"post",
                data:categoryId,
                success:function(resp){
                    $('#foodLst').empty();

                    console.log(resp);
                    let content = "";
                    for(let i of resp.foods){
                        content += `
                            <li class="list-group-item" id=F${i.id}>
                                <div class="d-flex flex-row align-items-center mb-0">
                                    <h5 class="me-auto mb-0">${i.name}</h5>
                                    <h5 class="text-success mb-0 me-3">价格：${i.price}</h5>
                                    <button type="button" class="btn btn-info mb-0 me-3">视图</button>
                                    <button type="button" class="btn btn-warning mb-0 me-3">加入购物车</button>
                                </div>
                            </li>                  
                        `;
                    }
                    $('#foodLst').append(content);

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
        })
    });
}