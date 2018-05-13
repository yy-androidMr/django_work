var thum_path;
var middle_path;
var dir_path;
var gallery_name;
var media_root = '/static/media';
var curPage = 0;
var pageError = false;
var xmlhttp;


var inload = false;
$(window).scroll(function () {
    var h = $(document.body).height();//网页文档的高度
    var c = $(document).scrollTop();//滚动条距离网页顶部的高度
    var wh = $(window).height(); //页面可视化区域高度

    // console.log("wh:" + wh + " c:" + c + "  h:" + h);
    if (pageError) {
        return;
    }
    if (Math.ceil(wh + c) >= h - 100) {
        if (inload) {
            return;
        }
        $('#curstate').html('正在加载图片....');
        inload = true;

        curPage++;
        var csrftoken = getMyCookie('csrftoken');

        if (window.XMLHttpRequest) {
            //  IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
            xmlhttp = new XMLHttpRequest();
        }
        else {
            // IE6, IE5 浏览器执行代码
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
        }
        xmlhttp.onreadystatechange = function () {
            // if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            //     document.getElementById("myDiv").innerHTML = xmlhttp.responseText;
            // }
        }
        // $("#curstate2").html(csrftoken);
        xmlhttp.open("POST", document.URL, true);
        xmlhttp.setRequestHeader('content-type', 'application/x-www-form-urlencoded');
        xmlhttp.setRequestHeader('X-CSRFToken', csrftoken);
        // xmlhttp.setData("page", curPage)
        xmlhttp.onreadystatechange = onLoad;
        // xmlhttp.data = {"page": curPage};
        xmlhttp.send("page=" + curPage);//'page=' + curPage

        // $.ajax({
        //     beforeSend: function (request) {
        //         request.setRequestHeader('X-CSRFToken', csrftoken);
        //     },
        //     url: document.URL,
        //     type: "POST",
        //     data: {"page": curPage},
        //     success: onLoad,
        // });
        // $.post('', onLoad)
    }
});

function onLoad(ret) {

    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        var message = xmlhttp.responseText;
        console.log("加载成功:" + message);
        if (message == null || message == '') {
            pageError = true;
            $('#curstate').html('已经到底了...');
            return;
        }
        var data = JSON.parse(message);
        var next_page = convert_json(data);
        var item_list = insertContent(next_page);
        play_fateInAnim(item_list);
        $("#main").viewer('update');
        setTimeout(resetLoad, 100)
    }
}

function resetLoad() {
    $('#curstate').html('加载完了');
    inload = false;
}

$(document).ready(function () {
        $('#gallery_name').html(gallery_name);
        insertContent(level2_dir);
    }
);


function getMyCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var fullscreen = function () {
    elem = document.body;
    if (elem.webkitRequestFullScreen) {
        elem.webkitRequestFullScreen();
    } else if (elem.mozRequestFullScreen) {
        elem.mozRequestFullScreen();
    } else if (elem.requestFullScreen) {
        elem.requestFullscreen();
    } else {
        //浏览器不支持全屏API或已被禁用
    }
}

function play_fateInAnim(item_list) {
    // for (var i = 0; i < item_list.length; i++) {
    //     var thum_ = item_list[i].find('.thumb');
    //     thum_.css({
    //         "-moz-transition-delay": i + '.25s',
    //         '-webkit-transition-delay': i + '.25s',
    //         '-ms-transition-delay': i + '.25s'
    //     });
    // thum_.setAttribute('-moz-transition-delay', i + '.25s');
    // thum_.setAttribute('-webkit-transition-delay', i + '.25s');
    // thum_.setAttribute('-ms-transition-delay', i + '.25s');
    // thum_.setAttribute('transition-delay', i + '.25s');
    // }
}

function insertContent(data_list) {
    // return;
    // pic_thum_item
    var parent = $('#main');
    var item_list = new Array();
    for (var i = 0; i < data_list.length; i++) {
        var data_item = data_list[i];
        var item = $('#pic_thum_item').clone(true);
        item.removeAttr('style');
        item.removeAttr('id');

        var thum_pic = item.find('#pic');
        var t_p = media_root + thum_path + dir_path + '/' + data_item.name;
        var m_p = media_root + middle_path + dir_path + '/' + data_item.name;

        thum_pic.attr('src', t_p);
        thum_pic.attr('data-original', m_p);
        item_list.push(item);
        parent.append(item);

    }

    return item_list;
    // $('#pic_thum_item').remove();
}

function GetCookie()//两个参数，一个是cookie的名子，一个是值
{
    console.log(document.cookie);
    // thum_path = decodeURI($.cookie('thum_path'));
    // dir_path = decodeURI($.cookie('dir_path'));
    // gallery_name = decodeURI($.cookie('gallery_name'));
    thum_path = sessionStorage.getItem('thum_path');
    dir_path = sessionStorage.getItem('dir_path');
    gallery_name = sessionStorage.getItem('gallery_name');
}

var level2_dir;

function convert_json(json) {
    var dirs = new Array();
    for (var i = 0, count = json.length; i < count; i++) {
        var item = json[i];
        dirs[i] = {
            name: item.name,
            c_id: item.c_id,
        }
    }
    return dirs;
}

function convert_2pic(dirsJson, path) {
    curPage = 1;
    middle_path = path;
    pageError = false;
    GetCookie();
    level2_dir = convert_json(dirsJson);
}
