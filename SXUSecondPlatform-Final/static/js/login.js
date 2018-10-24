function $(id)
{
    return document.getElementById(id);
}
function validate()
{
    var re = /[0-9a-zA-Z]{6,16}/; //用户名只能允许由数字和字母构成，长度为6-16个
    var re2 = /^\S{6,16}$/; //密码只允许为非空的字符组成，且长度为6-16个。
    if($("telephone").value=="" || $("telephone").value==null)
    {
        alert("用户名不能为空！");
        return false;
    }
    // if(!re.test($("telephone").value))
    // {
    //     alert("用户名只能允许由数字和字母构成，长度为6-16个");
    //     return false;
    // }


    if($("password").value=="" || $("password").value==null)
    {
        alert("密码不能为空");
        return false;
    }

    if(!re2.test($("password").value))
    {
        alert("密码只允许为非空的字符组成，且长度为6-16个。");
        return false;
    }
    return true;
}


