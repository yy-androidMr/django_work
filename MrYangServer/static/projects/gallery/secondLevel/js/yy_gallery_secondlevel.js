var thum_path;
var middle_path;
var dir_path;
var gallery_name;
var intro_1;
var intro_2;
var media_root = '/static/media';
var curPage = 0;
var pageError = false;
var xmlhttp;
var cur_pool;
var page = 4;

var inload = false;
$(window).scroll(function () {
    var h = $(document.body).height();//网页文档的高度
    var c = $(document).scrollTop();//滚动条距离网页顶部的高度
    var wh = $(window).height(); //页面可视化区域高度

    console.log("wh:" + wh + " c:" + c + "  h:" + h);
    if (pageError) {
        return;
    }
    if (Math.ceil(wh + c) >= h - 100) {
        load_more();
    }
});

function load_more() {
    if (inload) {
        return;
    }
    $('#load_tips').html('正在加载下一页');
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
    // $("#curstate2").html(csrftoken);
    xmlhttp.open("POST", document.URL, true);
    xmlhttp.setRequestHeader('content-type', 'application/x-www-form-urlencoded');
    xmlhttp.setRequestHeader('X-CSRFToken', csrftoken);
    // xmlhttp.setData("page", curPage)
    xmlhttp.onreadystatechange = onLoad;
    // xmlhttp.data = {"page": curPage};
    xmlhttp.send("page=" + curPage);//'page=' + curPage
}

function onLoad(ret) {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        var message = xmlhttp.responseText;
        console.log("加载成功:" + message);
        if (message == null || message == '') {
            pageError = true;
            $('#load_tips').html('所有都加载完毕');
            return;
        }
        var data = JSON.parse(message);
        var next_page = convert_json(data);
        var item_list = insertContent(next_page);
        $("#first_content").viewer('update');
        setTimeout(resetLoad, 100)
    }
}

function resetLoad() {
    $('#load_tips').html('加载完毕');
    inload = false;
}

$(document).ready(function () {
        $('#g_title').html(gallery_name);
        $('#g_intro').html(intro_1);
        $('#g_intro2').html(intro_2);
        $('#load_tips').html('滑动加载');
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

function insertContent(data_list) {
    // return;
    // pic_thum_item
    var parent = $('#first_content');
    var item_list = new Array();
    var cur_poolIndex = 0;

    for (var i = 0; i < data_list.length; i++) {
        var data_item = data_list[i];
        if (cur_pool == null || cur_pool.children('li').length == page) {
            var item = $('#pic_thum_item').clone(true);
            cur_pool = item.find('.folio_list');
            item.children().remove();
            parent.append(cur_pool);
        }
        // pool.parentNode.removeChild(pool);
        // item.removeChild(pool);
        var item2 = $('#pic_thum_item2').clone(true);

        item2.removeAttr('id');
        item2.removeAttr('hidden');

        var thum_pic = item2.find('#pic');
        var t_p = media_root + thum_path + dir_path + '/' + data_item.name;
        var m_p = media_root + middle_path + dir_path + '/' + data_item.name;

        thum_pic.attr('src', t_p);
        thum_pic.attr('data-original', m_p);
        item_list.push(item2);
        // cur_pool.append(item2);
        cur_pool.prepend(item2);
    }


    return item_list;
    // $('#pic_thum_item').remove();
}

function GetCookie()//两个参数，一个是cookie的名子，一个是值
{
    console.log(document.cookie);
    thum_path = sessionStorage.getItem('thum_path');
    dir_path = sessionStorage.getItem('dir_path');
    gallery_name = sessionStorage.getItem('gallery_name');
    intro_1 = sessionStorage.getItem('intro_1');
    intro_2 = sessionStorage.getItem('intro_2');
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
