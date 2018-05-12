var thum_path;
var middle_path;
var dir_path;
var gallery_name;
var media_root = '/static/media';


$(document).ready(function () {
        $('#gallery_name').html(gallery_name);
        insertContent();
    }
);

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

function insertContent() {
    // return;
    // pic_thum_item
    var parent = $('#main');
    for (var i = 0; i < level2_dir.length; i++) {
        var data_item = level2_dir[i];
        var item = $('#pic_thum_item').clone(true);
        item.removeAttr('style');
        item.removeAttr('id');

        var thum_pic = item.find('#pic');
        var t_p = media_root + thum_path + dir_path + '/' + data_item.name;
        var m_p = media_root + middle_path + dir_path + '/' + data_item.name;

        thum_pic.attr('src', t_p);
        thum_pic.attr('data-original', m_p);

        parent.append(item);

    }

    // $('#pic_thum_item').remove();
}

function GetCookie()//两个参数，一个是cookie的名子，一个是值
{
    thum_path = decodeURI($.cookie('thum_path'));
    dir_path = decodeURI($.cookie('dir_path'));
    gallery_name = decodeURI($.cookie('gallery_name'));
}

var level2_dir;

function convert_2pic(dirsJson, path) {
    middle_path = path;
    GetCookie();
    var dirs = new Array();
    for (var i = 0, count = dirsJson.length; i < count; i++) {
        var item = dirsJson[i];
        dirs[i] = {
            name: item.name,
            c_id: item.c_id,
        }
        // if (item.tags[0].length != 0) {
        //     dirs[i].name = item.tags[0];//dir_split[dir_split.length - 1];
        // } else {
        //     dirs[i].name = '暂未命名';//dir_split[dir_split.length - 1];
        // }
        // if (item.tags.length > 1) {
        //     if (item.tags[1].length != 0) {
        //         dirs[i].intro = item.tags[1];//dir_split[dir_split.length - 1];
        //     } else {
        //         dirs[i].intro = '没有任何描述';
        //     }
        // }
        // dirs[i].time = '';
        // if (item.tags.length > 2) {
        //     dirs[i].time = item.tags[2];//dir_split[dir_split.length - 1];
        // }
        //
        // if (item.tags.length > 3) {
        //     dirs[i].thum = item.tags[3];//dir_split[dir_split.length - 1];
        //     // 这里没有临时文件
        // }

        // if (item.p_id != null) {
        //     dirs[i].parent = item.p_id;
        // } else {
        //     dirs[i].parent = -1;
        //     rootDir = dirs[i];
        // }
    }
    level2_dir = dirs;
}
