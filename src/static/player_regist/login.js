
$(function () {

    $("#btnregister").click(function () {
        var account = $("#account").val();
        var pwd = $("#pwd").val();
        var mobile = $("#mobile").val();
        var qq = $("#qq").val();
        var agent = $("#hdagent").val();
        var code = $("#code").val();

        $.ajax({
            url: '/postregister',
            type: 'POST',
            data: {
                'account': account,
                'pwd': pwd,
                'code': code,
                'mobile': mobile,
                'qq':qq,
                'agent': agent
            },
            success: function (result) {
                if (result.success) {
                    alert("注册成功");
                    window.location.reload();
                }
                else {
                    $("#error").html(result.error);
                }
            }
        })
    });
    $("#btnlogin").click(function () {
        var account = $("#account").val();
        var pwd = $("#pwd").val();
        var agent = $("#hdagent").val();
        $.ajax({
            url: '/tlbb/postlogin',
            type: 'POST',
            data: {
                'account': account,
                'pwd': pwd,
            },
            success: function (result) {
                if (result.IsSuccess) {
                    localStorage.setItem("account", account);
                    localStorage.setItem("pwd", pwd);
                }
                else {
                    $("#error").html(result.Message);
                }
            }
        })
    });

    $("#btnpassword").click(function () {
        var account = $("#account").val();
        var pwd = $("#pwd").val();
        var confirmpwd = $("#confirmpwd").val();
        $.ajax({
            url: '/tlbb/postpassword',
            type: 'POST',
            data: {
                'account': account,
                'pwd': pwd,
                'confirmpwd': confirmpwd
            },
            success: function (result) {
                if (result.IsSuccess) {
                    alert("修改成功");
                    window.location.reload();
                }
                else {
                    layer.alert(result.Message, { icon: 2 });
                }
            }
        })
    });
})