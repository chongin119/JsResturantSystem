function carClickControl(){
    let _btn = $('#carObjBtn');
    let _Modal = $('#ModalCarBody');

    _btn.on('click',function(){
        _Modal.empty();
        let content = '';
        let obj;
        $.ajax({
            url:"/user/getCarSession",
            method:"post",
            async:false,
            success:function(resp){
                obj = JSON.parse(resp);
            }
        });

        $.ajax({
            url:"/user/getCarLst",
            method:"post",
            async:false,
            data:obj,
            success:function(resp){
                let sum = 0;
                for(let i in resp){
                    content += `<h3 class="w-100 border-bottom">${i}</h3>`;
                    content += '<ul class="list-group list-group-flush mb-3">';
                    //console.log(resp[i])
                    for(let j of resp[i]){
                        //console.log(j);
                        sum += j.price * parseInt(j.count);
                        content += `<li class="list-group-item d-flex flex-row">
                                        <h5 class="text-secondary me-auto mb-0">${j.name}</h5>
                                        <h5 class="text-success mb-0 me-3">${j.price}</h5>
                                        <h5 class="text-danger mb-0 me-3">x${j.count}</h5>
                                    </li>`

                    }
                    content += '</ul>';
                }
                _Modal.append(content);
                $('#sumPrice').html(`总价：${sum}`);

                $('#createOrder').on('click',function(){
                    $.ajax({
                        url:"/user/createOrder",
                        method:"post",
                        data:"",
                        success:function(){

                        }
                    })
                });
            }
        });
    });
}

function carFunc(obj = "empty"){
    let sum = 0;

    if(obj === "empty"){
        $.ajax({
            url:"/user/getCarSession",
            method:"post",
            async:false,
            success:function(resp){
                obj = JSON.parse(resp);
            }
        });
    }

    for(let i in obj){
        sum += parseInt(obj[i]);
    }

    let _carCount = $('#carObj');
    if(sum === 0){
        _carCount.addClass('d-none');
    }else{
        _carCount.html(sum.toString());
        _carCount.removeClass('d-none');
    }
}