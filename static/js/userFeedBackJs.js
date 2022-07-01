$(document).ready(function(){
    carFunc();
    carClickControl();
    dropDownControl();
    submitControl();

    let need = getQueryVariable('need')
    if(need === "true"){
        let myToast = new bootstrap.Toast(document.querySelector('.toast'));
        myToast.show();
    }
});

function dropDownControl(){
    let _a = $('#RRdropDown').children().children('a');
    _a.on('click',function(){
        let _this = $(this);
        let _thisId = _this.parent().attr('id');
        _thisId = _thisId.substr(2,_thisId.length);
        $('#dropdownMenuButton1').html(_this.html());
        $('#rrInput').val(_thisId);
    });
}

function submitControl(){
    $('#submitBtn').on('click',function(){
        let _Rid = $('#rrInput').val();
        let _comment = $("#feedBackComment").val();
        if(_Rid !== "" && _comment !== ""){

            $.ajax({
               url:"/user/sendFeedBackComment",
               method:"post",
               data:{"id":_Rid,"comment":_comment},
               success:function(){
                   window.location = window.location + "?need=true";
               }
            });
        }
    });
}

function getQueryVariable(variable)
{
       var query = window.location.search.substring(1);
       var vars = query.split("&");
       for (var i=0;i<vars.length;i++) {
               var pair = vars[i].split("=");
               if(pair[0] == variable){return pair[1];}
       }
       return false;
}