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


        $.ajax({
            url:"",
            method:"post",
            data:"",
            success:function(resp){
                $('#foodCards').empty();

                let content = `
                    
                `;
            }
        });
    });
}