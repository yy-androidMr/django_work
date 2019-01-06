var pageIndex = 0;
var pageItemCount = 9999;//一页有几个
//在界面上初始化
var js_dir;
var play_target_url;
var video_ready = false;

$(document).ready(function () {
        init_video();
        showDir3();
    }
);

function convertBoolean(modelB) {
    if (modelB == 'True') {
        return true;
    }
    return false;
}

function moreDirs() {
    pageIndex++;
    showDir3();
}

function nextLevelDir(dirInfo) {
    js_dir = dirInfo;
    pageIndex = 0;
    showDir3();
    applyLayout1();
}

function showTargetDir(clickData) {
    nextLevelDir(clickData.data);

}

function moviePage() {
    var tiles = $('#tiles');
    var titleName = $('#titleName');
    titleName.unbind();
    if (js_dir.parent == -1) {
        titleName.html('/')
    } else {
        titleName.html(js_dir.path)
        titleName.bind('click', js_dir.parent, showTargetDir);
    }

    var clearContent = pageIndex == 0;
    if (clearContent) {
        tiles.empty();
    }
    var startIndex = pageItemCount * pageIndex;
    var count = pageItemCount;
    //这一页加载数量判断.
    if (startIndex + pageItemCount > js_dir.children.length) {
        count = js_dir.children.length - startIndex;
    }
    var endIndex = startIndex + count;//位置

    for (var i = startIndex; i < endIndex; i++) {
        var file_item = js_dir.children[i];
        var cloneNode = $('#flag').clone(true);
        //修改属性.
        cloneNode.removeAttr('hidden');
        cloneNode.removeAttr('id');
        // cloneNode.attr('style', 'display: list-item; position: absolute; top: 0px; left: 212px;');
        //修改显示内容
        var aTag = cloneNode.find('#item_name');
        var typeTag = cloneNode.find('#item_type');
        typeTag.html("影视");

        var itemImg = cloneNode.find('#itemImg');//需要改变宽高
        if (file_item.info) {
            aTag.html(file_item.info.name);

        } else {
            aTag.html(file_item.name);
        }
        if (file_item.isDir) {

            cloneNode.removeAttr('href');
            cloneNode.bind('click', file_item, showTargetDir);
            if (file_item.children.length > 0) {
                itemImg.attr('src', '/static/images/has_file_folder.png');

            } else {
                itemImg.attr('src', '/static/images/no_file_folder.jpg');

            }
            //
        } else {
            cloneNode.unbind();
            itemImg.attr('src', '/static/images/movie_icon.png');
            // cloneNode.attr('href', 'http://192.168.199.124/movie/' + file_item.path);
            var encode = file_item.path;

            cloneNode.bind('click', encode, showVideo);
            // cloneNode.attr('href', '{% url \'video/\' ' + encode + ' %}');
        }
        tiles.append(cloneNode);
    }
}


function showDir3() {
    moviePage();

}

function SetCookie(name, value)//两个参数，一个是cookie的名子，一个是值
{
    sessionStorage.setItem(name, value);
    // $.cookie(name, encodeURI(value));
}

function showVideo(videoUrl) {

    play_target_url = videoUrl.data;
    play_video(videoUrl.data)
    // SetCookie('url', videoUrl.data);
    // window.open('video');
}

function applyLayout1() {

    $('#tiles').imagesLoaded(function () {
        $('#tiles li').wookmark({
            autoResize: true, // This will auto-update the layout when the browser window is resized.
            container: $('#main'), // Optional, used for some extra CSS styling
            offset: 10, // Optional, the distance between grid items
            outerOffset: 0,
            align: 'center',
            itemWidth: 130 // Optional, the width of a grid item
        });
    });
}

function _showMoive() {
    $.get(
        "aj_mov",
        function (callBack) {
            var movie_root = convert_dirsjson(callBack, MOVIE_TYPE);
            nextLevelDir(movie_root);
        }
    );
}

var MOVIE_TYPE = 1;
var PIC_TYPE = 2;

function _showPic() {
    $.get(
        "aj_pic",
        function (callBack) {
            var pic_root = convert_dirsjson(callBack, PIC_TYPE);
            nextLevelDir(pic_root);
        }
    );
}


function convert_dirsjson(dirsJson, info_json) {

    var rootDir;
    var dirs = new Array();
    var info_map = new Map();
    for (var i = 0, count = info_json.length; i < count; i++) {
        var item = info_json[i];
        var item_key = item.d_id;
        data_item = {
            // 'name', 'duration', 'size', 'source_size', 'fps'
            name: item.name,
            duration: item.duration,
            size: item.size,
            pix: item.source_size,
            fps: item.fps,

        }
        info_map.set(item_key, data_item);
    }

    for (var i = 0, count = dirsJson.length; i < count; i++) {
        var item = dirsJson[i];
        dirs[i] = {
            id: item.id,
            parent: -1,
            // name: null,
            children: [],
            isDir: item.isdir,
            path: item.path,
            tags: item.tags,
            name: item.name,
            info: info_map.get(item.id),
        }

        var dir_split = item.path.split('/');
        dir_split = dir_split.filter(function (n) {
            return n;
        });
        // dirs[i].name = dir_split[dir_split.length - 1];
        if (item.p_id != null) {
            dirs[i].parent = item.p_id;
        } else {
            dirs[i].parent = -1;
            rootDir = dirs[i];
        }
    }
    SetCookie('url', dirs[0].path);


    for (var i = 0; i < dirs.length; i++) {
        var find_parent_item = dirs[i];
        var parent = find_parent_item.parent;
        if (parent == -1) {
            continue;
        }
        for (var j = 0; j < dirs.length; j++) {
            var find_list_item = dirs[j];
            if (find_parent_item != find_list_item) {
                if (find_list_item.id == find_parent_item.parent) {
                    //找到父节点.
                    find_list_item.children[find_list_item.children.length] = find_parent_item;
                    find_parent_item.parent = find_list_item;
                }
            }
        }
    }
    return rootDir;//有且仅有一个

}

function init_video() {
    video_ready = false;
    videoIns = videojs("my-video");


    // videoIns = videojs("my-video");
    // videoIns.ready(function () {
    //     var myPlayer = this;
    //     myPlayer.src({
    //         type: "application/x-mpegURL"
    //     });
    // });

    if (window.addEventListener) {
        document.addEventListener('fullscreenchange', function () {
            HideVideo();
        });
        document.addEventListener('webkitfullscreenchange', function () {
            HideVideo();

        });
        document.addEventListener('mozfullscreenchange', function () {
            HideVideo();

        });
        document.addEventListener('MSFullscreenChange', function () {
            HideVideo();

        });
    }
}

function HideVideo() {
    if (!isFullscreen()) {
        videoIns.pause();
        // videoIns.exitFullscreen();
        // videoIns.exitFullWindow();
        $('#video-div').attr('hidden', '');
    }
}

function isFullscreen() {
    return document.fullscreenElement ||
        document.msFullscreenElement ||
        document.mozFullScreenElement ||
        document.webkitFullscreenElement || false;
}

function play_video(v_name) {
    var url = "http://localhost:909/statics" + v_name + "/out.m3u8";
    // var url = "/电影/0b8d5fd8a64b1de603ed53232d903596.ym3/out.m3u8";
    videoIns = videojs("my-video");
    videoIns.ready(function () {
        var myPlayer = this;
        myPlayer.src({
            src: url,
            type: "application/x-mpegURL"
        });
        myPlayer.requestFullscreen();
        myPlayer.play();

    });

    $('#video-div').removeAttr('hidden');

}