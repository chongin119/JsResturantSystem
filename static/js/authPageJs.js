$(document).ready(function(){
    authInputControl();
});

function authInputControl(){
    $('#inputUsername').on('keyup',function(){
        let _this = $(this);
        let data = {"username":_this.val()}
        $.ajax({
            url:"/auth/validUsername",
            method:"POST",
            data:data,
            success:function(resp){
                if(resp === "success"){
                    _this.removeClass('is-invalid');
                    _this.addClass('is-valid');

                }else{
                    if(resp === "failure")$('#usernameInvalidFeedback').html('此帐号已被使用');
                    else if(resp === "null")$('#usernameInvalidFeedback').html('帐号不能为空');
                    else if(resp === "short")$('#usernameInvalidFeedback').html('帐号过短');

                    _this.removeClass('is-valid');
                    _this.addClass('is-invalid');
                }
                checksubmit();
            }
        });
    });

    $('#inputConPassword').on('keyup',function(){
       let _this = $(this);
       let password = $('#inputPassword').val();
       let Conpassword = _this.val();
       $('#passwordInvalidFeedback').html('请输入两次重覆密码');
        
       if(password.length === 0 || Conpassword.length === 0){
            $('#passwordInvalidFeedback').html('不能为空');

            _this.removeClass('is-valid');
            $('#inputConPassword').removeClass('is-valid');

            $('#inputConPassword').addClass('is-invalid');
            _this.addClass('is-invalid');
        }else{
            if(password === Conpassword){
                _this.removeClass('is-invalid');
                $('#inputPassword').removeClass('is-invalid');
     
                $('#inputPassword').addClass('is-valid');
                _this.addClass('is-valid');
     
            }else{
                _this.removeClass('is-valid');
                $('#inputPassword').removeClass('is-valid');
     
                $('#inputPassword').addClass('is-invalid');
                _this.addClass('is-invalid');
            }
            checksubmit();
        }
    });

    $('#inputPassword').on('keyup',function (){
        let _this = $(this);
        let password = _this.val();
        let Conpassword = $('#inputConPassword').val();
        $('#passwordInvalidFeedback').html('请输入两次重覆密码');

        if(password.length === 0 || Conpassword.length === 0){

            $('#passwordInvalidFeedback').html('不能为空');
            _this.removeClass('is-valid');
            $('#inputConPassword').removeClass('is-valid');

            $('#inputConPassword').addClass('is-invalid');
            _this.addClass('is-invalid');
        }else{

            if(password === Conpassword){
                _this.removeClass('is-invalid');
               $('#inputConPassword').removeClass('is-invalid');
   
               $('#inputConPassword').addClass('is-valid');
               _this.addClass('is-valid');
   
           }else{
               _this.removeClass('is-valid');
               $('#inputConPassword').removeClass('is-valid');
   
               $('#inputConPassword').addClass('is-invalid');
               _this.addClass('is-invalid');
           }
           checksubmit();
        }
     });
}

function checksubmit(){
    let username = document.getElementById('inputUsername');
    let password = document.getElementById('inputPassword');

    if(username.classList.contains('is-valid') && password.classList.contains('is-valid')){
        $('#submitBtn').removeClass('disabled');
    }else{
        $('#submitBtn').addClass('disabled');
    }
}